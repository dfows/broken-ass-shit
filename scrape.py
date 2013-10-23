#get a python script to import the html file and parse it to scrape all inline styles

from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self,posStakk,outF,plain):
        HTMLParser.__init__(self)
        #keep track of position in DOM
        #i will use a stack.  every time i enter, i push the element onto the stack
        self.posStakk = posStakk
        #outputF is the external CSS file that I am generating
        self.outputF = outF
        #markupF is the styleless HTML file that I am generating
        self.markupF = plain
    def handle_starttag(self, tag, attrs):
        self.markupF.write(self.rewrite_start_tag(tag,attrs))
        #prepare an external stylesheet
        if tag == "head":
          self.markupF.write("<link href='asdf.css' type='text/css' rel='stylesheet'>")
        self.update_stakk(tag,attrs)
        #if there's an inline style in this tag, extract it
        if "style" in [attr[0] for attr in attrs]:
          self.extract_styling(tag,attr)
        return tag
    def handle_endtag(self, tag):
        self.markupF.write("</"+tag+">")
        self.posStakk.pop(-1)
        return "end"
    def handle_data(self, data):
        self.markupF.write(data)

    #helper functions
    #reconstructs the start tag by combining each attr[0] with attr[1]
    #this is used to make a copy of the document where inline styles are not present.  I suppose I could have just made a copy of the document and resisted copying over the styling.  We'll see.
    def rewrite_start_tag(self, tag, attrs):
        start_tag = "<"+tag
        for attr in attrs:
          if attr[0] != "style":
            start_tag += " "+attr[0]+"=\""+attr[1]+"\""
        start_tag += ">"
        return start_tag
    #pushes the next element onto the position stack
    #takes extra note of any id or class
    def update_stakk(self, tag, attrs):
        element = tag
        for attr in attrs:
          if attr[0] == "class":
            element += "."+attr[1].replace(" ",".")
          if attr[0] == "id":
            element += "#"+attr[1].replace(" ","#")
        self.posStakk.append(element)
    #cobbles together a selector by reading from the position stack
    #writes to the CSS file the selector and the styling
    def extract_styling(self, tag, attr):
        selektor = ''
        styling = attr[1]
        for i in range(1,len(self.posStakk)):
          selektor += self.posStakk[i]+" "
        selektor += "{"
        self.outputF.write(selektor+styling+"}\n")

def scrapeStyles():
  #create a stack to hold location within nested elements
  #and an output file to hold CSS
  posStakk = []
  outF = open('asdf.css','w')
  styleless = open('asdf2.html','w')

  # instantiate the parser and feed it some HTML
  parser = MyHTMLParser(posStakk,outF,styleless)
  
  #open file
  page = open('asdf.html','r+')
  
  #pipe entire page contents into parser
  parser.feed(page.read())

# unfortunately i am falling the fuck asleep right here

scrapeStyles()
