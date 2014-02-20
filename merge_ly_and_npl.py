#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import codecs


def find_legislator_from_ly_info(names, term, ly_dict_list):
    possible = [legislator for legislator in ly_dict_list if legislator["ad"] == term["ad"] and legislator["name"].replace(u'．', u'.') in names]
    if len(possible) == 1:
        return possible[0]
    elif len(possible) == 0:
        print 'ly2npl can not find legislator at ad: %s name in: %s' % (str(term["ad"]), names[0])
    else:
        print 'ly2npl duplicate name in: %s at ad: %s' % (names[:], str(term["ad"]))
        possible2one = [legislator for legislator in possible if legislator["party"] == term["party"] and legislator["gender"] == term["gender"]]
        if len(possible2one) == 1:
            return possible2one[0]
        else:
            print 'ly2npl still can not find only one legislator from possible list!!'

def find_legislator_from_npl(ly_legislator, origin_npl_dict_list):
    possible = [legislator for legislator in origin_npl_dict_list if legislator["name"] == ly_legislator["name"].replace(u'．', u'.') and legislator["ad"] == ly_legislator["ad"]]
    if len(possible) == 1:
        return possible[0]
    elif len(possible) == 0:
        print 'npl2ly can not find legislator at ad: ' + str(ly_legislator["ad"]) + ' named: ' + ly_legislator["name"]
    else:
        print 'npl2ly duplicate name: ' + ly_legislator["name"] + ' at: ' + str(ly_legislator["ad"])
        possible2one = [legislator for legislator in possible if legislator["party"] == ly_legislator["party"] and legislator["gender"] == ly_legislator["gender"]]
        if len(possible2one) == 1:
            return possible2one[0]
        else:
            print 'npl2ly still can not find only one legislator from possible list!!'

def complement(addition, base):
    pairs = [(key, value) for key, value in addition.items() if not base.has_key(key)]
    base.update(pairs)
    base["constituency"]=addition["constituency"]
    return base

def conflict(compare, base, f):
    for key in ["gender", "party", "in_office",]:
        if compare.has_key(key) and base.has_key(key):
            if compare[key] != base[key]:
                f.write('key, %s, (ly.gov.tw), %s, (npl), %s, uid, %s, ad, %s, name, %s, links, %s\n' % (key, compare[key], base[key], base["uid"], base["ad"], base["name"], compare["links"]["ly"]))
        else:
            f.write('can not find key: %s\n' % key)

ly_dict_list = json.load(open('ly_info.json'))
npl_dict_list = json.load(open('npl_ly(same_id_in_one_dict).json'))
origin_npl_dict_list = json.load(open('npl_ly.json'))
for npl_legislator in npl_dict_list:
    names_list = [npl_legislator["name"]]
    for name in npl_legislator.get("former_names", []):
        names_list.append(name)
    for term in npl_legislator["each_term"]:
        if term["ad"] != 1:
            ly_legislator = find_legislator_from_ly_info(names_list, term, ly_dict_list)
            if ly_legislator:
                term = complement(ly_legislator, term)
# --> cross check data conflict
f = codecs.open('./log/conflict.txt','w', encoding='utf-8')
for ly_legislator in ly_dict_list:
    npl_legislator = find_legislator_from_npl(ly_legislator, origin_npl_dict_list)
    if npl_legislator:
        conflict(ly_legislator, npl_legislator, f)
f.close()
# <-- end

output_file = codecs.open('merged.json', 'w', encoding='utf-8')
dump_data = json.dumps(npl_dict_list, sort_keys=True)
output_file.write(dump_data)
output_file.close()
output_pretty_file = codecs.open('./data(pretty_format)/merged.json', 'w', encoding='utf-8')
dump_data = json.dumps(npl_dict_list, sort_keys=True, indent=4, ensure_ascii=False)
output_pretty_file.write(dump_data)
output_pretty_file.close()
