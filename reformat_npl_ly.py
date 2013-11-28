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
    legislator_rename = []
    pre_dict_item = dict_list_id_sorted[0]
    same_id_term = [dict_per_ad(pre_dict_item)]
    for dict_item in dict_list_id_sorted[1:]:
        if dict_item["id"] == pre_dict_item["id"]:
            if dict_item["name"] != pre_dict_item["name"]:
               legislator_rename.append(pre_dict_item["name"])
            same_id_term.append(dict_per_ad(dict_item))
        else:
            if not legislator_rename:
                output.append({"id": pre_dict_item["id"], "name": pre_dict_item["name"], "each_term": same_id_term})
            else:
                output.append({"id": pre_dict_item["id"], "name": pre_dict_item["name"], "former_names": legislator_rename, "each_term": same_id_term})
                legislator_rename = []
            same_id_term = [dict_per_ad(dict_item)]
        pre_dict_item = dict_item
    return output

objs = json.load(open('npl_ly.json'))
dump_data = json.dumps(merge_dicts(sorted(objs, key=lambda d: d["id"])), sort_keys=True, indent=4, ensure_ascii=False)
convert_file = codecs.open('npl_ly(pretty_format).json', 'w', encoding='utf-8')
convert_file.write(dump_data)
convert_file.close()
origin_file = codecs.open('npl_ly(same_id_in_one_dict).json', 'w', encoding='utf-8')
dump_data = json.dumps(merge_dicts(sorted(objs, key=lambda d: d["id"])), sort_keys=True)
origin_file.write(dump_data)
origin_file.close()
