#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import codecs


def dict_per_ad(dict_in):
    dict_out = dict_in.copy()
    for key in ["uid", "former_names"]:
        dict_out.pop(key,None)
    return dict_out

def merge_dicts(dict_list_id_sorted):
    output = []
    legislator_rename = []
    pre_dict_item = dict_list_id_sorted[0]
    same_id_term = [dict_per_ad(pre_dict_item)]
    for dict_item in dict_list_id_sorted[1:]:
        if dict_item["uid"] == pre_dict_item["uid"]:
            if dict_item["name"] != pre_dict_item["name"]:
               legislator_rename.append(pre_dict_item["name"])
            same_id_term.append(dict_per_ad(dict_item))
        else:
            if legislator_rename:
                output.append({"uid": pre_dict_item["uid"], "name": pre_dict_item["name"], "former_names": legislator_rename, "each_term": same_id_term})
            else:
                output.append({"uid": pre_dict_item["uid"], "name": pre_dict_item["name"], "each_term": same_id_term})
            legislator_rename = []
            same_id_term = [dict_per_ad(dict_item)]
        pre_dict_item = dict_item
    if legislator_rename:
        output.append({"uid": pre_dict_item["uid"], "name": pre_dict_item["name"], "former_names": legislator_rename, "each_term": same_id_term})
    else:
        output.append({"uid": pre_dict_item["uid"], "name": pre_dict_item["name"], "each_term": same_id_term})
    return output

def write_file(data, file_name):
    file = codecs.open(file_name, 'w', encoding='utf-8')
    file.write(data)
    file.close()

objs = json.load(open('../data/npl_ly.json'))
dump_data = json.dumps(merge_dicts(sorted(objs, key=lambda d: d["uid"])), sort_keys=True, indent=4, ensure_ascii=False)
write_file(dump_data, '../data/pretty_format/npl_ly.json')
dump_data = json.dumps(merge_dicts(sorted(objs, key=lambda d: d["uid"])), sort_keys=True)
write_file(dump_data, '../data/npl_ly(same_id_in_one_dict).json')
