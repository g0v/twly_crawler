#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import codecs


json_orgi = json.load(open('constituency_8.json'))
json_out = json_orgi.copy()
for key, value in json_orgi.items():
    county, district, village = [], [], []
    for raw in value:
        county.append(raw.split(',')[:1])
        district.append(raw.split(',')[1:2])
        village.append(raw.split(',')[2:3])
    data = {
        "county": list(set([x[0] for x in county if len(x) != 0])),
        "district": list(set([x[0] for x in district if len(x) != 0])),
        "village": list(set([x[0] for x in village if len(x) != 0]))
    }
    json_out.update({"%s" % key: data})
output_file = codecs.open('constituency_8_maped.json', 'w', encoding='utf-8')
dump_data = json.dumps(json_out, sort_keys=True, indent=4, ensure_ascii=False)
output_file.write(dump_data)
output_file.close()
