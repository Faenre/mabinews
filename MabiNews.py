#! /usr/bin/env python3

import hashlib
import json

# pip install
import requests
from lxml import html

with open('./webhook.txt', 'r') as f :
    WEBHOOK = f.read()

class Article() :
    url = "http://mabinogi.nexon.net"
    tags = {
        'ANNOUNCE'  : "Announcement",
        'EVENTS'    : "Event",
        'MAINT'     : "Maintenance"
        }

    def __init__(self, tr) :
        """
        Create an Article entry using the table row element of the listing

        Input:
            tr : table row for the individual news listing on /News/All/#
        """
        self.link = Article.url + tr.xpath('./td[1]/a/@href')[0]
        self.name = tr.xpath('./td[1]/a/text()')[0]
        self.date = tr.xpath('./td[2]/text()')[0]
        self.tag  = Article.tags[tr.xpath('./td[3]/span/text()')[0].strip()]
        print("[{self.tag:<12}] {self.date}: {self.name}".format(self=self))
        hash = hashlib.md5((self.link+self.name+self.date+self.tag).encode())
        self.hash = hash.hexdigest()
        print("0x"+self.hash[-6:])

    def GetContents (self) :
        """
        Populate various fields (if they exist within the div)

        Input:
            none
        """

        page = requests.get(self.link)
        tree = html.fromstring(page.content)
        div = tree.xpath('//div[@id="news-content"]')[0]

        img = div.xpath('//img[1]')[0]
        self.image = {
            'url'   : img.get('src'),
            'height': img.get('height'),
            'width' : img.get('width')
        }
        p = div.xpath('//p')
        self.desc = ""
        for desc in p :
            text = "".join(desc.itertext())

            if len("".join(text.split())) > 50 :
                self.desc = {'text': text}
                break

    def PostToDiscord(self) :
        payload = {"embeds":[{
            "title"         : self.name,
            "description"   : "{a.tag} - {a.date}".format(a=self),
            "url"           : self.link,
            "color"         : int(self.hash[-6:],16),
            "image"         : self.image,
            "footer"        : self.desc,
            }]}
        rq = requests.post(WEBHOOK, json=payload)


def GetArticles() :
    """Checks the news page for new announcements.
    Yields each article in reverse order (newest last)
    """
    URL = "http://mabinogi.nexon.net/News/All/1"
    page = requests.get(URL)
    tree = html.fromstring(page.content)

    articles = []

    for tr in list(tree.xpath('//table[@class="list"]/tbody/*'))[::-1] :
        a = Article(tr)
        yield a


def OldHashes(fn) :
    try :
        with open(fn, 'r') as f :
            return json.load(f)
    except Exception as e :
        return [] # TODO

def SaveHashes(hashes, fn) :
    with open(fn, 'w') as f :
        json.dump(hashes, f)

if __name__ == "__main__" :
    fn = "hashes.json"
    fresh_articles = GetArticles()
    hashes = OldHashes(fn)
    _SILENT = not hashes
    new = False
    for a in GetArticles() :
        if a.hash not in hashes :
            hashes.append(a.hash)
            new = True
            a.GetContents()
            if not _SILENT :
                a.PostToDiscord()
    if new :
        SaveHashes(hashes, fn)
