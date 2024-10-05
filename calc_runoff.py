import wikidot
import datetime


class DatumStructure:
    def __init__(self, fullname: str, rating: int, runoff_rating: int, author: str):
        self.fullname = fullname
        self.rating = rating
        self.runoff_rating = runoff_rating
        self.author = author

    def total_rating(self):
        return self.rating + self.runoff_rating


class VoterStructure:
    def __init__(self):
        self.uv = 0
        self.dv = 0
        self.runoff_uv = 0
        self.runoff_dv = 0

    def total_vote(self):
        return self.uv - self.dv

    def total_runoff_vote(self):
        return self.runoff_uv - self.runoff_dv

    def increment_uv(self):
        self.uv += 1

    def increment_dv(self):
        self.dv += 1

    def increment_runoff_uv(self):
        self.runoff_uv += 1

    def increment_runoff_dv(self):
        self.runoff_dv += 1


data = {
    "scp": [],
    "goi-format": [],
    "tale": []
}

# voters = {}

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
    page_time = datetime.datetime.now()

    runoff_pages = {
        page.fullname.removeprefix("poll:terror24-"): page
        for page in site.pages.search(
            category="poll",
            order="rating desc",
            name="terror24-*"
        )
    }
    runoff_time = datetime.datetime.now()

    for fullname, runoff_page in runoff_pages.items():
        page = pages.get(fullname)
        if page:
            for tag in data.keys():
                if tag in page.tags:
                    data[tag].append(
                        DatumStructure(fullname, page.rating, runoff_page.rating, page.created_by.unix_name))
                    break

            # for v in page.votes:
            #     if v.user.unix_name not in voters:
            #         voters[v.user.unix_name] = VoterStructure()
            #     if v.value == 1:
            #         voters[v.user.unix_name].increment_uv()
            #     elif v.value == -1:
            #         voters[v.user.unix_name].increment_dv()
            #
            # for v in runoff_page.votes:
            #     if v.user.unix_name not in voters:
            #         voters[v.user.unix_name] = VoterStructure()
            #     if v.value == 1:
            #         voters[v.user.unix_name].increment_runoff_uv()
            #     elif v.value == -1:
            #         voters[v.user.unix_name].increment_runoff_dv()

for tag, datums in data.items():
    datums.sort(key=lambda datum: datum.total_rating(), reverse=True)

with open("calc_runoff.txt", "w") as f:
    f.write(f"Page Time: {page_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Runoff Time: {runoff_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    for tag, datums in data.items():
        f.write(f"{tag}\n")
        f.write("\n".join(
            [
                f"{str(datum.total_rating()).rjust(3, ' ')}\t({str(datum.rating).rjust(3, ' ')} + {str(datum.runoff_rating).rjust(3, ' ')})\t{datum.fullname} ({datum.author})"
                for datum
                in
                datums]))
        f.write("\n\n")

    # f.write("Voters\n")
    # for user, voter in voters.items():
    #     f.write(f"{user}\t{voter.total_vote()}({voter.uv} - {voter.dv})\t{voter.total_runoff_vote()}({voter.runoff_uv} - {voter.runoff_dv})\n")
