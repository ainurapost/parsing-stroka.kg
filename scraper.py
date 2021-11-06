# scraper.py
import requests
from bs4 import BeautifulSoup
import xlsxwriter



url = 'https://stroka.kg/kupit-kvartiru/?topic_rooms[]=1&topic_rooms[]=2&q&order=cost&cost_min&cost_max'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

prices = soup.find_all('td', class_='topics-item-topic_cost topics-item-td')
roomsNumber = soup.find_all('td', class_='topics-item-td topics-item-topic_rooms')
types = soup.find_all('td', class_='topics-item-topic_series topics-item-td')
squares = soup.find_all('td', class_='topics-item-topic_area topics-item-td')
description = soup.find_all('a', class_='topics-item-view')
items = soup.find_all('tr', class_='topics-item-tr topics-item-tr-title')

# for n, i in enumerate(items, start=1):
#     itemPrice = i.find('td', class_='topics-item-topic_cost topics-item-td').text
#     itemRoomsNumber = i.find('td', class_='topics-item-td topics-item-topic_rooms').text
#     itemType = soup.find('td', class_='topics-item-topic_series topics-item-td').text
#     itemSquares = i.find('td', class_='topics-item-topic_area topics-item-td').text
#     itemDescription = i.find('a', class_='topics-item-view').text
#
#     print(f'{n}:  {itemPrice} за {itemRoomsNumber} - комнатную квартиру типа {itemType}, '
#           f'площадью {itemSquares}, {itemDescription}  ')


# for n, i in enumerate(roomsNumber, start=1):
#     print(f'{n}, (i')
# print(f'{n}, {prices[i].text}, {roomsNumber[i].text}, {types[i].text},'
#       f'{squares[i].text}, {description[i].text}')

pages = soup.find('div', class_='paginator clearfix')
urls = []
links = pages.find_all('a', class_='paginator-item')

for link in links:
    pageNum = int(link.text) if link.text.isdigit() else None
    if pageNum != None:
        hrefval = link.get('href')
        urls.append(hrefval)
# print(urls)


workbook = xlsxwriter.Workbook('ParsingResults.xlsx')
worksheet = workbook.add_worksheet()

for j in range(0,15):
    newUrl = f'https://stroka.kg/kupit-kvartiru/?topic_rooms%5B0%5D=1&topic_rooms%5B1%5D=2&q=&order=cost&cost_min=&cost_max=&p={j}#paginator'
    response = requests.get(newUrl)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('tr', class_='topics-item-tr topics-item-tr-title')
    for n, i in enumerate(items, start=1):
        k=180*j+n
        worksheet.write(f'A{k}', k)
        itemPrice = i.find('td', class_='topics-item-topic_cost topics-item-td').text
        worksheet.write(f'B{k}', itemPrice)
        itemRoomsNumber = i.find('td', class_='topics-item-td topics-item-topic_rooms').text
        worksheet.write(f'C{k}', itemRoomsNumber)
        itemType = soup.find('td', class_='topics-item-topic_series topics-item-td').text
        worksheet.write(f'D{k}', itemType)
        itemSquares = i.find('td', class_='topics-item-topic_area topics-item-td').text
        worksheet.write(f'E{k}', itemSquares)
        itemDescription = i.find('a', class_='topics-item-view').text
        worksheet.write(f'F{k}', itemDescription)



        # print(f'{j}-{n}:  {itemPrice} за {itemRoomsNumber} - комнатную квартиру типа {itemType}, '
        #       f'площадью {itemSquares}, {itemDescription}  ')



workbook.close()