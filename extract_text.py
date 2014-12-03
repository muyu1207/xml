__author__ = 'adm'

import xml.etree.ElementTree as ET
import codecs
tree = ET.parse('C:\\Users\\adm\\Downloads\\emissions_nat_10_INSERT_20_000_20140711-223513_0001.xml')
root = tree.getroot()
count = 0
with codecs.open("extracted.txt", "w", encoding='utf16') as out_file:
    for type_tag in root.iter('RES'):
        s = type_tag.text
        count += 1
        out_file.write(s)

print(count)