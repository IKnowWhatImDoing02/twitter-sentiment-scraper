import queue
import threading
import requests

proxy_queue = queue.Queue()
valid_https_proxies = []

# Load proxies
with open('proxy_list.txt', 'r') as f:
    for line in f:
        proxy = line.strip()
        if proxy:
            proxy_queue.put(proxy)

def check_https_proxy():
    while not proxy_queue.empty():
        proxy = proxy_queue.get()
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",  # Always use http scheme here
        }
        try:
            response = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=5)
            if response.status_code == 200:
                print(f"[VALID] {proxy}")
                valid_https_proxies.append(proxy)
        except requests.exceptions.RequestException:
            pass  # silently ignore bad proxies

# Launch threads
threads = []
for _ in range(10):
    t = threading.Thread(target=check_https_proxy)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# Save valid proxies
with open("valid_https_proxies.txt", "w") as f:
    for proxy in valid_https_proxies:
        f.write(proxy + "\n")

print(f"✅ Done. {len(valid_https_proxies)} HTTPS proxies saved to valid_https_proxies.txt")
