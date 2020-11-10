import requests
from html.parser import HTMLParser
import hashlib
import datetime
import json
import os
import xml.etree.ElementTree as ET
import urllib.robotparser


class JsonLdHTMLParser(HTMLParser):

    def __init__(self, url, datadir):
        super().__init__()
        self.found = False
        self.url = url
        self.timestamp = datetime.datetime.now().timestamp()
        self.datadir = datadir
    
    def get_filename(self):
        key = "{0}|{1}".format(self.url, self.timestamp)
        filename =  "{0}.json".format(
            hashlib
            .sha224(key.encode('utf-8'))
            .hexdigest()
        )

        return os.path.join(self.datadir, filename)
    
    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            for attr in attrs:
                if attr[0] == 'type' and attr[1] == 'application/ld+json':
                    self.found = True

    def handle_endtag(self, tag):
        if self.found:
            self.found = False

    def handle_data(self, data):
        if self.found:
            try:
                jsonld = {}
                jsonld["data"] = json.loads(data)
                jsonld["url"] = self.url
                jsonld["time"] = self.timestamp
                with open(self.get_filename(), 'w+') as fp:
                    fp.write(json.dumps(jsonld))
            except Exception as e:
                print("handle_data : {0}".format(e))

def get_html(url):
    try:
        resp = requests.get(url)
        if resp.ok:
            return resp.text
        else:
            return None
    except Exception as e:
        print("get_html : {0}".format(e))
    return None

def fetch_data(urls, rp, datadir=None):
    if not datadir:
        datadir = os.getcwd()
    for url in urls:
        if can_fetch(rp, "*", url):
            htmltext = get_html(url)
            parser = JsonLdHTMLParser(url, datadir)
            if htmltext:
                parser.feed(htmltext)    

def parse_data(datadir=None):
    if not datadir:
        datadir = os.getcwd()    
    json_files = [ f for f in os.listdir(datadir) if os.path.isfile(f) and f.split(".")[1] == 'json']
    for jf in json_files:
        with open(jf) as fp:
            try:
                data = json.loads(fp.read())
                print("[{0}][{1}]".format(data["time"], data["url"]))
                if type(data["data"]) is list:
                    for d in data["data"]:
                        print("{0} : {1}".format(d["@context"], d["@type"]))
                else:
                    print("{0} : {1}".format(data["@context"], data["@type"]))
            except Exception as e:
                print("load files : {0}".format(e))    

def fetch_sitemap(domain, url=None, outdir=None):
    if not url:
        url = "{0}/sitmap.xml".format(domain)
    if not outdir:
        outdir = os.getcwd()
    try:
        resp = requests.get(url)
        if resp.ok:
            filename = os.path.join(outdir, 'sitemap.xml')

        with open(filename, 'w+') as fp:
            fp.write(resp.text)
        return filename

    except Exception as e:
        print("fetch_sitemap : {0}".format(e))
    return None

def parse_sitemap(sitemap):
    urls = []
    tree = ET.parse(sitemap)
    root = tree.getroot()
    for url in root:
        for loc in url:
            if 'loc' in loc.tag:
                urls.append(loc.text)
    return urls

def get_robotstxt(domain):
    url = "{0}/robots.txt".format(domain)
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url)
    rp.read()
    return rp

def get_rate(rp, user_agent):
    return rp.request_rate(user_agent)

def get_crawl_delay(rp, user_agent):
    return rp.crawl_delay(user_agent)    
    
def get_sitemaps(rp):
    return rp.site_maps()

def can_fetch(rp, user_agent, url):
    return rp.can_fetch(user_agent, url)

if __name__ == "__main__":
    
    domain = ''

    rp = get_robotstxt(domain)
    print(get_rate(rp, "*"))
    print(get_crawl_delay(rp, "*"))
    
    sitemaps = get_sitemaps(rp)
    print(sitemaps)
    
    urls = []
    for sitemap_url in sitemaps:
        sitemap_content = fetch_sitemap(None, url=set_url)
        urls.extend(parse_sitemap(sitemap_content)
    fetch_data(urls[0:1])
    parse_data()
