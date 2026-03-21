import urllib.request
import random
import subprocess
import time
import re

url_yt = "https://www.youtube.com/watch?v=zSN0ospdIaE"
print("Baixando proxy list...")
req = urllib.request.Request("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt")
try:
    with urllib.request.urlopen(req, timeout=10) as response:
        proxies = [p.strip() for p in response.read().decode('utf-8').splitlines() if p.strip()]
        print(f"Baixados {len(proxies)} proxies.")
except Exception as e:
    print(f"Erro proxy: {e}")
    proxies = []

def test_ytdlp(proxy):
    cmd = [
        "yt-dlp",
        "--socket-timeout", "10",
        "--proxy", f"http://{proxy}",
        "-f", "best[ext=mp4]/best",
        "--get-url", url_yt
    ]
    try:
        t0 = time.time()
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        t1 = time.time()
        if p.returncode == 0 and "http" in p.stdout:
            print(f"SUCESSO proxy {proxy} em {t1-t0:.2f}s")
            return p.stdout.strip()
        else:
            print(f"FALHA proxy {proxy}: {p.stderr.strip()[:60]}")
    except Exception as e:
        print(f"TIMEOUT proxy {proxy}")
    return None

random.shuffle(proxies)
for p in proxies[:5]:
    url = test_ytdlp(p)
    if url:
        print("URL encontrada:", url[:50] + "...")
        break
