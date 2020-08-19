# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup
import json
import csv


class RightmoveScraper:
    results = []
    
    def fetch(self, url): # method to acess URL 
        print('HTTP GET request to URL: %s' % url, end ='')
        response = requests.get(url)
        print('| Status code: %s' % response.status_code)
        return response
    
    def parse(self, html): # taking the data from the HTML and restructing for a CSV file 
        # print(html) just to check that you file can be read to python console
        content = BeautifulSoup(html,'lxml')
        title = [title.text.strip() for title in content.findAll('h2',{'class':'propertyCard-title'})]
        address = [address['content'].strip('\n') for address in content.findAll('meta', {'itemprop':'streetAddress'})]
        description = [description.text for description in content.findAll('span', {'data-test':'property-description'})] 
        prices = [price.text.strip() for price in content.findAll('div',{'class':'propertyCard-priceValue'})]
        dates = [date.text for date in content.findAll('span',{'class':'propertyCard-branchSummary-addedOrReduced'})]  
        # while ("" in dates_added_or_reduced):
        #     dates_added_or_reduced.remove('')
        # dates = [num.split()[-1] for num in dates_added_or_reduced]
        # any data without a dates have been omitted 
        seller = [seller.text.split('by')[-1].strip() for seller in content.findAll('span', {'class': 'propertyCard-branchSummary-branchName'})] 
        images = [image['src'] for image in content.findAll('img', {'itemprop':'image'})]    
        # list the element from the pages of the properties whilst removing all unnecessary information and spaces
        #print(dates) # can print the output for any of the above to check that the code works
        for index in range(0, len(dates)):
            # iterate through each of the information block on a page len(amount of blocks of information)
            self.results.append({
                'Property': title[index],
                'Address': address[index],
                'Description': description[index],
                'Price': prices[index],
                'Date Posted': dates[index],
                'Seller': seller[index],
                'Image':  images[index],
            })
            #print(json.dumps(item, indent=2))
        
    def to_csv(self): # write webpage data to csv file
        with open('rightmove2.csv', 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
            
            for row in self.results:
                writer.writerow(row)
            
            print('Stored results to "rightmove.csv"') # debugging info 
            
            
    def run(self):
        # removing data from a webpage an putting on another web page.
        # response = self.fetch('https://www.rightmove.co.uk/property-for-sale/luton.html')
        # with open('res.html', 'w', encoding='utf-8') as html_file:
        #     html_file.write(response.text)
        # html = ''
        # with open('res.html', 'r', encoding='utf-8') as html_file:
        #     for line in html_file:
        #         html += html_file.read() 
        for page in range (0, 13):
            index = page*24
            url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22%7DfjzHa%7CW%7B~%40hnc%40%7B~%40%7C%7D%5BgiDrpd%40d~Jt_N~%60q%40rqGvjFhg%60%40kw%5B~sHk_S~lE%7B%7DRivIuqS%3FqqM_iR%7DfJsmTcsCu_Njx%5Co_uB%3F%7Dp_B~%7BVihCb~PhrVxtS%7Cre%40j_E~hRute%40r%7BZ%22%7D&minBedrooms=3&maxPrice=300000&radius=1.0&index='+ str(index) +'&propertyTypes=detached%2Csemi-detached%2Cbungalow%2Cland&mustHave=garden%2Cparking&dontShow=sharedOwnership%2Cretirement&furnishTypes=&keywords='
            # url = ('https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E1244&minBedrooms=3&maxPrice=300000&radius=15.0&index=' + str(index) + '&propertyTypes=bungalow%2Cdetached%2Cland%2Cpark-home%2Csemi-detached&includeSSTC=false&mustHave=garden%2Cparking&dontShow=retirement%2CsharedOwnership&furnishTypes=&keywords=')
            # print(url) # debugging to check if it is the right amount of page that you want 
            response = self.fetch(url)
            self.parse(response.text)
        
        self.to_csv()
    
if __name__ == '__main__': # driver to run scraper 
    scraper = RightmoveScraper()
    scraper.run()