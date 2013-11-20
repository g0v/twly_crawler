twly_crawler
==========

Crawler for http://twly.herokuapp.com/

使用方法
======
Enter a directory where you’d like to store these code and then run:
rm -f ly_info.json
scrapy crawl ly_info -o ly_info.json -t json

After crawler finished, ly_info.json file will been create, if you want a pretty format:
rm -f ly_info(pretty_format).json
python reformat_ly_info.py

資料來源
======
http://www.ly.gov.tw/

授權
======
http://twly.herokuapp.com/about/
