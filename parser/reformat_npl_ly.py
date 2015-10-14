#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import common


def dict_per_ad(dict_in):
    dict_out = dict_in.copy()
    for key in ["uid", "former_names"]:
        dict_out.pop(key, None)
    return dict_out

def merge_dicts(dict_list_id_sorted):
    output = []
    pre_dict_item = dict_list_id_sorted[0]
    same_id_term = [dict_per_ad(pre_dict_item)]
    for dict_item in dict_list_id_sorted[1:]:
        if dict_item["uid"] == pre_dict_item["uid"]:
            same_id_term.append(dict_per_ad(dict_item))
        else:
            output.append({"uid": pre_dict_item["uid"], "name": pre_dict_item["name"], "former_names": pre_dict_item["former_names"], "each_term": same_id_term})
            same_id_term = [dict_per_ad(dict_item)]
        pre_dict_item = dict_item
    output.append({"uid": pre_dict_item["uid"], "name": pre_dict_item["name"], "former_names": pre_dict_item["former_names"], "each_term": same_id_term})
    return output

objs = json.load(open('../data/npl_ly.json'))
for npl_legislator in objs:
    common.normalize_name(npl_legislator)
    if not npl_legislator.get('elected_party'):
        npl_legislator['elected_party'] = npl_legislator['party']
dump_data = json.dumps(objs, sort_keys=True, ensure_ascii=False)
common.write_file(dump_data, '../data/npl_ly.json')
dump_data = json.dumps(objs, sort_keys=True, indent=4, ensure_ascii=False)
common.write_file(dump_data, '../data/pretty_format/npl_ly.json')
merged_npl = merge_dicts(sorted(objs, key=lambda d: [d["uid"], d['ad']]))
dump_data = json.dumps(merged_npl, sort_keys=True, indent=4, ensure_ascii=False)
common.write_file(dump_data, '../data/pretty_format/npl_ly(same_id_in_one_dict).json')
dump_data = json.dumps(merged_npl, sort_keys=True)
common.write_file(dump_data, '../data/npl_ly(same_id_in_one_dict).json')
