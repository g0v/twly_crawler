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


爬蟲流程
=======

如下圖所示, *scrapy* 這隻爬蟲程式依據 *ly_info_spider.py* 和 *npl_info_spider.py* 分別去
立法院全球資訊網和立法院國會圖書館抓立委的資料，分別產生 *ly_info.json* 和 *npl_info.json*
但這兩個檔案裡的中文都是未編碼的unicode，為了debug和後處理方便，各自有一隻reformat的程式
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
