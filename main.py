from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


#creates a url with the search term passed to it.
def geturl(searchTerm):
    template='https://www.amazon.com/s?k={}&crid=1CYT66YKRZMRU&sprefix=moisturize%2Caps%2C325&ref=nb_sb_noss_2'
    searchTerm = searchTerm.replace(' ','+')
    url = template.format(searchTerm)
    url += '&page={}'
    return url

#takes html code for an item in the search and gets all the information about it.
def getInfo(result):
    # get the name of the item
    atag = result.h2.a
    name = atag.text.strip()

    # get the url to the item
    url = 'https://amazon.com' + atag.get('href')
    try:
        # get the price of the item
        priceParent = result.find('span', 'a-price')
        price = priceParent.find('span', 'a-offscreen').text
    except AttributeError:
        return


    try:
        rating = result.i.text

        reviewCountParent = result.find('div', 'a-row a-size-small')
        reviewCount = reviewCountParent.find('span', 'a-size-base s-underline-text').text
    except AttributeError:
        rating = ''
        reviewCount = ''
    #print(item)
    #print(url)
    #print(price)
    #print(rating)
    #print(reviewCount)

    toReturn = (name, url, price, rating, reviewCount)
    return toReturn

#logoc of the program
def main():
    searchTerm = input("What would you like to scrape Amazon for? ")
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    url = geturl(searchTerm)
    total = []


    for page in range (1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for result in results:
            returned = getInfo(result)
            if returned:
                total.append(returned)

    driver.quit()
    fileName = searchTerm + ' Results.csv'
    with open(fileName, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'URL', 'Price', 'Rating', 'Review Count'])
        writer.writerows(total)
if(__name__  == '__main__'):
    main()


