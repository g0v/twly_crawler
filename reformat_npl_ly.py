#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import codecs


def merge_dicts(dict_list_id_sorted):
    output = []
    pre_dict_item = dict_list_id_sorted[0]
    same_id_term = [{"ad": pre_dict_item["ad"], "in_office": pre_dict_item["in_office"]}]
    for dict_item in dict_list_id_sorted[1:]:
        if dict_item["id"] == pre_dict_item["id"]:
            same_id_term.append({"ad": dict_item["ad"], "in_office": dict_item["in_office"]})
        else:
            output.append({"id": pre_dict_item["id"], "name": pre_dict_item["name"], "term": same_id_term})
            same_id_term = [{"ad": dict_item["ad"], "in_office": dict_item["in_office"]}]
        pre_dict_item = dict_item
    return output

objs = json.load(open('npl_ly.json'))
dump_data = json.dumps(merge_dicts(sorted(objs, key=lambda d: d['id'])), sort_keys=True, indent=4, ensure_ascii=False)
print dump_data
convert_file = codecs.open('npl_ly(pretty_format).json', 'w', encoding='utf-8')
convert_file.write(dump_data)
convert_file.close()
