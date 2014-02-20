#!/bin/bash
rm -f ly_info.json npl_ly.json     
scrapy crawl ly_info -o ly_info.json -t json        
scrapy crawl npl_ly -o npl_ly.json -t json  
