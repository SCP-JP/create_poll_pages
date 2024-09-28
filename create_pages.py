import os
import re
from pprint import pprint

import wikidot
from dotenv import load_dotenv

load_dotenv()

WD_USER = os.getenv("WD_USER")
WD_PASS = os.getenv("WD_PASS")

# targets.txt読み込み
with open("targets.txt", "r") as f:
    raw_targets = f.read().splitlines()

targets = []
regex = re.compile(r"^(.+)\((\d+)\)/(.+)$")
for target in raw_targets:
    match = regex.match(target)
    if match:
        targets.append({
            "tag": match.group(1),
            "rating": int(match.group(2)),
            "fullname": match.group(3)
        })
    else:
        print(f"Invalid target: {target}")
        raise ValueError


with wikidot.Client(username=WD_USER, password=WD_PASS) as client:
    site = client.site.get("pseudo-scp-jp")

    for target in targets:
        source = f"""[[>]]
[[module Rate]]
[[/>]]
[[module ThemePreviewer noUi="true"]]
[[div class="blockquote pollNote"]]
このページは**[[[terror-contest-2024|]]]**の決選投票用ページです
* **対象記事: [[[{target['fullname']}|]]]**
* **投稿時評価: {target['rating']}**
[[/div]]
"""
        title = f"恐怖コン決選投票-{target['tag']}/{target['fullname']}"

        page = site.page.create(
            fullname=f"uktest:poll:{target['fullname']}",
            title=title,
            source=source,
            comment=f"決選投票ページ作成: {target['tag']}/{target['fullname']}"
        )

