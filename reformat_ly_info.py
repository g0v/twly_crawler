# -*- coding: utf-8 -*
import json
import codecs

objs = json.load(open('ly_info.json'))
dump_data = json.dumps(objs, sort_keys=True, indent=4, ensure_ascii=False)
print dump_data
convert_file = codecs.open('ly_info(pretty_format).json', 'w', encoding='utf-8')
convert_file.write(dump_data)
convert_file.close()
