# -*- coding: utf-8 -*
import re
import codecs


def write_file(data, file_name):
    file = codecs.open(file_name, 'w', encoding='utf-8')
    file.write(data)
    file.close()

def normalize_name(person):
    person['name'] = re.sub(u'[。˙・•．.]', u'‧', person['name'])
    person['name'] = re.sub(u'[　\s()（）]', '', person['name'])
    person['name'] = person['name'].title()
