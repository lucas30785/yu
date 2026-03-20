#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador automatico de M3U8 para canais do YouTube ao vivo.
Mescla uma base estatica (EPG + canais fixos) com links dinamicos do YouTube.
"""
import io
import subprocess
import threading
import time
import os
import sys
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

IS_CI = os.environ.get("GITHUB_ACTIONS") == "true"

# ============================================================
# CONFIGURACAO
# ============================================================
# Canais que serao extraidos do YouTube automaticamente
CANAIS_YOUTUBE = [
    {
        "nome": "TV Cancao Nova",
        "url": "https://www.youtube.com/watch?v=zSN0ospdIaE",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/thumb/3/3f/Logotipo_da_TV_Can%C3%A7%C3%A3o_Nova.png/330px-Logotipo_da_TV_Can%C3%A7%C3%A3o_Nova.png",
        "grupo": "Catolico",
    },
    {
        "nome": "TV Jornal Caruaru",
        "url": "https://www.youtube.com/@TVJornalInterior/live",
        "logo": "https://imgmxa.net/sbt.png",
        "grupo": "PE",
    },
    {
        "nome": "Canal Rural",
        "url": "https://www.youtube.com/watch?v=hmUCjG_P0xg",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/thumb/a/a3/Canal_Rural.png/300px-Canal_Rural.png",
        "grupo": "Variedades",
    },
    {
        "nome": "Rede Vida +",
        "url": "https://www.youtube.com/@REDEVIDAMAIS/live",
        "logo": "https://redevida.com.br/wp-content/uploads/2024/07/logo-redevida.png.webp",
        "grupo": "Catolico",
    },
]

ARQUIVO_BASE = "playlist_base.m3u"
ARQUIVO_SAIDA = "playlist.m3u"
INTERVALO_SEGUNDOS = 3600   # Atualiza a cada 1 hora
TIMEOUT_CANAL = 30          # Tempo maximo por canal
# ============================================================


def _rodar_ytdlp(url, resultado_container, extract_all=False):
    """Executa yt-dlp em thread separada com suporte a cookies e fallbacks."""
    try:
        flags = 0
        if sys.platform == "win32":
            flags = subprocess.CREATE_NO_WINDOW
        
        base_cmd = [
            "yt-dlp",
            "--no-update",
            "--no-playlist",
            "--js-runtimes", "node",
            "--socket-timeout", "15",
            "--retries", "1",
            "--fragment-retries", "1",
        ]

        if IS_CI:
            # Tenta logar a versao do yt-dlp no CI
            try:
                v_proc = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
                if v_proc.returncode == 0:
                    print(f"  [DEBUG] yt-dlp version: {v_proc.stdout.strip()}")
            except: pass
        
        # Tenta spoofing de cliente variado para evitar bloqueios
        if not extract_all:
            base_cmd += ["--extractor-args", "youtube:player_client=android,ios,web_creator,tv"]

        def executar(cmd_adicional):
            cmd = base_cmd + cmd_adicional
            if extract_all:
                cmd += ["--flat-playlist", "--print", "title", "--print", "url", url]
            else:
                cmd += ["-f", "best[ext=mp4]/best", "--get-url", url]
            
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=flags,
            )
            resultado_container["proc"] = proc
            stdout_bytes, stderr_bytes = proc.communicate()
            return stdout_bytes, stderr_bytes, proc.returncode

        # Logica de cookies e fallback
        cmd_cookies = []
        caminho_cookies = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookies.txt")
        if os.path.exists(caminho_cookies):
            cmd_cookies = ["--cookies", caminho_cookies]
        elif not IS_CI:
            # So tenta cookies do navegador localmente se nao houver cookies.txt
            cmd_cookies = ["--cookies-from-browser", "chrome"]

        # Primeira tentativa (com cookies se houver)
        stdout_b, stderr_b, code = executar(cmd_cookies)
        stderr_text = stderr_b.decode("utf-8", errors="replace") if stderr_b else ""

        # Fallback se falhar por DPAPI ou cookies problematicos
        if "DPAPI" in stderr_text or "cookie" in stderr_text.lower():
            if "--cookies-from-browser" in cmd_cookies:
                # Tenta sem cookies de navegador
                stdout_b, stderr_b, code = executar([])
                stderr_text = stderr_b.decode("utf-8", errors="replace") if stderr_b else ""

        def to_str(b):
            if isinstance(b, bytes):
                return b.decode("utf-8", errors="replace")
            return str(b) if b is not None else ""

        resultado_container["stdout"] = to_str(stdout_b)
        resultado_container["stderr"] = stderr_text
        resultado_container["returncode"] = code
    except FileNotFoundError:
        resultado_container["erro_fatal"] = True
    except Exception as e:
        resultado_container["stderr"] = (resultado_container.get("stderr", "") or "") + f"\nErro: {str(e)}"


def obter_urls_live(canal_info):
    """Extrai uma ou mais URLs de stream do YouTube. Retorna lista de (nome, url, erro)."""
    nome_original = canal_info.get("nome", "Desconhecido")
    url_yt = canal_info.get("url", "")
    is_multi = canal_info.get("multi", False)
    
    container = {"proc": None, "stdout": "", "stderr": "", "returncode": -1, "erro_fatal": False}
    t = threading.Thread(target=_rodar_ytdlp, args=(url_yt, container, is_multi), daemon=True)
    t.start()
    t.join(timeout=TIMEOUT_CANAL)

    if t.is_alive():
        proc = container.get("proc")
        if proc and hasattr(proc, "kill"):
            try: proc.kill()
            except Exception: pass
        return [(nome_original, None, f"Timeout de {TIMEOUT_CANAL}s")]

    if container.get("erro_fatal"):
        return [(nome_original, None, "yt-dlp nao encontrado")]

    stdout = (container.get("stdout") or "").strip()
    stderr = (container.get("stderr") or "").strip()

    if is_multi:
        resul = []
        linhas = stdout.splitlines()
        for i in range(0, len(linhas) - 1, 2):
            titulo = linhas[i].strip()
            url_video = linhas[i+1].strip()
            # Filtragem para TV Justiça e outros multi-live
            # Queremos apenas lives ativas (que nao contenham tempo decorrido, apenas 'AO VIVO' ou similar)
            # No entanto, --flat-playlist costuma listar tudo.
            if any(k in titulo.lower() for k in ["ao vivo", "live", "justiça", "rádio"]):
                # Filtra videos curtos ou passados que nao sao lives reais (heuristica simples)
                if any(x in titulo for x in ["0:", "1:"]): continue # Provavelmente video gravado Ja postado
                
                u_stream, err = obter_url_m3u8_simples(url_video)
                if u_stream:
                    exibicao = titulo.replace(" - Ao vivo", "").replace(" (AO VIVO)", "").replace(" ao vivo", "")
                    resul.append((f"{nome_original}: {exibicao}", u_stream, None))
        
        if not resul:
             # Se nao achou nada no modo multi, tenta a URL base como live simples
             u_stream, err = obter_url_m3u8_simples(url_yt)
             if u_stream:
                 return [(nome_original, u_stream, None)]
             return [(nome_original, None, "Offline")]
        return resul

    # Caso simples
    for linha in stdout.splitlines():
        linha = linha.strip()
        if linha.startswith("http"):
            return [(nome_original, linha, None)]

    # Erro no caso simples
    erro_msg = "Nao encontrado"
    if "unavailable" in stderr.lower(): erro_msg = "Indisponivel"
    elif "bot" in stderr.lower() or "sign in" in stderr.lower(): erro_msg = "Bloqueio Bot (Verifique Cookies)"
    elif "live" in stderr.lower() and "not" in stderr.lower(): erro_msg = "Offline"
    elif "begin in" in stderr.lower(): erro_msg = "Programada"
    elif stderr: erro_msg = stderr.splitlines()[0][:60]
    return [(nome_original, None, erro_msg)]


def obter_url_m3u8_simples(video_url):
    """Auxiliar para pegar URL de um vídeo específico rapidamente."""
    container = {"proc": None, "stdout": "", "stderr": "", "returncode": -1, "erro_fatal": False}
    _rodar_ytdlp(video_url, container, extract_all=False)
    stdout = (container.get("stdout") or "").strip()
    for linha in stdout.splitlines():
        if linha.strip().startswith("http"):
            return linha.strip(), None
    return None, "Erro"


def gerar_playlist():
    """Gera a playlist final mesclando a base com os links do YouTube."""
    linhas = []
    
    # 1. Tenta ler o arquivo base
    caminho_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), ARQUIVO_BASE)
    if os.path.exists(caminho_base):
        print(f"  [BASE] Lendo {ARQUIVO_BASE}...")
        try:
            with open(caminho_base, "r", encoding="utf-8") as f:
                linhas = f.readlines()
                if linhas and not linhas[-1].endswith("\n"):
                    linhas[-1] += "\n"
        except Exception as e:
            print(f"  [ERRO] Falha ao ler base: {e}")
            linhas = ["#EXTM3U\n"]
    else:
        print(f"  [AVISO] Arquivo {ARQUIVO_BASE} nao encontrado. Criando apenas com YouTube.")
        linhas = ["#EXTM3U\n"]

    # 2. Adiciona canais do YouTube
    print("  [YOUTUBE] Atualizando links...")
    atualizados = 0
    for canal in CANAIS_YOUTUBE:
        logo = canal.get("logo", "")
        grupo = canal.get("grupo", "YouTube")

        resultados = obter_urls_live(canal)

        for nome_exibicao, url_stream, erro in resultados:
            print(f"    --> {nome_exibicao} ... ", end="", flush=True)
            if url_stream:
                extinf = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{grupo}",{nome_exibicao}\n'
                linhas.append(extinf)
                linhas.append(url_stream + "\n")
                print("[OK]")
                atualizados += 1
            elif erro in ["Offline", "Programada", "Nenhuma live ativa detectada"]:
                print(f"[{erro}]")
            else:
                print(f"[FALHOU: {erro}]")

    # 3. Salva o resultado
    caminho_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), ARQUIVO_SAIDA)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.writelines(linhas)

    print(f"\n  Arquivo gerado: {ARQUIVO_SAIDA}")
    print(f"  YouTube: {atualizados}/{len(CANAIS_YOUTUBE)} canais OK")
    if IS_CI:
        print(f"  [CI] Processo concluido. Pronto para commit.")


def main():
    rodada = 1
    
    while True:
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[Rodada #{rodada}] {agora}")
        print("-" * 55)

        gerar_playlist()

        if IS_CI:
            break

        print(f"\n  Proxima atualizacao em {INTERVALO_SEGUNDOS//60} minutos.")
        try:
            time.sleep(INTERVALO_SEGUNDOS)
        except KeyboardInterrupt:
            break
        rodada += 1


if __name__ == "__main__":
    main()
