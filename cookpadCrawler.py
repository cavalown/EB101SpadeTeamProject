import requests
from bs4 import BeautifulSoup
import pprint
import pandas as pd
import csv, random, time

### for macOS ###
import ssl
import os
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
#################

### Home page url ###
url = 'https://cookpad.com/tw'

### header ###
headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}

### form data ###
data_str = '''payload: aUkQRhAIEGJqABAeEFYQCEkQYmoLBBAIEFpGRkJBCB0dUV1dWUJTVhxRXV8dRkUQHhBiagQBEAgQf1NRe1xGV14QHhBiagoHAhAIAh4QYmoKBwMQCAMHBwUeEGJqAQUDEAhUU15BV09Pbw==
appId: PXFqtAw5et
tag: v5.3.7
uuid: 8813dcf0-807a-11ea-88fe-b923a739059a
ft: 140
seq: 0
en: NTA
pc: 6842615508289801
sid: 2cc95e90-8068-11ea-ab18-8b1efdbb12a6
vid: de5ea071-7ee7-11ea-9210-419bd9814cb7
pxhd: f7545dee48bd5ab51124a6771502ca60ab9843b85e5a90eab43d018c8b94abe5:de5ea071-7ee7-11ea-9210-419bd9814cb7'''
data = {each_data.split(': ')[0]:each_data.split(': ')[-1] for each_data in data_str.split('\n') }

with open('./cookpad.csv', 'w') as cp:
    writeCsv = csv.writer(cp)
    writeCsv.writerow(['食譜名稱', '食譜網址', '食譜食材', '圖片網址'])

while url != "https://cookpad.com":
    ### request Home page ###
    res = requests.get(url, headers=headers, data=data)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup.prettify())

    # p_text = Path('cookpadUrlRead.txt')
    # p_text.write_text(str(soup.prettify()))


    ### select every dishes list in a page ###
    dishList = soup.select('div[class="p-3 feed__body"]')
    for dish in dishList:
        # print(dish)
        # print('----------')
        try:
            ## -食譜名稱- ##
            dish_select_Name = dish.a.h2
            dishName = dish_select_Name.text.strip()
            print(dishName)
            print('--')

            ## -食譜網址- ##
            dish_url = 'https://cookpad.com' + dish.a["href"]
            print(dish_url)
            print('--')

            ### request dish content page ###
            res_dish = requests.get(dish_url, headers=headers, data=data)
            soup_dish = BeautifulSoup(res_dish.text, 'html.parser')
            #print(soup_dish.prettify())

            ## -食譜材料- ##
            dish_page = soup_dish.select('div[class="card card--borderless"]')
            for dish_content in dish_page:
                # print(dish_content)
                ingredient = dish_content.select('div[class="ingredient__details"]')
                all_ingredient = []
                for ingredientName in ingredient:
                    print(ingredientName.text.strip())
                    all_ingredient.append(ingredientName.text.strip())
                print(all_ingredient)
                print('----')

            ## -食譜照片- ##
            dish_pic = soup_dish.find(id="recipe_image").a["href"]
            dish_pic_url = "https://cookpad.com" + dish_pic
            print(dish_pic_url)
            print('----------------------')

            with open('./cookpad.csv', 'a') as cp:
                writeCsv = csv.writer(cp)
                writeCsv.writerow([dishName, dish_url, all_ingredient, dish_pic_url])

        except TypeError:
            print('"Here is TypeError"')

    url_link = soup.find(id="feed_pagination").a["href"]
    url = "https://cookpad.com" + url_link
    print('+++ Next page:', url)
    time.sleep(random.randint(2,5))
