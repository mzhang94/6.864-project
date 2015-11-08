import urllib2
from BeautifulSoup import BeautifulSoup
import re, string

class Book:
    def __init__(self, name):
        self.name = name
        self.url = "http://www.sparknotes.com/lit/%s/characters.html" % name
        self.characters = {}

    def getCharactersFromWeb(self):
        page = urllib2.urlopen(self.url)
        soup = BeautifulSoup(page.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)
        regex = re.compile('<!--\\n.*DisplayAds.*\\n.*-->')
        for div in soup.findAll("div", {"class" :"content_txt"}):
            self.characters[div.get('id')] = regex.sub("", div.text)

books = set([])
for l in string.ascii_lowercase:
    url = "http://www.sparknotes.com/lit/index_%s.html" % l
    page = urllib2.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html)

    for link in soup.findAll('a'):
        url = link.get('href')
        if not url == None and url.startswith("http://www.sparknotes.com/lit/"):
            book = url[30:]
            if book != "" and not book.startswith("index"):
                books.add(book)
