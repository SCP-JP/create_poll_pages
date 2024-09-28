import wikidot


class DatumStructure:
    def __init__(self, fullname: str, rating: int, runoff_rating: int, author: str):
        self.fullname = fullname
        self.rating = rating
        self.runoff_rating = runoff_rating
        self.author = author

    def total_rating(self):
        return self.rating + self.runoff_rating


data = {
    "scp": [],
    "goi-format": [],
    "tale": []
}

with wikidot.Client() as client:
    site = client.site.get("scp-jp")

    pages = {
        page.fullname: page
        for page in site.pages.search(
            category="_default",
            order="rating desc",
            tags=f"+恐怖コン24 -コンテスト"
        )
    }

    runoff_pages = {
        page.fullname.removeprefix("poll:terror24-"): page
        for page in site.pages.search(
            category="poll",
            order="rating desc",
            name="terror24-*"
        )
    }

    for fullname, runoff_page in runoff_pages.items():
        page = pages.get(fullname)
        if page:
            for tag in data.keys():
                if tag in page.tags:
                    data[tag].append(DatumStructure(fullname, page.rating, runoff_page.rating, page.created_by.unix_name))
                    break

for tag, datums in data.items():
    datums.sort(key=lambda datum: datum.total_rating(), reverse=True)

with open("calc_runoff.txt", "w") as f:
    for tag, datums in data.items():
        f.write(f"{tag}\n")
        f.write("\n".join(
            [f"{datum.total_rating()}\t({datum.rating} + {datum.runoff_rating})\t{datum.fullname} ({datum.author})" for datum
             in
             datums]))
        f.write("\n\n")
