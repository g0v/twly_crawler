#!/bin/bash
rm -f ../data/ly_info.json ../data/npl_ly.json     
scrapy crawl ly_info -o ../data/ly_info.json -t json        
scrapy crawl npl_ly -o ../data/npl_ly.json -t json  
