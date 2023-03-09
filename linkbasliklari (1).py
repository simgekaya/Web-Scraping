import requests
from bs4 import BeautifulSoup
import csv
import os

url = 'http://www.tk.org.tr/index.php/tk/issue/archive'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

h4s = soup.find_all('h4')

links = []
for h4 in h4s:
    link_tags = h4.find_all('a')
    for link in link_tags:
        link_ciltsayi = link.text.strip()
        link_url = link.get('href')
        link_response = requests.get(link_url)
        link_soup = BeautifulSoup(link_response.content, 'html.parser')
        link_makale = [td.text.strip() for td in link_soup.find_all('td', {'class': 'tocTitle'})]
        link_yazar = [td.text.strip() for td in link_soup.find_all('td', {'class': 'tocAuthors'})]
        link_sayfa = [td.text.strip() for td in link_soup.find_all('td', {'class': 'tocPages'})]
        #link_detay = [td.text.strip() for td in link_soup.find_all('td', {'class': 'tocGalleys'})]
        #link_detay = [td.text.strip() for td in link_soup.find_all('td', {'class': 'tocGalleys'})]
        link_detay = [link.get('href') for link in link_soup.find_all('a', {'class': 'file'})]
        print([link.get('href') for link in link_soup.find_all('a', {'class': 'file'})])
        response=requests.get(link_detay)
        soup = BeautifulSoup(response.content, 'html.parser')
        aS=soup.find_all('a')
        for a in aS:
            link_tags=a.find_all('a')
            for link in link_tags:
                link_detay=[link_soup.find_all('a', {'id': 'pdfDownloadLink'})]
        links.append({'CiltSayi': link_ciltsayi, 'Makale': link_makale, 'Yazar':link_yazar, 'Sayfa':link_sayfa, 'PDF':link_url, 'DetayLinki':link_detay})

with open('turkkutuphaneciligideneme.csv', mode='w') as file:
    writer = csv.DictWriter(file, fieldnames=['CiltSayi','Makale', 'Yazar','Sayfa','PDF','DetayLinki'])
    writer.writeheader()
    for link in links:
        writer.writerow(link)

with open('turkkutuphaneciligideneme.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        url = row['PDF']
        filename = os.path.basename(url)
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        