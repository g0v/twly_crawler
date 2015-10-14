#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import common


objs = json.load(open('../data/ly_info.json'))
for ly_legislator in objs:
    common.normalize_name(ly_legislator)
dump_data = json.dumps(objs, sort_keys=True, ensure_ascii=False)
common.write_file(dump_data, '../data/ly_info.json')
dump_data = json.dumps(objs, sort_keys=True, indent=4, ensure_ascii=False)
common.write_file(dump_data, '../data/pretty_format/ly_info.json')
empty_term_start = [(legislator["ad"], legislator["name"], legislator["links"]["ly"]) for legislator in objs if not legislator.has_key("term_start")]
dump_data = json.dumps(empty_term_start, sort_keys=True, indent=4, ensure_ascii=False)
common.write_file(dump_data, '../log/term_start_empty_on_lygovtw.json')
