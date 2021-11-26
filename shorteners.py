import pyshorteners

def getShortURL(url):
    try:
        x = pyshorteners.Shortener()
        Geturl=str(url)
        short=x.tinyurl.short(Geturl)
        return short
    except:
        return False


