import urllib.request
import requests
from os import path, mkdir
from shutil import rmtree
from bs4 import BeautifulSoup
import html2text
import io

#define user agent for query to force desktop viewing for optimal scraping
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
headers = {"user-agent" : USER_AGENT}

ILL_CHARS = ['<', '>', ':', '"', '\\', '|', '?', '*'] #array of illegal characters in order to avoid windows filename errors

count_q = int(input("how many queries? ")) #ask about how many queries (topics) to gather
queries = []
for x in range(count_q): #loop and input query names appended into the query array
    i = input(f"query {x+1}: ") 
    queries.append(i)
#print(queries)

if(count_q != 0):
    if path.exists("./dataset/"): #create (or remove first then create) directory to hold dataset
        rmtree("./dataset/")
    mkdir("./dataset/")


for x in range(count_q): #BEGIN query loop
    query = queries[x]
    print(f"QUERY: {query}")
    mkdir(f'./dataset/{query}') #make the category directory
    mkdir(f'./dataset/{query}/text/')
    query.replace(' ', "+") #replace spaces with + so that it works in the Google query search
    URL  = f"https://google.com/search?q={query}" 

    resp = requests.get(URL, headers=headers) #use requests library to request the Google search results webpage

    if resp.status_code == 200: #code 200 means successful request
        soup = BeautifulSoup(resp.content, "html.parser") 

    results = []
    for g in soup.find_all('div', class_='r'): #parse through all the google search results looking for titles and links
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            item = {
                "title": title,
                "link": link
            }
            results.append(item)

    next = soup.find(id='pnnext') #use the parser to find the link to the next google search page
    next_link = next['href']
    
    next_page = "https://www.google.com"+next_link #concat. the search link with a google page link

    whitelist = [ #an array of allowed text sources within an HTML page to get important text
        'p'
    ]
    
    for x in results: #go thru the array of search results and scrape those pages
        print(f"{x}")
        url = x.get('link') #use the dictionary to grab the link
        response = requests.get(url, headers=headers) #request the page in said search result
        if response.status_code != 200:
            continue
           
        title = x.get('title') 
        if('/' in title):
            title = title.replace('/', '-') #this serves to remove slashes in the title because otherwise it messes up the directory tree

        fileH = f"./dataset/{query}/{title}.html" #format a string to become the .html file name
        fileT = f"./dataset/{query}/text/{title}.txt"

        for ch in ILL_CHARS:
            if ch in fileH:
                fileH = fileH.replace(ch, '') #replace characters that produce windows errors in filenames
            if ch in fileT:
                fileT = fileT.replace(ch, '')

        output = ''
        searchSoup = BeautifulSoup(response.content, 'html.parser') #open a new soup object to parse text within HTML
        text = searchSoup.find_all(text=True) #find all elements that contain text (non-HTML)

        for t in text: #iterate through all elements and put them into output string if their element parent is a paragraph <p>
            if t.parent.name in whitelist:
                output += '{} '.format(t)
        
        with open(fileH, 'wb') as f:
            f.write(response.content) #write to the file

        with io.open(fileT, 'w', encoding="utf-8") as ff: #write to .txt file with utf-8 to support any characters
            #ff.write(h.handle(response.text))
            ff.write(output)

    resp = requests.get(next_page, headers=headers) #this requests the next page of search results

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

    results = []
    for g in soup.find_all('div', class_='r'): #again, parse through the google page to obtain the actual results
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            item = {
                "title": title,
                "link": link
            }
            results.append(item)

    for x in results: #repeat for the next page (yes, i know this could've been done with a loop or function im lazy)
        print(f"{x}")
        url = x.get('link')
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            continue

        title = x.get('title')
        if('/' in title):
            title = title.replace('/', ' ')
        

        fileH = f"./dataset/{query}/{title}.html"
        fileT = f"./dataset/{query}/text/{title}.txt"
        for ch in ILL_CHARS:
            if ch in fileH:
                fileH = fileH.replace(ch, '')
            if ch in fileT:
                fileT = fileT.replace(ch, '')
        
        output = ''
        searchSoup = BeautifulSoup(response.content, 'html.parser')
        text = searchSoup.find_all(text=True)
        # h = html2text.HTML2Text()
        # h.ignore_links = True #these are settings for html2text object
        # h.ignore_images = True
        # h.ignore_tables = True

        #print(h.handle(response.text))
        for t in text:
            if t.parent.name in whitelist:
                output += '{} '.format(t)

        with open(fileH, 'wb+') as f:
            f.write(response.content)

        with io.open(fileT, 'w', encoding="utf-8") as ff:
            #ff.write(h.handle(response.text))
            ff.write(output)
            

       
