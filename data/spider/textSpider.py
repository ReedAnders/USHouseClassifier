# Run with $scrapy runspider textSpider.py

import scrapy
import json
import re
import unicodedata

from csv import DictReader, DictWriter

class BlogSpider(scrapy.Spider):
    name = 'seedspider'

    url_list = []
    train_list = list(DictReader(open("../train.csv", 'r')))
    for entry in train_list:
        url_list.append('https://www.congress.gov/bill/113th-congress/house-bill/' + entry['No.'] + '/text?format=txt')

    start_urls = url_list

    def __init__(self):
        self.seed_list = []

    def parse(self, response):
        yield scrapy.Request(response.url, self.parse_titles)

    def parse_titles(self, response):
        individual_dict = {}

        for billName in response.selector.xpath('//pre/text()').extract():
            billName = billName.strip()

            m = re.search('house-bill/(.+?)/text', response.url)
            if m:
                billNum = m.group(1)


            individual_dict[billNum] = billName   

        self.seed_list.append(individual_dict)
        self.dump_data()

    def dump_data(self):

        # Save combined dictionary as CSV
        # o = DictWriter(open("train.csv", 'w'), ["No.", "Label", "Text", "State", "Party", "NameFull"])
        # o.writeheader()
        # for BillNum in labels.keys():
        #     if billText[BillNum]:
        #         d = {'No.':BillNum , 'Label':labels[BillNum] , 'Text':billText[BillNum] , 'State':billState[BillNum] , 'Party':billParty[BillNum] , 'NameFull':billNameFull[BillNum]}
        #         o.writerow(d)
                
        with open('billText_data.json', 'wb') as fp:
            json.dump(self.seed_list, fp, indent=4, sort_keys=True, ensure_ascii=False)
            fp.close()

        