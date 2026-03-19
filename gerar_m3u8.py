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
        "url": "https://www.youtube.com/watch?v=IAMfZy0-eZs",
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
        "nome": "Rede Vida Mais",
        "url": "https://www.youtube.com/watch?v=YYJSUSHAiHw",
        "logo": "https://redevida.com.br/wp-content/uploads/2024/07/logo-redevida.png.webp",
        "grupo": "Catolico",
    },
    {
        "nome": "TV Pernambuco",
        "url": "https://www.youtube.com/watch?v=qgVz7FESmNE",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/thumb/f/f2/Logotipo_da_TV_Pernambuco.jpg/330px-Logotipo_da_TV_Pernambuco.jpg",
        "grupo": "PE",
    },
    {
        "nome": "PREF TV CARUARU",
        "url": "https://www.youtube.com/@preftvof/live",
        "logo": "https://yt3.googleusercontent.com/fREpAt4-Q4eR6W_lI1NlS-c7qQ8G-1X8-oZ-iE7vX3-F-P-E-S-T-A-D-O-R-A-S=s160-c-k-c0x00ffffff-no-rj",
        "grupo": "PE",
    },
]

ARQUIVO_BASE = "playlist_base.m3u"
ARQUIVO_SAIDA = "playlist.m3u"
INTERVALO_SEGUNDOS = 3600   # Atualiza a cada 1 hora
TIMEOUT_CANAL = 30          # Segundos maximos por canal
# ============================================================


def _rodar_ytdlp(url, resultado_container):
    """Executa yt-dlp em thread separada."""
    try:
        flags = 0
        if sys.platform == "win32":
            flags = subprocess.CREATE_NO_WINDOW
        proc = subprocess.Popen(
            [
                "yt-dlp",
                "--no-update",
                "--no-playlist",
                "--socket-timeout", "10",
                "--retries", "1",
                "--fragment-retries", "1",
                "-f", "best[ext=mp4]/best",
                "--get-url",
                url,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=flags,
        )
        resultado_container["proc"] = proc
        stdout, stderr = proc.communicate()
        resultado_container["stdout"] = stdout.decode("utf-8", errors="replace")
        resultado_container["stderr"] = stderr.decode("utf-8", errors="replace")
        resultado_container["returncode"] = proc.returncode
    except FileNotFoundError:
        resultado_container["erro_fatal"] = True


def obter_url_m3u8(youtube_url):
    """Extrai URL de stream com timeout."""
    container = {"proc": None, "stdout": "", "stderr": "", "returncode": -1, "erro_fatal": False}
    t = threading.Thread(target=_rodar_ytdlp, args=(youtube_url, container), daemon=True)
    t.start()
    t.join(timeout=TIMEOUT_CANAL)

    if t.is_alive():
        proc = container.get("proc")
        if proc:
            try: proc.kill()
            except Exception: pass
        return None

    if container["erro_fatal"]:
        return None

    for linha in container["stdout"].strip().splitlines():
        linha = linha.strip()
        if linha.startswith("http"):
            return linha
    return None


def gerar_playlist():
    """Gera a playlist final mesclando a base com os links do YouTube."""
    linhas = []
    
    # 1. Tenta ler o arquivo base
    caminho_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), ARQUIVO_BASE)
    if os.path.exists(caminho_base):
        print(f"  [BASE] Lendo {ARQUIVO_BASE}...")
        with open(caminho_base, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            if not linhas[-1].endswith("\n"):
                linhas[-1] += "\n"
    else:
        print(f"  [AVISO] Arquivo {ARQUIVO_BASE} nao encontrado. Criando apenas com YouTube.")
        linhas = ["#EXTM3U\n"]

    # 2. Adiciona canais do YouTube
    print("  [YOUTUBE] Atualizando links...")
    atualizados = 0
    for canal in CANAIS_YOUTUBE:
        nome = canal["nome"]
        url_yt = canal["url"]
        logo = canal.get("logo", "")
        grupo = canal.get("grupo", "YouTube")

        print(f"    --> {nome} ... ", end="", flush=True)
        url_stream = obter_url_m3u8(url_yt)

        if url_stream:
            extinf = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{grupo}",{nome}\n'
            linhas.append(extinf)
            linhas.append(url_stream + "\n")
            print("[OK]")
            atualizados += 1
        else:
            print("[FALHOU]")

    # 3. Salva o resultado
    caminho_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), ARQUIVO_SAIDA)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.writelines(linhas)

    print(f"\n  Arquivo gerado: {ARQUIVO_SAIDA}")
    print(f"  YouTube: {atualizados}/{len(CANAIS_YOUTUBE)} canais OK")


def main():
    is_ci = os.environ.get("GITHUB_ACTIONS") == "true"
    rodada = 1
    
    while True:
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[Rodada #{rodada}] {agora}")
        print("-" * 55)

        gerar_playlist()

        if is_ci:
            break

        print(f"\n  Proxima atualizacao em {INTERVALO_SEGUNDOS//60} minutos.")
        try:
            time.sleep(INTERVALO_SEGUNDOS)
        except KeyboardInterrupt:
            break
        rodada += 1


if __name__ == "__main__":
    main()
