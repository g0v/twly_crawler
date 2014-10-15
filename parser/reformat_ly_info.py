#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import codecs


def check_term_start(dict_list):
    output = []
    pre_notnull_dict_item = ''
    for dict_item in dict_list:
        if not dict_item.has_key("term_start"):
            continue
        else:
            if pre_notnull_dict_item:
                if dict_item["term_start"] != pre_notnull_dict_item["term_start"]:
                    output.append((dict_item["ad"], dict_item["name"], dict_item["term_start"], dict_item["links"]["ly"]))
            pre_notnull_dict_item = dict_item
    return output

def write_file(data, file_name):
    file = codecs.open(file_name, 'w', encoding='utf-8')
    file.write(data)
    file.close()

objs = json.load(open('../data/ly_info.json'))
dump_data = json.dumps(objs, sort_keys=True, indent=4, ensure_ascii=False)
write_file(dump_data, '../data/pretty_format/ly_info.json')
empty_term_start = [(legislator["ad"], legislator["name"], legislator["links"]["ly"]) for legislator in objs if not legislator.has_key("term_start")]
dump_data = json.dumps(empty_term_start, sort_keys=True, indent=4, ensure_ascii=False)
write_file(dump_data, '../log/term_start_empty_on_lygovtw.json')
dump_data = json.dumps(check_term_start(objs), sort_keys=True, indent=4, ensure_ascii=False)
write_file(dump_data, '../log/term_start_need_check_on_lygovtw.json')
