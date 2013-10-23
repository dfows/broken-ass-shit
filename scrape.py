#get a python script to import the html file and parse it to scrape all inline styles

from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        #keep track of position in DOM
        #i will use a stack.  every time i enter, i push the element onto the stack
        self.posStakk = []
    def handle_starttag(self, tag, attrs):
        element = tag
        styling = ''
        selektorVal = ''
        selektor = ''
        for attr in attrs:
          if attr[0] == "class":
            element += "."+attr[1]
          if attr[0] == "id":
            element += "#"+attr[1]
          if attr[0] == "style":
            selektorVal = attr[1]
        self.posStakk.append(element)
        if selektorVal:
          for i in range(1,len(self.posStakk)):
            selektor += self.posStakk[i]+" "
          selektor += "{" 
          print selektor, selektorVal, "}"
        return tag
    def handle_endtag(self, tag):
        self.posStakk.pop(-1)
        return "end"
    #def handle_data(self, data):
        #print "Encountered some data  :", data

def scrapeStyles():
  # instantiate the parser and feed it some HTML
  parser = MyHTMLParser()

  #open file
  page = open('asdf.html','r+')
  
  parser.feed(page.read())

# unfortunately i am falling the fuck asleep right here

scrapeStyles()
