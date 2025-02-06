import os
import requests
import openpyxl
from bs4 import BeautifulSoup
url ="" # URL masked
titles = []
description = []
NormalPrice = []
img = []
for i in range (1,4): # loop through the first 3 pages
    url += str(i)
    page = requests.get(url)
    soup = BeautifulSoup(page.content , 'html.parser')
    products = soup.find_all('div', itemprop="itemListElement") # products container
    for product in products : # extract data for each product
        titles.append(product.find('div',class_="text-center").a.get_text(strip=True))
        description.append(product.find('a',itemprop="url").text)
        NormalPrice.append(product.find('span',class_="price").text)
        img.append(product.find('img')['src'])

# Directory to save the images
directory = "images"
os.makedirs(directory, exist_ok=True)

for i,url in enumerate(img):
    response = requests.get(url)
    imgext = url.split('.')[-1]
    imgname = f"{description[i]}.{imgext}"
    imgpath = os.path.join(directory, imgname)
    with open(imgpath, 'wb') as file:
        file.write(response.content)

xlsx_file = "products.xlsx"
workbook = openpyxl.Workbook()
sheet = workbook.active

headers = ['ID', 'Title', 'Description', 'Normal Price']
sheet.append(headers)

# Write data rows
for i in range(len(titles)):
    sheet.append([i + 1, titles[i], description[i], NormalPrice[i]])

workbook.save(xlsx_file)






