#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador automatico de M3U8 para canais do YouTube ao vivo.
Atualiza o arquivo playlist.m3u com links frescos automaticamente.
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
# CONFIGURACAO - Edite aqui seus canais
# ============================================================
CANAIS = [
    {
        "nome": "TV Cancao Nova",
        "url": "https://www.youtube.com/watch?v=zSN0ospdIaE",
        "logo": "",
        "grupo": "Religioso",
    },
    {
        "nome": "TV Jornal Caruaru",
        "url": "https://www.youtube.com/watch?v=IAMfZy0-eZs",
        "logo": "",
        "grupo": "Noticias",
    },
    {
        "nome": "Canal Rural",
        "url": "https://www.youtube.com/watch?v=hmUCjG_P0xg",
        "logo": "",
        "grupo": "Variedades",
    },
    {
        "nome": "Rede Vida Mais",
        "url": "https://www.youtube.com/watch?v=YYJSUSHAiHw",
        "logo": "",
        "grupo": "Religioso",
    },
    {
        "nome": "TV Pernambuco",
        "url": "https://www.youtube.com/watch?v=qgVz7FESmNE",
        "logo": "",
        "grupo": "Noticias",
    },
]

ARQUIVO_SAIDA = "playlist.m3u"
INTERVALO_SEGUNDOS = 3600   # Atualiza a cada 1 hora
TIMEOUT_CANAL = 30          # Segundos maximos por canal
# ============================================================


def _rodar_ytdlp(url, resultado_container):
    """Executa yt-dlp em thread separada e guarda a saida."""
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
    """Usa yt-dlp com kill forcado por timeout para extrair URL de stream."""
    container = {"proc": None, "stdout": "", "stderr": "", "returncode": -1, "erro_fatal": False}
    t = threading.Thread(target=_rodar_ytdlp, args=(youtube_url, container), daemon=True)
    t.start()
    t.join(timeout=TIMEOUT_CANAL)

    if t.is_alive():
        # Kill forcado do processo
        proc = container.get("proc")
        if proc:
            try:
                proc.kill()
            except Exception:
                pass
        print("\n  [TIMEOUT " + str(TIMEOUT_CANAL) + "s] Video pode nao estar ao vivo.")
        return None

    if container["erro_fatal"]:
        print("\n[ERRO FATAL] yt-dlp nao encontrado. Instale: pip install yt-dlp")
        sys.exit(1)

    for linha in container["stdout"].strip().splitlines():
        linha = linha.strip()
        if linha.startswith("http"):
            return linha

    stderr = container["stderr"].strip()[:300]
    print("\n  [AVISO] Nenhuma URL encontrada.")
    if stderr:
        print("  Detalhe: " + stderr[:200])
    return None


def gerar_playlist(canais):
    """Gera o arquivo .m3u com os links atualizados."""
    linhas = ["#EXTM3U\n"]
    atualizados = 0

    for canal in canais:
        nome = canal["nome"]
        url_yt = canal["url"]
        logo = canal.get("logo", "")
        grupo = canal.get("grupo", "YouTube")

        print("  --> " + nome + " ... ", end="", flush=True)
        url_stream = obter_url_m3u8(url_yt)

        if url_stream:
            extinf = (
                '#EXTINF:-1 tvg-logo="' + logo +
                '" group-title="' + grupo + '",' + nome + "\n"
            )
            linhas.append(extinf)
            linhas.append(url_stream + "\n")
            print("[OK]")
            atualizados = atualizados + 1
        else:
            print("[FALHOU]")

    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), ARQUIVO_SAIDA)
    with open(caminho, "w", encoding="utf-8") as f:
        f.writelines(linhas)

    print()
    print("  Arquivo: " + caminho)
    print("  Resultado: " + str(atualizados) + "/" + str(len(canais)) + " canais OK")


def main():
    # Detect if running in CI (GitHub Actions)
    is_ci = os.environ.get("GITHUB_ACTIONS") == "true"

    print("=" * 55)
    print("  YouTube -> M3U8  |  Atualizacao automatica")
    print("=" * 55)

    rodada = 1
    while True:
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n[Rodada #" + str(rodada) + "]  " + agora)
        print("-" * 55)

        gerar_playlist(CANAIS)

        if is_ci:
            print("\n  [CI Detectado] Playlist atualizada. Encerrando...")
            break

        proxima = datetime.fromtimestamp(time.time() + INTERVALO_SEGUNDOS)
        print("\n  Proxima atualizacao: " + proxima.strftime("%H:%M:%S"))
        print("  [Ctrl+C para encerrar]\n")

        try:
            time.sleep(INTERVALO_SEGUNDOS)
        except KeyboardInterrupt:
            print("\n  Encerrado. Ate logo!")
            break

        rodada += 1


if __name__ == "__main__":
    main()
