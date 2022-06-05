from ctypes.wintypes import PINT
import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract(page):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'}
    url = f'https://in.indeed.com/jobs?q=software%20developer&start={page}&vjk=352353f699137e8f'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_="cardOutline")
    for items in divs:
        title = items.find('a').text.strip()
        comapany = items.find('span', class_='companyName').text.strip()
        try:
            salary = items.find(
                'div', class_='metadata salary-snippet-container').text.strip()
        except:
            salary = ' '

        summary = items.find(
            'div', class_='job-snippet').text.strip().replace('\n', "")

        job = {
            'title': title,
            'company': comapany,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)
    return


joblist = []
for i in range(0, 41, 10):
    print(f'Getting entries, {i}-{i+10}...')
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)
# print(df.head())
df.to_csv('jobs1.csv')
# print(joblist)
