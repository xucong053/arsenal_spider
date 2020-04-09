import os
import requests
import csv
import tqdm


def download_img(url, name):
    if not os.path.exists("./images/"):
        os.mkdir("./images/")
    name = name.replace("/", "_").replace('"', '“')
    if os.path.exists("./images/" + name + '.jpg'):
        return
    req = requests.get(url=url)
    try:
        with open("./images/" + name + '.jpg', 'wb') as f:
            f.write(req.content)
    except Exception as e:
        print(e)


def read_csv(address):
    with open(address, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
        for num in tqdm.trange(1, len(rows)):
            download_img(rows[num][2], rows[num][1])


if __name__ == '__main__':
    read_csv("./data/arsenal.csv")
