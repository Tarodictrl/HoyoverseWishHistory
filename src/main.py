import os
import re
from pathlib import Path
import time
from typing import Optional
import tempfile
import subprocess

import requests
import pyperclip
from urllib.parse import urlparse
from urllib.parse import parse_qs

from core.constants import (
    API_HOST,
    PARAMS,
    LOG_LOCATION,
    HEADERS
)


def testUrl(url: str) -> Optional[dict]:
    try:
        uri = f"{API_HOST}/gacha_info/api/getGachaLog"
        params = parse_qs(urlparse(url).query)
        params.update(PARAMS)
        response = requests.get(url=uri, params=params, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
    except TimeoutError:
        print("Check link failed!")


if not os.path.exists(LOG_LOCATION):
    exit("Cannot find the log file! Make sure to open the wish history first!")

with open(LOG_LOCATION) as f:
    logs = f.read()

matches = re.search(r"(?m).:/.+(GenshinImpact_Data|YuanShen_Data)", logs, re.I)

if matches is None:
    exit("Cannot find the wish history url! Make sure to open the wish history first!")

game_dir = matches.group()
web_caches = sorted(Path(game_dir + "\\webCaches").iterdir(),
                    key=os.path.getmtime, reverse=True)
cache_file = f"{web_caches[0]}\Cache\Cache_Data\data_2"
temp_dir = tempfile.gettempdir()
temp_path = os.path.join(temp_dir, 'temp_cache')
os.system(f'echo.>{temp_path}')
subprocess.run(['powershell', '-Command', f'copy "{cache_file}" "{temp_path}"'])

with open(temp_path, encoding="utf-8", errors='ignore') as f:
    content = f.read()

splitted = content.split("1/0/")
found = [x for x in splitted if re.search("webview_gacha", x) is not None]
flag = False

for i in range(len(found)-1, -1, -1):
    t = re.findall(r"(https.+?game_biz=)", found[i])
    link = t[0]
    os.system("cls")
    print(f"Checking link: {i}\n")
    test_result = testUrl(link)
    if test_result.get("retcode", -1) == 0:
        flag = True
        print(link)
        pyperclip.copy(link)
        print("\033[92m" + "\nLink copied to clipboard!\n" + "\x1b[0m")
        break
    time.sleep(1)

if not flag:
    print("Cannot find the wish history url! Make sure to open the wish history first!\n")

for i in range(9, 0, -1):
    print(f"Window will close after: {i} s", end="\r", flush=True)
    time.sleep(1)
