from allproxy import Get
import random
import requests

proxy_list = Get.get_proxies()

proxy = random.choice(proxy_list)

print(proxy)

response = requests.get("https://ipinfo.io/json", proxies={'http': proxy}, timeout=10)
print(response.text)