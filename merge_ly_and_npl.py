#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import codecs


def find_legislator_from_ly_info(name, term, ly_dict_list):
    possible = [legislator for legislator in ly_dict_list if legislator["ad"] == term["ad"] and legislator["name"] == name]
    if len(possible) == 1:
        return possible
    elif len(possible) == 0:
        print 'ly2npl can not find legislator at ad: ' + str(term["ad"]) + ' named: ' + name
    else:
        print 'ly2npl duplicate name: ' + name + ' at: ' + str(term["ad"])
        possible2one = [legislator for legislator in possible if legislator["party"] == term["party"] and legislator["gender"] == term["gender"]]
        if len(possible2one) == 1:
            return possible2one
        else:
            print 'ly2npl still can not find only one legislator from possible list!!'

def find_legislator_from_npl(ly_legislator, origin_npl_dict_list):
    possible = [legislator for legislator in origin_npl_dict_list if legislator["name"] == ly_legislator["name"] and legislator["ad"] == ly_legislator["ad"]]
    if len(possible) == 1:
        return possible
    elif len(possible) == 0:
        print 'npl2ly can not find legislator at ad: ' + str(ly_legislator["ad"]) + ' named: ' + ly_legislator["name"]
    else:
        print 'npl2ly duplicate name: ' + ly_legislator["name"] + ' at: ' + str(ly_legislator["ad"])
        possible2one = [legislator for legislator in possible if legislator["party"] == ly_legislator["party"] and legislator["gender"] == ly_legislator["gender"]]
        if len(possible2one) == 1:
            return possible2one
        else:
            print 'npl2ly still can not find only one legislator from possible list!!'

def complement(source, destination):
    source_fields = []
    destination_fields = []
    for key, value in term.items():
        if dict_item["id"] == pre_dict_item["id"]:
            same_id_term.append(dict_per_ad(dict_item))
        else:
            output.append({"id": pre_dict_item["id"], "name": pre_dict_item["name"], "each_term": same_id_term})
            same_id_term = [dict_per_ad(dict_item)]
        pre_dict_item = dict_item
    return term

ly_dict_list = json.load(open('ly_info.json'))
npl_dict_list = json.load(open('npl_ly(same_id_in_one_dict).json'))
origin_npl_dict_list = json.load(open('npl_ly.json'))
for npl_legislator in npl_dict_list:
    for term in npl_legislator["each_term"]:
        if term["ad"] != 1:
            ly_legislator = find_legislator_from_ly_info(npl_legislator["name"], term, ly_dict_list)
            #term = merge_into_npl(term, legislator_ly)

for ly_legislator in ly_dict_list:
    npl_legislator = find_legislator_from_npl(ly_legislator, origin_npl_dict_list)


#dump_data = json.dumps(merge_dicts(sorted(objs, key=lambda d: d["id"])), sort_keys=True)
#origin_file.write(dump_data)
#origin_file.close()
