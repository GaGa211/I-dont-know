import requests
import concurrent.futures
import os, sys,time
import requests
from time import strftime
import pystyle
import os,sys
import pywifi
from requests import session
from colorama import Fore, Style
import requests, random, re
from random import randint
import requests,pystyle
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from datetime import date
from datetime import datetime
from time import sleep
time=datetime.now().strftime("%H:%M:%S")
from pystyle import *
luc = "\033[1;32m"
trang = "\033[1;37m"
do = "\033[1;31m"
vang = "\033[0;93m"
hong = "\033[1;35m"
xduong = "\033[1;34m"
lam = "\033[1;36m"
red='\u001b[31;1m'
yellow='\u001b[33;1m'
green='\u001b[32;1m'
blue='\u001b[34;1m'
tim='\033[1;35m'
xanhlam='\033[1;36m'
xam='\033[1;30m'
black='\033[1;19m'
data_machine = []
today = date.today()
now = datetime.now()
thu = now.strftime("%A")
ngay_hom_nay = now.strftime("%d")
thang_nay = now.strftime("%m")
nam_ = now.strftime("%Y")
def check_internet_connection():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Kiểm tra kết nối internet
if check_internet_connection():
    print(f"{luc}Vui Lòng Chờ!!!")
    sleep(0.1)
else:
    print(f"{do}Vui Lòng Kiểm Tra Kết NốI!!!")
    sys.exit()
def get_location_by_ip():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()

        city = data.get("city")
        region = data.get("region")
        country = data.get("country")
        loc = data.get("loc").split(",")
        latitude, longitude = loc if len(loc) == 2 else (None, None)

        return city, region, country, latitude, longitude
    except Exception as e:
        print(f"Lỗi: {e}")
        return None, None, None, None, None
city, region, country, latitude, longitude = get_location_by_ip()
def get_weather():
    try:
        # Lấy thông tin vị trí từ dịch vụ ipinfo.io
        response = requests.get("https://ipinfo.io")
        data = response.json()
        location = data.get("loc").split(",")
        latitude, longitude = location
        # Lấy thông tin thời tiết từ trang web công cộng
        base_url = f"https://wttr.in/{latitude},{longitude}?format=%t"
        response = requests.get(base_url)
        weather_description = response.text.strip()
        return weather_description
    except Exception as e:
        print(f"Lỗi: {e}")
        return None
weather_description = get_weather()
System.Clear()
print(' Đang chạy tiến trình')
logo = f"""  
\033[1;31m ██████╗ ██╗   ██╗██╗   ██╗██╗  ██╗██╗  ██╗ █████╗ ███╗   ██╗██╗  ██╗
\033[1;36m ██╔══██╗██║   ██║╚██╗ ██╔╝██║ ██╔╝██║  ██║██╔══██╗████╗  ██║██║  ██║
\033[1;32m ██║  ██║██║   ██║ ╚████╔╝ █████╔╝ ███████║███████║██╔██╗ ██║███████║
\033[1;34m ██║  ██║██║   ██║  ╚██╔╝  ██╔═██╗ ██╔══██║██╔══██║██║╚██╗██║██╔══██║
\033[1;35m ██████╔╝╚██████╔╝   ██║   ██║  ██╗██║  ██║██║  ██║██║ ╚████║██║  ██║
\033[1;31m ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
 
               BOX ZALO: https://zalo.me/g/nguadz335
               ADMIN : DUY KHÁNH 
               YTB : REVIEWTOOL247NDK
\033[1;97m= = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
"""
print(logo)
sleep(2)
filename = "allproxy.txt"
a = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=1000000&country=CN&ssl=all&anonymity=all')
b = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=10000000&country=VN&ssl=all&anonymity=all')
c = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=10099999900&country=UK&ssl=all&anonymity=all')
d = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=US&ssl=all&anonymity=all')
e = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=BR&ssl=all&anonymity=all')
f = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=ID&ssl=all&anonymity=all')
h = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=JP&ssl=all&anonymity=all')
k = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=NL&ssl=all&anonymity=all')
i = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=FI&ssl=all&anonymity=all')
y = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=ES&ssl=all&anonymity=all')
z = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=PL&ssl=all&anonymity=all')
l = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=929929199&country=BD&ssl=all&anonymity=all')
print(' \033[1;32mĐào Proxy Thành Công !')
print(' \033[1;36mLưu Trong File allproxy.txt !')
open(filename,"a").write(a.text)
open(filename,"a").write(b.text)
open(filename,"a").write(c.text)
open(filename,"a").write(d.text)
open(filename,"a").write(e.text)
open(filename,"a").write(f.text)
open(filename,"a").write(h.text)
open(filename,"a").write(k.text)
open(filename,"a").write(i.text)
open(filename,"a").write(y.text)
open(filename,"a").write(z.text)
open(filename,"a").write(l.text)
