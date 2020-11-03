# MabiNews

*AKA Queen Eirawen*

This is a Discord webhook bot which posts to a channel any time a new blog post, patch update, or really anything new happens.

![Sample](https://i.imgur.com/WP717iZ.png)

Frankly it's quite garbage, I wrote it for some friends in about an hour, 3-4 years ago.  I'm publishing it in case anyone wants to use it, but the code itself would make a fantastic Bearenstain Bears episode: "How Not To Write A Scraper".  If I ever revisit this, it should quite simply use BeautifulSoup and be done with it.

Requirements:
>
```sh
pip3 install requests lxml
```

Usage:
>
```sh
cd mabinews
python3 ./MabiNews.py
```

On a crontab:
>
```sh
*/10 * * * * /home/cronstack/mabinews/news.sh
```
