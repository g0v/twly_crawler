twly_crawler
==========

Crawler for [立委投票指南](http://vote.ly.g0v.tw/)

Change Log
======
1. 2015-10-13: 發現國會圖書館改版, change related npl_ly crawler
2. 2016-06-14: 國會圖書館 not provide unique id for legislator anymore, change crawler/parser which ad >= 9, manage unique id ourself at [twly_fileHandler](https://github.com/thewayiam/twly_fileHandler)

環境
======
http://doc.scrapy.org/en/latest/intro/install.html      

使用方法
======
Enter a directory where you’d like to store these code and then run:        
```
crawler$ ./crawl_all.sh      
```
or
```
rm -f data/ly_info.json data/npl_ly.json     
crawler$ scrapy crawl ly_info -o ../data/ly_info.json -t json        
crawler$ scrapy crawl npl_ly -o ../data/npl_ly.json -t json        
```
or specific ad
```
rm -f data/9/
crawler$ scrapy crawl ly_info -a ad=9 -o ../data/9/ly_info.json -t json        
crawler$ scrapy crawl npl_ly -a ad=9 -o ../data/9/npl_ly.json -t json        
```
        
After crawler finished:        
```
parser$ ./merge_all.sh
```
or
```
parser$ python reformat_ly_info.py      
parser$ python reformat_npl_ly.py      
parser$ python merge_ly_and_npl.py      
```
or specific ad, e.g.
```
parser$ python merge_ly_and_npl_one_ad.py --ad 9      
```
        
merge.json is the final data, ./data(pretty_format)/merge.json is it's pretty format in order to read easily.

資料來源
======
[立法院全球資訊網](http://www.ly.gov.tw/)       
[立法院國會圖書館](http://npl.ly.gov.tw/)

爬蟲流程
=======

如下圖所示, *scrapy* 這隻爬蟲程式依據 *ly_info_spider.py* 和 *npl_info_spider.py* 分別去
立法院全球資訊網和立法院國會圖書館抓立委的資料，分別產生 *ly_info.json* 和 *npl_info.json*
但這兩個檔案裡的內容需要互補，各自有一隻reformat的程式
，分別再產生一些中繼檔。最後再經由 *merge_ly_and_npl.py* 合併產生最終結果 *merged.json*
，作為 *twly_fileHandler* 的輸入檔


```
          +-----------------------+                    +----------------------+
          |ly_info_spider.py      |                    |  npl_info_spider.py  |
          +-----------------------+                    +----------------------+
                       +                                         +
                       |                                         |
                       |                                         |
                       |                                         |
                       +--------->     scrapy   <----------------+
                                         +
          +-----------------+            |             +-----------------+
          |   ly_info.json  |  <---------+-------->    |npl_info.json    |
          +-----------------+                          +-----------------+
                   +                                            +
                   |                                            |
                   |                                            v
                   v
             reformat_ly.py                               reformat_npl.py
                   +                                            +
                   |                                            |
                   v                                            v
   +-------------------------------------+             +--------------------------------------+
   |data/(pretty_format)/ly_info.json  -> for debug    |data/(pretty_format)/npl_ly.json -> for debug
   |                                     |             |npl_ly(same_id_in_one_dict).json      |
   |-->for check                         |             |                                      |
   |log/term_start_empty_on_lygovtw.json |             |                                      |
   |log/term_start_need_check_on_lygovtw.json          |                                      |
   +-------------------------------------+             +--------------------------------------+
                                                +
                                                |
                                                v
                           +----------------------------------+
                           |ly_info.json                      |
                           |npl_info.jsno                     |
                           |npl_ly(same_id_in_one_dict).json  |
                           |util.json                         |
                           |constituency_8_mapped.json        |
                           +----------------------------------+
                                                +
                                                v
                                merge_ly_and_npl.py

                                                +
                                                |
                                                v

                           +----------------------------------+
                           |merged.json -> final data for filehandler
                           |log/conflict.txt                  |
                           |                                  |
                           |                                  |
                           +----------------------------------+
```


CC0 1.0 Universal
=================
CC0 1.0 Universal       
This work is published from Taiwan.     
[about](http://vote.ly.g0v.tw/about/)
