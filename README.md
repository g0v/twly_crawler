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
or              
scrapy crawl npl_ly -o npl_ly.json -t json        
        
After crawler finished, ly_info.json file will been create, if you want a pretty format:        
rm -f ly_info(pretty_format).json npl_ly(pretty_format).json      
python reformat_ly_info.py      
or              
python reformat_npl_ly.py      

資料來源
======
http://www.ly.gov.tw/

授權
======
http://twly.herokuapp.com/about/
