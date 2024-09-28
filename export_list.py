import wikidot

targets = []

with wikidot.Client() as client:
    site = client.site.get("scp-jp")

    tags = ["scp", "goi-format", "tale"]
    for tag in tags:
        pages = site.pages.search(
            category="_default",
            order="rating desc",
            tags=f"+恐怖コン24 {tag} -コンテスト"
        )
        targets.extend([f"{tag}({page.rating})/{page.fullname}" for page in pages])

with open("export.txt", "w") as f:
    f.write("\n".join(targets))
