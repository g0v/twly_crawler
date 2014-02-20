twly_crawler
==========

Crawler for [立委投票指南](http://vote.ly.g0v.tw/)

環境
======
http://doc.scrapy.org/en/latest/intro/install.html      

使用方法
======
Enter a directory where you’d like to store these code and then run:        
```
./crawl_all.sh
```
or
```
rm -f ly_info.json npl_ly.json     
scrapy crawl ly_info -o ly_info.json -t json        
scrapy crawl npl_ly -o npl_ly.json -t json        
```
        
After crawler finished:        
```
./merge_all.sh
```
or
```
python reformat_ly_info.py      
python reformat_npl_ly.py      
python merge_ly_and_npl.py      
```
        
merge.json is the final data, ./data(pretty_format)/merge.json is it's pretty format in order to read easily.

File too large? Please see in below url:        
[pretty version](http://g0v.github.io/twly_crawler/merged%28pretty_format%29.json)      
[origin version](http://g0v.github.io/twly_crawler/merged.json)

資料來源
======
[立法院全球資訊網](http://www.ly.gov.tw/)       
[立法院國會圖書館](http://npl.ly.gov.tw/)

CC0 1.0 Universal
=================
CC0 1.0 Universal       
This work is published from Taiwan.     
[about](http://vote.ly.g0v.tw/about/)
