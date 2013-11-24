#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import codecs


def dict_per_ad(dict_in):
    dict_out = dict_in.copy()
    for key in ["id","name"]:
        dict_out.pop(key,None)
    return dict_out
def merge_dicts(dict_list_id_sorted):
    output = []
    pre_dict_item = dict_list_id_sorted[0]
    same_id_term = [dict_per_ad(pre_dict_item)]
    for dict_item in dict_list_id_sorted[1:]:
        if dict_item["id"] == pre_dict_item["id"]:
            same_id_term.append(dict_per_ad(dict_item))
        else:
            output.append({"id": pre_dict_item["id"], "name": pre_dict_item["name"], "term": same_id_term})
            same_id_term = [dict_per_ad(dict_item)]
        pre_dict_item = dict_item
    return output

objs = json.load(open('npl_ly.json'))
dump_data = json.dumps(merge_dicts(sorted(objs, key=lambda d: d["id"])), sort_keys=True, indent=4, ensure_ascii=False)
print dump_data
convert_file = codecs.open('npl_ly(pretty_format).json', 'w', encoding='utf-8')
convert_file.write(dump_data)
convert_file.close()
