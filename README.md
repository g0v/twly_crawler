twly_crawler
==========

Crawler for http://twly.herokuapp.com/

環境
======
http://doc.scrapy.org/en/latest/intro/install.html      

使用方法
======
Enter a directory where you’d like to store these code and then run:        
rm -f ly_info.json npl_ly.json     
scrapy crawl ly_info -o ly_info.json -t json        
scrapy crawl npl_ly -o npl_ly.json -t json        
        
After crawler finished:        
python reformat_ly_info.py      
python reformat_npl_ly.py      
python merge_ly_and_npl.py      
        
merge.json is the final data, merge(pretty_format).json is it's pretty format in order to read easily.

File too large? Please see in below url:
http://g0v.github.io/twly_crawler/merged%28pretty_format%29.json
http://g0v.github.io/twly_crawler/merged.json

資料來源
======
http://www.ly.gov.tw/       
http://npl.ly.gov.tw/

授權
======
http://twly.herokuapp.com/about/