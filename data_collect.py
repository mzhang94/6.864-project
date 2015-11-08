import urllib2
from django.utils.encoding import smart_str, smart_unicode
from BeautifulSoup import BeautifulSoup
import re, string, os

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
            name = div.get('id')
            # get rid of ads and remove first line
            text = regex.sub("", div.text)
            text = text.split('\n')[1:]
            text = '\n'.join(text)
            text = text.replace('\n', ' ')
            text = text.strip()

            s = text.split('.')
            first_sentence = text.split('.')[0]
            if re.search(name, first_sentence, re.IGNORECASE) == None: 
                if first_sentence.startswith('A ') or first_sentence.startswith('An ') or first_sentence.startswith('The '):
                    first_sentence = first_sentence[0].lower() + first_sentence[1:]
                first_sentence = name + ' is ' + first_sentence
                s[0] = first_sentence
                text = '.'.join(s)
                
            text = smart_str(text)
            self.characters[name] = text

    def writeToFile(self):
        directory = 'books/%s' % self.name
        if not os.path.exists(directory):
            os.makedirs(directory)
        for name in self.characters:
            f = open('%s/%s' % (directory, name), 'w')
            f.write(self.characters[name])

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
                print 'getting book %s' % book
                books.add(book)
                book = Book(book)
                book.getCharactersFromWeb()
                book.writeToFile()
