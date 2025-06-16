import requests
import threading
from queue import Queue
import time
import os
from tqdm import tqdm
import random
import re

# Kiểm tra package requests[socks]
try:
    from requests.packages.urllib3.contrib import socks
except ImportError:
    print("Cần cài đặt requests[socks]: Chạy lệnh 'pip install requests[socks]'")
    exit(1)

def is_valid_proxy(proxy):
    # Kiểm tra định dạng IP:PORT
    pattern = r'^(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}$'
    return bool(re.match(pattern, proxy))

def fetch_proxies_from_api(api_urls):
    proxies = []
    proxies_set = set()  # Dùng để kiểm tra trùng lặp
    total_raw_proxies = 0
    for url in api_urls:
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                lines = [line.strip() for line in response.text.splitlines() if line.strip()]
                new_proxies = []
                for line in lines:
                    if is_valid_proxy(line):
                        proxy = f"socks5://{line}"  # Mặc định SOCKS5 cho API GitHub
                        new_proxies.append(proxy)
                    elif line.startswith("http://") or line.startswith("socks"):
                        new_proxies.append(line)
                total_raw_proxies += len(new_proxies)
                count_before = len(proxies_set)
                proxies.extend(new_proxies)
                proxies_set.update(new_proxies)
                count_after = len(proxies_set)
                print(f"✅ Đã lấy {len(new_proxies)} proxy từ {url} ({count_after - count_before} mới, tổng duy nhất: {count_after})")
            else:
                print(f"❌ Lỗi khi lấy proxy từ {url}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ Lỗi khi lấy proxy từ {url}: {str(e)}")
    print(f"📊 Tổng proxy thô: {total_raw_proxies}, proxy hợp lệ: {len(proxies)}, proxy duy nhất: {len(proxies_set)}")
    return proxies

def check_proxy(proxy, timeout, live_proxies, dead_proxies, total_checked, total_proxies, progress_bar):
    test_urls = [
        "http://httpbin.org/ip",
        "https://api.ipify.org?format=json",
        "http://ip-api.com/json",
        "https://ifconfig.me/ip"
    ]
    proxy_type = "http" if "http://" in proxy else "socks"

    # Thử 3 lần để đảm bảo chính xác
    for _ in range(3):
        try:
            proxy_dict = {
                "http": proxy,
                "https": proxy
            }
            url = random.choice(test_urls)
            effective_timeout = random.uniform(0.1, timeout)
            response = requests.get(url, proxies=proxy_dict, timeout=effective_timeout)
            if response.status_code == 200:
                with threading.Lock():
                    live_proxies.append(proxy)
                    progress_bar.set_postfix(live=len(live_proxies), dead=len(dead_proxies))
                return
        except:
            continue

    with threading.Lock():
        dead_proxies.append(proxy)
        progress_bar.set_postfix(live=len(live_proxies), dead=len(dead_proxies))

    with threading.Lock():
        total_checked[0] += 1
        progress_bar.update(1)

def worker(queue, timeout, live_proxies, dead_proxies, total_checked, total_proxies, progress_bar):
    while not queue.empty():
        proxy = queue.get()
        check_proxy(proxy, timeout, live_proxies, dead_proxies, total_checked, total_proxies, progress_bar)
        queue.task_done()

def main():
    print("🔥 Tool Quét Proxy VIP PRO - Đẹp, Chất, Xịn 🔥")
    source = input("Quét proxy từ file hay link API? (F = file, A = API): ").strip().upper()
    proxies = []

    if source == "F":
        proxy_file = input("Nhập file chứa proxy (ví dụ: proxy.txt): ") or "proxy.txt"
        if not os.path.exists(proxy_file):
            print(f"❌ File {proxy_file} không tồn tại!")
            return
        with open(proxy_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            proxies = []
            proxies_set = set()  # Dùng để kiểm tra trùng lặp
            for line in lines:
                if is_valid_proxy(line):
                    proxy = f"socks5://{line}"  # Mặc định SOCKS5 cho file
                    proxies.append(proxy)
                elif line.startswith("http://") or line.startswith("socks"):
                    proxies.append(line)
                proxies_set.add(line)
            print(f"📊 Tổng proxy thô: {len(lines)}, proxy hợp lệ: {len(proxies)}, proxy duy nhất: {len(proxies_set)}")
    elif source == "A":
        api_file = input("Nhập file chứa link API proxy (ví dụ: api.txt): ") or "api.txt"
        if not os.path.exists(api_file):
            print(f"❌ File {api_file} không tồn tại!")
            return
        with open(api_file, "r", encoding="utf-8") as f:
            api_urls = [line.strip() for line in f if line.strip()]
        if not api_urls:
            print("❌ File API rỗng!")
            return
        proxies = fetch_proxies_from_api(api_urls)
    else:
        print("❌ Lựa chọn không hợp lệ! Chọn F hoặc A.")
        return

    total_proxies = len(proxies)
    if total_proxies == 0:
        print("❌ Không có proxy nào để quét!")
        return

    print(f"✅ Đã đọc {total_proxies} proxy để quét từ {source.lower()}")

    timeout = float(input("Nhập timeout của proxy (ví dụ: 1, 2, 4, 5): ") or 5)

    live_proxies = []
    dead_proxies = []
    total_checked = [0]
    queue = Queue()

    for proxy in proxies:
        queue.put(proxy)

    progress_bar = tqdm(total=total_proxies, desc="🔥 Quét Proxy 🔥", unit="proxy",
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {postfix}",
                        dynamic_ncols=True)

    num_threads = min(100, total_proxies)
    threads = []

    start_time = time.time()
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(queue, timeout, live_proxies, dead_proxies, total_checked, total_proxies, progress_bar))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    progress_bar.close()
    print(f"\n🎉 Hoàn tất! Thời gian: {time.time() - start_time:.2f} giây")
    print(f"✅ Proxy sống: {len(live_proxies)}/{total_proxies}")
    print(f"❌ Proxy chết: {len(dead_proxies)}/{total_proxies}")

    save = input("Lưu proxy sống ra file riêng? (Y/N): ").strip().upper()
    if save == "Y":
        output_file = "Proxysong.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            for proxy in live_proxies:
                f.write(proxy + "\n")
        print(f"💾 Đã lưu file {output_file}")

if __name__ == "__main__":
    main()