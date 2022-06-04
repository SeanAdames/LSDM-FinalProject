from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
baseurl = 'https://www.wholefoodsmarket.com'
requester = requests.get('https://www.wholefoodsmarket.com/products/all-products')
soup = bs(requester.content, 'html.parser')
list_ = soup.find_all('div', class_='w-pie--product-tile')
links = []

for item in list_:
    for link in item.find_all('a', href=True):
        links.append(baseurl + link['href'])

Product_name = []
Ingredients = []
Allergen_or_not = []
for Product_list in links:
    requester = requests.get(Product_list)
    soup = bs(requester.content, 'html.parser')
    name = soup.find('h1', class_='w-cms--font-headline__serif').text.strip()
    ingredients = soup.find('div', class_='w-cms--font-body__sans')
    allergen = soup.find('div', class_='w-cms--font-body__sans')

    try:
        ingredients = ingredients.find('p').text.strip()

    except:
        ingredients = 'No results'

    try:
        allergen = allergen.find_all('p')[1].text.strip()
    except:
        allergen = 'No allergen'

    Product_name.append(name)
    Ingredients.append(ingredients)
    Allergen_or_not.append(allergen)

df = pd.DataFrame(list(zip(Product_name, Ingredients, Allergen_or_not)), columns=['Name', 'ingredients', 'allergen'])
print (df)