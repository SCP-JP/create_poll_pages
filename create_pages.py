import os
import re

import wikidot
from dotenv import load_dotenv

load_dotenv()

WD_USER = os.getenv("WD_USER")
WD_PASS = os.getenv("WD_PASS")

# targets.txt読み込み
with open("targets.txt", "r") as f:
    raw_targets = f.read().splitlines()

targets = []
sources = []
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
    site = client.site.get("scp-jp")

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
            fullname=f"poll:terror24-{target['fullname']}",
            title=title,
            source=source,
            comment=f"決選投票ページ作成: {target['tag']}/{target['fullname']}"
        )

        page.set_tags(["jp", "投票"])

        # ページ掲載用ソース生成
        source = f"""[[module listpages category="_default" fullname="{target['fullname']}" limit="1" separate="no" wrapper="no"]]
[[div_ class="runoff-item"]]
[[div_ class="runoff-heading"]]
%%title_linked%%
[[/div]]
[[div_ class="runoff-author"]]
by [[user %%created_by_unix%%]]
[[/div]]
[[div_ class="runoff-voting"]]
評価： [[span class="runoff-voting-value"]]%%rating%%[[/span]]
[[/div]]
[[div_ class="runoff-ratemodule"]]
[[iframe http://scp-jp.wikidot.com/poll:terror24-%%fullname%%?theme_url=https://scp-jp.wdfiles.com/local--code/terror-contest-2024/1 scrolling="no" style="width:100%;height:1.75em;overflow:hidden;" frameborder="0"]]
[[/div]]
[[/div]]
[[/module]]"""
        sources.append(source)
        print(source)

with open("sources.txt", "w") as f:
    f.write("\n\n\n".join(sources))
