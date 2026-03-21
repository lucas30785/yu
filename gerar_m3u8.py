#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador automático de M3U8 para canais do YouTube ao vivo.
Mescla uma base estática (EPG + canais fixos) com links dinâmicos do YouTube.
"""
import io
import subprocess
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
    {
        "nome": "Rede Vida Educacao",
        "url": "https://www.youtube.com/@redevidaeducacao/live",
        "logo": "https://redevida.com.br/wp-content/uploads/2024/07/logo-redevida.png.webp",
        "grupo": "Educatido",
    },
    {
        "nome": "TV Pernambuco",
        "url": "https://www.youtube.com/@tvpernambuco/live",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/thumb/f/f2/Logotipo_da_TV_Pernambuco.jpg/330px-Logotipo_da_TV_Pernambuco.jpg",
        "grupo": "PE",
    },
    {
        "nome": "TV Justica",
        "url": "https://www.youtube.com/@RadioeTVJustica/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Logotipo_da_TV_Justi%C3%A7a.png/300px-Logotipo_da_TV_Justi%C3%A7a.png",
        "grupo": "Justiça",
        "multi": True,
    },
    {
        "nome": "PREF TV CARUARU",
        "url": "https://www.youtube.com/@preftvof/live",
        "logo": "https://yt3.googleusercontent.com/fREpAt4-Q4eR6W_lI1NlS-c7qQ8G-1X8-oZ-iE7vX3-F-P-E-S-T-A-D-O-R-A-S=s160-c-k-c0x00ffffff-no-rj",
        "grupo": "PE",
    },
    {
        "nome": "RedeTV!",
        "url": "https://www.youtube.com/@redetv/live",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/RedeTV%21_logo.svg/330px-RedeTV%21_logo.svg.png",
        "grupo": "ABERTO",
    },
    {
        "nome": "BAND",
        "url": "https://www.youtube.com/@bandjornalismo/live",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Band_logo.svg/330px-Band_logo.svg.png",
        "grupo": "ABERTO",
    },
    {
        "nome": "SBT",
        "url": "https://www.youtube.com/@SBTonline/live",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/SBT_logo.svg/330px-SBT_logo.svg.png",
        "grupo": "ABERTO",
    },
    {
        "nome": "CNN Brasil Money",
        "url": "https://www.youtube.com/@cnnbrmoney/live",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/CNN_Brasil.svg/330px-CNN_Brasil.svg.png",
        "grupo": "Financeiro",
    },
    {
        "nome": "TV Aparecida",
        "url": "https://www.youtube.com/@tvaparecida/live",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/thumb/1/1e/Logotipo_da_TV_Aparecida.png/330px-Logotipo_da_TV_Aparecida.png",
        "grupo": "Catolico",
    },
    {
        "nome": "Rede Vida",
        "url": "https://www.youtube.com/@tvredevida.aovivo/live",
        "logo": "https://redevida.com.br/wp-content/uploads/2024/07/logo-redevida.png.webp",
        "grupo": "Catolico",
    },
    {
        "nome": "TV Pai Eterno",
        "url": "https://www.youtube.com/@paieterno/live",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/thumb/7/7c/Logotipo_TV_Pai_Eterno.png/330px-Logotipo_TV_Pai_Eterno.png",
        "grupo": "Catolico",
    },
    {
        "nome": "TV Horizonte",
        "url": "https://www.youtube.com/@tvhorizonte.oficial/live",
        "logo": "https://tvhorizonte.com.br/wp-content/uploads/2024/12/logo-rede-catedral.png",
        "grupo": "Catolico",
    },
    {
        "nome": "Vatican News",
        "url": "https://www.youtube.com/@VaticanNewsPT/live",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Vatican_News.svg/330px-Vatican_News.svg.png",
        "grupo": "Catolico",
    },
    {
        "nome": "Canal Agroplus",
        "url": "https://www.youtube.com/@canalagroplus/live",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Canal_Rural.png/300px-Canal_Rural.png",
        "grupo": "Variedades",
    },
    {
        "nome": "TV Gazeta",
        "url": "https://www.youtube.com/@tvgazetaoficial/live",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/TV_Gazeta.svg/330px-TV_Gazeta.svg.png",
        "grupo": "ABERTO",
    },
]


ARQUIVO_BASE = "playlist_base.m3u"
ARQUIVO_SAIDA = "playlist.m3u"
TIMEOUT_CANAL = 40          # Tempo máximo por canal (segundos)
# ============================================================

def executar_ytdlp(url, extract_all=False):
    """Executa yt-dlp com timeout e tratamento de erros."""
    flags = 0
    if sys.platform == "win32":
        flags = subprocess.CREATE_NO_WINDOW
    
    cmd = [
        "yt-dlp",
        "--no-update",
        "--no-playlist",
        "--socket-timeout", "15",
        "--retries", "1",
        "--fragment-retries", "1",
        "--no-check-certificate",
        "--ignore-errors",
    ]
    
    # Spoofing para evitar bloqueios
    cmd += ["--extractor-args", "youtube:player_client=android,ios,web_creator,tv"]
    
    if extract_all:
        cmd += ["--flat-playlist", "--print", "title", "--print", "url", url]
    else:
        cmd += ["-f", "best[ext=mp4]/best", "--get-url", url]
    
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=TIMEOUT_CANAL,
            creationflags=flags,
            encoding="utf-8",
            errors="replace"
        )
        return proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", -1
    except Exception as e:
        return "", str(e), -1

def obter_urls_live(canal_info):
    """Retorna lista de (nome, url_stream, erro)."""
    nome_original = canal_info.get("nome", "Desconhecido")
    url_yt = canal_info.get("url", "")
    is_multi = canal_info.get("multi", False)
    
    stdout, stderr, code = executar_ytdlp(url_yt, extract_all=is_multi)

    if is_multi:
        resul = []
        linhas = stdout.splitlines()
        for i in range(0, len(linhas) - 1, 2):
            titulo = linhas[i].strip()
            url_video = linhas[i+1].strip()
            if any(k in titulo.lower() for k in ["ao vivo", "live", "justiça", "rádio"]):
                if any(x in titulo for x in ["0:", "1:"]): continue 
                
                u_stream_out, _, _ = executar_ytdlp(url_video, extract_all=False)
                u_stream = u_stream_out.strip()
                if u_stream.startswith("http"):
                    exibicao = titulo.replace(" - Ao vivo", "").replace(" (AO VIVO)", "").replace(" ao vivo", "")
                    resul.append((f"{nome_original}: {exibicao}", u_stream, None))
        
        if not resul:
             u_stream_out, _, _ = executar_ytdlp(url_yt, extract_all=False)
             u_stream = u_stream_out.strip()
             if u_stream.startswith("http"):
                 return [(nome_original, u_stream, None)]
             return [(nome_original, None, "Offline")]
        return resul

    for linha in stdout.splitlines():
        if linha.strip().startswith("http"):
            return [(nome_original, linha.strip(), None)]

    erro_msg = "Nao encontrado"
    if "unavailable" in stderr.lower(): erro_msg = "Indisponivel"
    elif "bot" in stderr.lower() or "sign in" in stderr.lower(): erro_msg = "Bloqueio"
    elif "live" in stderr.lower() and "not" in stderr.lower(): erro_msg = "Offline"
    return [(nome_original, None, erro_msg)]

def gerar_playlist():
    """Gera o arquivo M3U8 final."""
    linhas = []
    
    # 1. Base Estática
    dir_p = os.path.dirname(os.path.abspath(__file__))
    c_base = os.path.join(dir_p, ARQUIVO_BASE)
    if os.path.exists(c_base):
        print(f"  [BASE] Lendo {ARQUIVO_BASE}...")
        with open(c_base, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            if linhas and not linhas[-1].endswith("\n"):
                linhas[-1] += "\n"
    else:
        print(f"  [AVISO] {ARQUIVO_BASE} nao encontrado.")
        linhas = ["#EXTM3U\n"]

    # 2. YouTube Dinâmico
    print("  [YOUTUBE] Atualizando links...")
    for canal in CANAIS_YOUTUBE:
        logo = canal.get("logo", "")
        grupo = canal.get("grupo", "YouTube")
        resultados = obter_urls_live(canal)

        for nome_exibicao, url_stream, erro in resultados:
            print(f"    --> {nome_exibicao} ... ", end="", flush=True)
            if url_stream:
                linhas.append(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{grupo}",{nome_exibicao}\n')
                linhas.append(f"{url_stream}\n")
                print("[OK]")
            else:
                # Fallback: Mantém o canal com link original do YouTube se a resolução falhar
                url_original = canal.get("url", "")
                linhas.append(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{grupo}",{nome_exibicao} [OFFLINE]\n')
                linhas.append(f"{url_original}\n")
                print(f"[FALHOU: {erro}] - Mantido link original")


    # 3. Salvar
    c_saida = os.path.join(dir_p, ARQUIVO_SAIDA)
    with open(c_saida, "w", encoding="utf-8") as f:
        f.writelines(linhas)
    print(f"\n  [SUCESSO] Playlist gerada: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    gerar_playlist()
