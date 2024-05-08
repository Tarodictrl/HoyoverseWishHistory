# Genshin Impact Wish History
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/tarodictrl/GenshinWishHistory?style=flat-square)](https://github.com/tarodictrl/GenshinWishHistory/releases) [![GitHub](https://img.shields.io/github/license/tarodictrl/GenshinWishHistory?style=flat-square)](https://github.com/tarodictrl/GenshinWishHistory/blob/main/LICENSE) ![GitHub repo size](https://img.shields.io/github/repo-size/tarodictrl/GenshinWishHistory?style=flat-square&label=size) ![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/tarodictrl/GenshinWishHistory/total?style=flat-square)

Get Genshin Impact wish url for [paimon.moe](https://paimon.moe)

### Installation
```bash
git clone https://github.com/Tarodictrl/GenshinWishHistory.git
```
or download [latest release](github.com/Tarodictrl/GenshinWishHistory/releases/latest)
### Arguments
```bash
>>> python main.py -h
usage: main.py [-h] [--open] [--no-open] [-r]

optional arguments:
  -h, --help  show this help message and exit
  --open      Open paimon.moe automatically (Default)
  --no-open   Don't open paimon.moe automatically
  -r          Select region. Support: global, china
```
### Usage with python
```
cd GenshinWishHistory\src
python -m venv .venv
.venv\Scripts\activate
python main.py
```
### References

- [Original powershell script](https://gist.github.com/MadeBaruna/1d75c1d37d19eca71591ec8a31178235/)

### License
This project is made available under the [MIT License](https://github.com/Tarodictrl/GenshinWishHistory/blob/main/LICENSE).
