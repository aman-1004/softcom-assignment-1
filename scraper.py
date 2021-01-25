import requests 
from bs4 import BeautifulSoup as Soup
import os 
import re

regex =re.compile('[a-zA-Z0-9\ _.-]*')

############ DOESN'T WORK FOR HOMEPAGE AS IT REQUIRED JS RENDERING ########################

Parent = os.getcwd()

def info(soup,file):
    file.write("###################################### TITLE ##################################################\n")
    title= soup.find('h1',attrs={"class":"_23498"})
    if title==None : 
        title = soup.find('div',attrs={"class":"fixedheading"}).span
    title = title.text
    file.write(title+"\n\n")
    file.write("###################################### DATE  ##################################################\n")
    time = soup.find('div',attrs={"class":"_3Mkg- byline"})
    if time==None:
        time = soup.find('div',attrs={"class":"bottom-area clearfix"})
    time = time.text[-24:]
    file.write(time+"\n\n")
    file.write("###################################### TEXT  ##################################################\n")
    text_content = soup.find('div',attrs={"class":"ga-headlines"})
    if text_content == None:
        text_content = soup.find('div',attrs={"class":"Normal"})
    text_content = text_content.text
    text_content = text_content.replace('. ','. \n')
    file.write(text_content+"\n\n")

def init(page):
    listdir = os.listdir()
    if not page in listdir:
        os.makedirs(os.getcwd()+'/'+page)


def scrap(page='',total=None): 
    init(page)
    home = 'https://timesofindia.indiatimes.com'
    href =  home + '/'+ page 
    print("Now Scrapping :",href)
    res = requests.get(href)
    soup = Soup(res.content,'lxml')
    urls=[]
    spans = soup.findAll('span',attrs={"class":"w_tle"})
    k = 0 
    for span in spans :
        if(span.a != None):
            url =span.a['href']
            if url[-4:] =='.cms' and url.split('/',2)[1] ==page:
                urls.append(home+span.a['href'])
    if page=='':
        os.chdir(Parent+'/home')
    else :
        os.chdir(Parent+'/'+page)
    done = 0 
    if total == None :
        total = len(urls)
    for url in urls[0:total]:
        res = requests.get(url).content
        soup=Soup(res,"lxml")
        title= soup.find('h1',attrs={"class":"_23498"})
        if title==None : 
            title = soup.find('div',attrs={"class":"fixedheading"}).span
        title = title.text
        filename = regex.search(title).group()[0:32].strip() +'.txt'
        with open(filename,'w+') as file:
            info(soup,file)
        done+=1
        print("Done:",str(done)+'/'+str(total))
    os.chdir(Parent)

scrap('business',4)
scrap('india',4)
scrap('world',4)




