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
import urllib.request
import urllib.error
import json
import random
import re
from datetime import datetime

WORKING_PROXY = None
PROXY_LIST = []

def load_proxies():
    global PROXY_LIST
    if not PROXY_LIST:
        print("\n  [PROXY] Coletando lista de proxies Brasileiros...")
        sources = [
            # Oficiais/Específicos para BR
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=BR",
            "https://www.proxy-list.download/api/v1/get?type=http&country=BR",
            "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&country=BR&protocols=http"
        ]
        
        collected = []
        import urllib.request, json
        for url in sources:
            try:
                print(f"    --> Lendo: {url.split('/')[2]}... ", end="", flush=True)
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=12) as response:
                    res_raw = response.read().decode('utf-8')
                    if "geonode" in url:
                        data = json.loads(res_raw)
                        found = [f"{p['ip']}:{p['port']}" for p in data.get('data', [])]
                    else:
                        found = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', res_raw)
                    collected.extend(found)
                    print(f"[{len(found)} ok]")
            except Exception:
                print(f"[falhou]")
        
        # Fallback global apenas se BR estiver vazio
        if not collected:
            try:
                print(f"    --> Lendo fallback global... ", end="", flush=True)
                url_fb = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
                req = urllib.request.Request(url_fb, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    found = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', response.read().decode('utf-8'))
                    collected.extend(found[:50]) # Limita fallback
                    print(f"[{len(found)} ok]")
            except Exception: print("[falhou]")

        PROXY_LIST = list(set(collected))
        import random
        random.shuffle(PROXY_LIST)
        print(f"  [PROXY] Total de {len(PROXY_LIST)} proxies carregados.")
        if not PROXY_LIST: PROXY_LIST = ["ERRO"]

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

IS_CI = os.environ.get("GITHUB_ACTIONS") == "true"
USE_PROXIES_IN_CI = os.environ.get("USE_PROXIES_IN_CI", "false").lower() == "true"
MAX_PROXY_TESTS = 2 if IS_CI else 15

def check_requirements():
    print(f"  [SISTEMA] Python: {sys.version.split()[0]} no {sys.platform}")
    try:
        ver = subprocess.check_output(["yt-dlp", "--version"], text=True).strip()
        print(f"  [SISTEMA] yt-dlp versão: {ver}")
    except Exception as e:
        print(f"  [ERRO] yt-dlp não encontrado ou falhou: {e}")

check_requirements()

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
    {
        "nome": "XSPORT",
        "url": "https://www.youtube.com/@xsports.brasil/streams",
        "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k6V10M-C6qI29L-a6-Q4E-J9k08J73NnQO5yT0d5o=s176-c-k-c0x00ffffff-no-rj",
        "grupo": "Esportes",
        "multi": True,
    },
    {
        "nome": "SportyNet",
        "url": "https://www.youtube.com/@SportyNetBrasil/streams",
        "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k6-Oa3eJ3S7X-J3u1Y0_Z5F8h_z0e5c9o9i3z_3X2lXz0=s176-c-k-c0x00ffffff-no-rj",
        "grupo": "Esportes",
        "multi": True,
    },
    {
        "nome": "N Sports",
        "url": "https://www.youtube.com/@NSports/streams",
        "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k6_6m2x7O-9k7U8H9g2_i8y6p3u2r5_0n3V8V5T9J3_3Y=s176-c-k-c0x00ffffff-no-rj",
        "grupo": "Esportes",
        "multi": True,
    },
    {
        "nome": "CazéTV",
        "url": "https://www.youtube.com/channel/UCZiYbVptd3PVPf4f6eR6UaQ/streams",
        "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k6_0i9H5B9L7E8s9N2y3b7C8A4d9T0u7_2e8a7N6A5=s176-c-k-c0x00ffffff-no-rj",
        "grupo": "Esportes",
        "multi": True,
    },
    {
        "nome": "Canal GOAT",
        "url": "https://www.youtube.com/@maiscanalgoatbr/streams",
        "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k4_6X2D8O3R0Q7V5H9L2_U0c9P3A8_8h9e5E7A3_1G=s176-c-k-c0x00ffffff-no-rj",
        "grupo": "Esportes",
        "multi": True,
    },
]


ARQUIVO_BASE = "playlist_base.m3u"
ARQUIVO_SAIDA = "playlist.m3u"
ARQUIVO_RELATORIO_IA = "relatorio_ia.md"
TIMEOUT_CANAL = 40          # Tempo máximo por canal (segundos)
# ============================================================

AI_API_URL = os.environ.get("AI_API_URL", "https://api.openai.com/v1/chat/completions")
AI_API_KEY = os.environ.get("AI_API_KEY", "").strip()
AI_MODEL = os.environ.get("AI_MODEL", "gpt-4o-mini").strip()
AI_ENABLED = os.environ.get("AI_ENABLED", "true").lower() not in {"0", "false", "nao", "não", "off"}

def executar_ytdlp(url, extract_all=False, proxy=None):
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
        "--match-filter", "is_live",
    ]
    
    # Spoofing para evitar bloqueios
    cmd += ["--extractor-args", "youtube:player_client=android,ios,web_creator,tv"]
    
    if proxy:
        cmd += ["--proxy", f"http://{proxy}"]
    
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

def obter_urls_live_core(canal_info, proxy=None):
    """Retorna lista de (nome, url_stream, erro)."""
    nome_original = canal_info.get("nome", "Desconhecido")
    url_yt = canal_info.get("url", "")
    is_multi = canal_info.get("multi", False)
    
    stdout, stderr, code = executar_ytdlp(url_yt, extract_all=is_multi, proxy=proxy)

    if is_multi:
        resul = []
        linhas = stdout.splitlines()
        for i in range(0, len(linhas) - 1, 2):
            titulo = linhas[i].strip()
            url_video = linhas[i+1].strip()
            if any(k in titulo.lower() for k in ["ao vivo", "live", "justiça", "rádio"]):
                if any(x in titulo for x in ["0:", "1:"]): continue 
                
                u_stream_out, _, _ = executar_ytdlp(url_video, extract_all=False, proxy=proxy)
                u_stream = u_stream_out.strip()
                if u_stream.startswith("http"):
                    exibicao = titulo.replace(" - Ao vivo", "").replace(" (AO VIVO)", "").replace(" ao vivo", "")
                    resul.append((f"{nome_original}: {exibicao}", u_stream, None))
        
        if not resul:
             u_stream_out, _, _ = executar_ytdlp(url_yt, extract_all=False, proxy=proxy)
             u_stream = u_stream_out.strip()
             if u_stream.startswith("http"):
                 return [(nome_original, u_stream, None)]
             return [(nome_original, None, "Offline")]
        return resul

    for linha in stdout.splitlines():
        if linha.strip().startswith("http"):
            return [(nome_original, linha.strip(), None)]

    stderr_lower = stderr.lower()
    erro_msg = "Nao encontrado"
    
    # Mapeamento refinado de erros
    if any(chave in stderr_lower for chave in ["country", "region", "geo", "available in your country", "not available in your country", "blocked in your country"]):
        erro_msg = "GeoBloqueio"
    elif any(chave in stderr_lower for chave in ["unavailable", "not available", "removed"]):
        erro_msg = "Indisponivel"
    elif any(chave in stderr_lower for chave in ["bot", "sign in", "confirm you are not a robot", "captcha"]):
        erro_msg = "Bloqueio"
    elif any(chave in stderr_lower for chave in ["live", "not live", "waiting", "upcoming"]):
        erro_msg = "Offline"
    elif "timeout" in stderr_lower:
        erro_msg = "Timeout"
        
    return [(nome_original, None, erro_msg)]

def obter_urls_live(canal_info):
    global WORKING_PROXY
    resultados = obter_urls_live_core(canal_info, proxy=WORKING_PROXY)
    
    # Em CI, evita dependência de proxies públicos por serem lentos e instáveis.
    if IS_CI and not USE_PROXIES_IN_CI:
        return resultados
    
    # Se falhou por bloqueio ou geolocalizacao, busca proxy BR
    if any(r[2] in ["Bloqueio", "Indisponivel", "Nao encontrado", "GeoBloqueio"] for r in resultados):
        load_proxies()
        tested = 0
        while PROXY_LIST and tested < MAX_PROXY_TESTS:
            cand_proxy = PROXY_LIST.pop(0)
            tested += 1
            if cand_proxy == "ERRO": 
                break
            
            print(f" [TESTANDO PROXY BR: {cand_proxy}] ", end="", flush=True)
            res_tentativa = obter_urls_live_core(canal_info, proxy=cand_proxy)
            
            if not any(r[2] in ["Bloqueio", "Indisponivel", "Nao encontrado", "GeoBloqueio"] for r in res_tentativa):
                WORKING_PROXY = cand_proxy
                print(f"[FUNCIONOU! Mantendo proxy BR para proximos canais] ", end="", flush=True)
                return res_tentativa
                
        return resultados
    return resultados


def gerar_relatorio_ia(registros, sucessos, bloqueios):
    if os.environ.get("AI_ENABLED") != "true":
        print("  [IA] Relatório IA desativado (AI_ENABLED != true).")
        return

    print("  [IA] Gerando relatório com IA...")
    api_key = os.environ.get("AI_API_KEY")
    api_url = os.environ.get("AI_API_URL", "https://api.openai.com/v1/chat/completions")
    model = os.environ.get("AI_MODEL", "gpt-3.5-turbo")

    if not api_key:
        print("  [IA] Erro: AI_API_KEY não configurada.")
        return

    # Preparar resumo para a IA
    resumo = f"Sucessos: {sucessos}\nBloqueios: {bloqueios}\nCanais:\n"
    for r in registros[:50]: # Limita para não estourar token
        resumo += f"- {r['nome']}: {r['status']} ({r['erro']})\n"

    prompt = f"Gere um relatório em markdown resumindo a execução do script IPTV. Foque nos sucessos ({sucessos}) e nos bloqueios ({bloqueios}). Liste canais offline de forma organizada.\n\nDados:\n{resumo}"

    try:
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        req = urllib.request.Request(api_url, data=json.dumps(data).encode('utf-8'), headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            relatorio = res_json['choices'][0]['message']['content']
            
            with open("relatorio_ia.md", "w", encoding="utf-8") as f:
                f.write(relatorio)
            print("  [IA] Relatório relatorio_ia.md gerado com sucesso.")
    except Exception as e:
        print(f"  [IA] Erro ao gerar relatório: {e}")

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
    sucessos = 0
    bloqueios = 0
    registros = []
    for canal in CANAIS_YOUTUBE:
        logo = canal.get("logo", "")
        grupo = canal.get("grupo", "YouTube")
        resultados = obter_urls_live(canal)

        for nome_exibicao, url_stream, erro in resultados:
            print(f"    --> {nome_exibicao} ... ", end="", flush=True)
            if url_stream:
                # Detectar se o link é IP-locked (contém o IP do proxy ou do runner)
                # GoogleVideo URLs geralmente têm /ip/X.X.X.X/
                ip_match = re.search(r'/ip/([^/]+)/', url_stream)
                suffix = ""
                if ip_match:
                    resolved_ip = ip_match.group(1)
                    # Se resolvemos com proxy, avisar que pode precisar de VPN
                    if WORKING_PROXY and resolved_ip in WORKING_PROXY:
                        suffix = " [PROXY BR]"
                    elif ":" in resolved_ip and not IS_CI: # IPv6 ou similar
                         suffix = " [IP Lock]"
                
                linhas.append(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{grupo}",{nome_exibicao}{suffix}\n')
                linhas.append(f"{url_stream}\n")
                sucessos += 1
                registros.append({
                    "nome": nome_exibicao,
                    "grupo": grupo,
                    "status": "ok",
                    "erro": None,
                })
                print(f"[OK]{suffix}")
            else:
                if erro == "Bloqueio":
                    bloqueios += 1
                registros.append({
                    "nome": nome_exibicao,
                    "grupo": grupo,
                    "status": "falha",
                    "erro": erro or "Desconhecido",
                })
                print(f"[FALHOU: {erro}] - Canal não adicionado à playlist")


    # 3. Salvar
    c_saida = os.path.join(dir_p, ARQUIVO_SAIDA)
    with open(c_saida, "w", encoding="utf-8") as f:
        f.writelines(linhas)
    print(f"\n  [SUCESSO] Playlist gerada: {ARQUIVO_SAIDA}")

    # Escrever keep-alive file para evitar que o GitHub pause a cron
    with open(os.path.join(dir_p, "last_update.txt"), "w", encoding="utf-8") as f:
        f.write(datetime.now().isoformat())

    falhas = len([r for r in registros if r["status"] == "falha"])
    print(f"  [RESUMO] Canais YouTube resolvidos: {sucessos}")
    print(f"  [RESUMO] Canais YouTube com falha: {falhas}")
    print(f"  [RESUMO] Bloqueios detectados: {bloqueios}")

    gerar_relatorio_ia(registros, sucessos, bloqueios)

    # Em CI, evita falha total do workflow por bloqueios do YouTube/proxies.
    # A playlist continua sendo gerada apenas com streams válidos.
    if sucessos == 0 and bloqueios > 0:
        print("\n  [AVISO] Todos os canais dinâmicos falharam e houve bloqueios do YouTube.")
        print("  [AVISO] A playlist foi gerada apenas com streams válidos, sem interromper o workflow.")

if __name__ == "__main__":
    gerar_playlist()
