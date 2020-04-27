from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import newspaper
from newspaper import Article
import nltk
driver = webdriver.Chrome("C:/Users/DELL/Desktop/chromedriver.exe")

urls = []
titles = []
description = []
shares = []
keywords = []
publish_dates = []

driver.get("https://www.indiatimes.com/")
content = driver.page_source
soup = BeautifulSoup(content,features="lxml")

for url in soup.find_all('a',href=True,attrs={'caption'}):
    urls.append(url.get('href'))

for link in urls:
    driver.get(link)
    content = driver.page_source
    soup = BeautifulSoup(content,features="lxml")
    if soup.find_all('div',attrs={'class':'share share-top'}) == []:
        shares.append("0")
    else:
        for share in soup.find_all('div', attrs={'class':'share share-top'}):
            shares.append(share.text)
    article = Article(link)
    article.download()
    article.parse()
    article.nlp()
    titles.append(article.title)
    publish_dates.append(article.publish_date)
    description.append(article.text)

old_news = []
for i in range(1,101):
    link = "https://www.indiatimes.com/seoarchive/pg-1"
    link = link[:-1]+str(i)
    driver.get(link)
    content = driver.page_source
    soup = BeautifulSoup(content,features="lxml")
    for url in soup.find_all('a',href=True,attrs={'caption'}):
        old_news.append(url.get('href'))

for link in old_news:
    driver.get(link)
    content = driver.page_source
    soup = BeautifulSoup(content,features="lxml")
    if soup.find_all('div', attrs={'class':'share share-top'})==[]:
        shares.append("0")
    else:
        for share in soup.find_all('div',attrs={'class':'share share-top'}):
            shares.append(share)
    article = Article(link)
    article.download()
    article.parse()
    article.nlp()
    titles.append(article.title)
    description.append(article.text)
    publish_dates.append(article.publish_date)

news_data = pd.DataFrame({"Title":titles,"Description":description,"PublishDate":publish_dates,"Shares":shares})
news_data.to_csv("C:/Users/DELL/Desktop/news.csv",encoding='utf-8',index = False)
