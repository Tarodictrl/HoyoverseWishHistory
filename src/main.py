import argparse
import os
import re
from pathlib import Path
import time
import toml
from typing import Optional
import tempfile
import subprocess

import requests
import pyperclip
from urllib.parse import urlparse
from urllib.parse import parse_qs

__version__ = "1.3.3"


class Wish:
    genshin_params = dict(lang="en-us", gacha_type="301", size=5)
    github_release_url = "https://api.github.com/repos/Tarodictrl/GenshinWishHistory/releases/latest"

    def __init__(self, game: str, region: str) -> None:
        self._game = game
        self._api_url = self._getApiUrl(game, region)
        self._log_location = self._getLogPath(game, region)

    @staticmethod
    def _getApiUrl(game: str, region: str) -> str:
        if game == "GenshinImpact":
            if region == "china":
                return "https://public-operation-hk4e.mihoyo.com"
            return "https://hk4e-api-os.hoyoverse.com"
        elif game == "HonkaiStarRail":
            return "https://api-os-takumi.mihoyo.com"

    @staticmethod
    def _getLogPath(game: str, region: str) -> str:
        profile = os.environ['USERPROFILE']
        if game == "GenshinImpact":
            if region == "china":
                china = "\u539f\u795e"
                return f"{profile}\\AppData\\LocalLow\\miHoYo\\{china}\\output_log.txt"
            return f"{profile}\\AppData\\LocalLow\\miHoYo\\Genshin Impact\\output_log.txt"
        elif game == "HonkaiStarRail":
            return f"{profile}\\AppData\\LocalLow\\Cognosphere\\Star Rail\\Player.log"

    def checkNeedUpdate(self) -> bool:
        response = requests.get(self.github_release_url)
        if response.status_code == 200:
            latest_version = response.json().get("tag_name")
            if __version__ < latest_version:
                return True
        return False

    def loadLogs(self):
        if not os.path.exists(self._log_location):
            raise FileNotFoundError("Cannot find the log file! Make sure to open the wish history first!")
        with open(self._log_location) as f:
            return f.read()

    def loadCaches(self, logs: str) -> list:
        if self._game == "GenshinImpact":
            matches = re.search(r"(?m).:/.+(GenshinImpact_Data|YuanShen_Data)", logs, re.I)
        if self._game == "HonkaiStarRail":
            matches = re.search(r"(.:/.+StarRail_Data)", logs, re.I)
        if matches is None:
            raise FileNotFoundError("Cannot find the wish history url! Make sure to open the wish history first!")
        game_dir = matches.group()
        web_caches = sorted(Path(game_dir + "\\webCaches").iterdir(),
                            key=os.path.getmtime, reverse=True
                            )
        cache_file_path = f"{web_caches[0]}\Cache\Cache_Data\data_2"
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, 'temp_cache')
        os.system(f'echo.>{temp_path}')
        subprocess.run(['powershell', '-Command', f'copy "{cache_file_path}" "{temp_path}"'])
        with open(temp_path, encoding="utf-8", errors='ignore') as f:
            content = f.read()
        splitted = content.split("1/0/")
        if self._game == "GenshinImpact":
            found = [x for x in splitted if re.search("webview_gacha", x) is not None]
        if self._game == "HonkaiStarRail":
            found = [x for x in splitted if re.search("/getGachaLog", x) is not None]
        return found

    def getLink(self, cache: str) -> Optional[str]:
        if self._game == "GenshinImpact":
            t = re.findall(r"(https.+?game_biz=)", cache)
        if self._game == "HonkaiStarRail":
            t = re.findall(r"(https.+?end_id=)", cache)
        link = t[0]
        if self._game == "GenshinImpact":
            test_result = self.testGenshinUrl(link)
        elif self._game == "HonkaiStarRail":
            test_result = self.testHonkaiUrl(link)
        if test_result:
            return link

    def testGenshinUrl(self, url: str) -> bool:
        try:
            uri = f"{self._api_url}/gacha_info/api/getGachaLog"
            params = parse_qs(urlparse(url).query)
            params.update(self.genshin_params)
            response = requests.get(url=uri, params=params)
            if response.status_code == 200:
                test_result = response.json()
                return test_result.get("retcode", -1) == 0
        except TimeoutError:
            print("Check link failed!")
        return False

    def testHonkaiUrl(self, url: str) -> bool:
        try:
            response = requests.get(url=url)
            if response.status_code == 200:
                test_result = response.json()
                return test_result.get("retcode", -1) == 0
        except TimeoutError:
            print("Check link failed!")
        return False


def printLogo():
    print("""
 ______   ______     ______     ______     _____     __     ______     ______   ______     __        
/\__  _\ /\  __ \   /\  == \   /\  __ \   /\  __-.  /\ \   /\  ___\   /\__  _\ /\  == \   /\ \       
\/_/\ \/ \ \  __ \  \ \  __<   \ \ \/\ \  \ \ \/\ \ \ \ \  \ \ \____  \/_/\ \/ \ \  __<   \ \ \____  
   \ \_\  \ \_\ \_\  \ \_\ \_\  \ \_____\  \ \____-  \ \_\  \ \_____\    \ \_\  \ \_\ \_\  \ \_____\ 
    \/_/   \/_/\/_/   \/_/ /_/   \/_____/   \/____/   \/_/   \/_____/     \/_/   \/_/ /_/   \/_____/                                                                                                                   
""")


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--open", help="Open paimon.moe automatically (Default)", action='store_true', default=True)
parser.add_argument("--game", help="Select game. Support: GenshinImpact, HonkaiStarRail (Genshin Impact Default)",
                    choices=["GenshinImpact", "HonkaiStarRail"], default="GenshinImpact", metavar='')
parser.add_argument("--no-open", help="Don't open paimon.moe automatically", dest='open', action='store_false')
parser.add_argument("-r", help="Select region. Support: global, china",
                    choices=["global", "china"], metavar='', default="global")
args = parser.parse_args()

if __name__ == "__main__":
    flag = False
    wish = Wish(game=args.game, region=args.r)
    try:
        logs = wish.loadLogs()
        caches = wish.loadCaches(logs)
        for i in range(len(caches) - 1, -1, -1):
            os.system("cls")
            printLogo()
            print(f"Checking link: {i}\n")
            link = wish.getLink(caches[i])
            if link:
                flag = True
                pyperclip.copy(link)
                print(link)
                print("\033[92m" + "\nLink copied to clipboard!\n" + "\x1b[0m")
                break
            time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        if not flag:
            print("Cannot find the wish history url! Make sure to open the wish history first!\n")
        else:
            if args.open:
                import webbrowser
                if args.game == "GenshinImpact":
                    webbrowser.open('https://paimon.moe/wish/import', new=2)
                if args.game == "HonkaiStarRail":
                    webbrowser.open('https://pom.moe/warp/import', new=2)
        if wish.checkNeedUpdate():
            print("\033[92m" + "A new version is available, visit: https://github.com/Tarodictrl/GenshinWishHistory/releases/latest\n" + "\x1b[0m")
        for i in range(9, 0, -1):
            print(f"Window will close after: {i} s", end="\r", flush=True)
            time.sleep(1)
