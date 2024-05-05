import os

USER_PROFILE = os.environ['USERPROFILE']
LOG_LOCATION = f"{USER_PROFILE}\\AppData\\LocalLow\\miHoYo\\Genshin Impact\\output_log.txt"
API_HOST = "https://hk4e-api-os.hoyoverse.com"
PARAMS = {
    "lang": "en-us",
    "gacha_type": "301",
    "size": 5,
}
HEADERS = {
    "ContentType": "application/json"
}
VERSION = "1.2.0"
GITHUB_RELEASE_URL = "https://api.github.com/repos/Tarodictrl/GenshinWishHistory/releases/latest"
