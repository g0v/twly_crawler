#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import codecs

objs = json.load(open('npl_ly.json'))
dump_data = json.dumps(objs, sort_keys=True, indent=4, ensure_ascii=False)
print dump_data
convert_file = codecs.open('npl_ly(pretty_format).json', 'w', encoding='utf-8')
convert_file.write(dump_data)
convert_file.close()
