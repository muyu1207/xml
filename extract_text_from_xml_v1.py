__author__ = 'adm'

import xml.etree.ElementTree as ET
import codecs
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', nargs = "+", dest = "files") #list of files to process
parser.add_argument('-t', action="store_true", dest = "extract_text") #extract only text in RES tag
parser.add_argument('-o', action="store_true", dest = "extract_other") #extract the text in other interesting tags (TI,TIEXT, TICOL, TI_OEUVRE, TYPE, NPRO, CH, LIB_SP, TERME, DESC_PRC, LIBELLE, INSERT)
parser.add_argument('-n', action="store_true", dest = "extract_names") #extract only names in NOM tag
parser.add_argument('-p', action="store_true", dest = "extract_places") #extract only places in LIEU tag
parser.add_argument('-q', action="store_true", dest = "extract_translated_items") #extract only tags that have translation (TICORP = TICORPANG, TICORPMAJ = TICORPMAJANG)
#args = parser.parse_args()
args = parser.parse_args("-f extraits_reg_10_INSERT_12_000_20140725-234239_0001.xml test.xml -n".split())

# names = NOM
# professions = ROLE_GENERIQUE
# places = LIEU
# TICORP = TICORPANG
# TICORPMAJ = TICORPMAJANG

if args.extract_text:
    tags_to_process = ["RES"]
    file_name = "text_only"
elif args.extract_other:
    tags_to_process = ["TI","TIEXT", "TICOL", "TI_OEUVRE", "TYPE", "NPRO", "CH", "LIB_SP", "TERME", "DESC_PRC",
                       "LIBELLE", "INSERT", "FONDS","ROLE_GENERIQUE"]
    file_name = "other"
elif args.extract_names:
    tags_to_process = ["NOM"]
    file_name = "names"
elif args.extract_places:
    tags_to_process = ["LIEU"]
    file_name = "places"
elif args.extract_translated_items:
    source_tags = ["TICORP"]
    translation_tags = ["TICORPANG"]
    file_name = "translated_items"
else:
    tags_to_process = ["RES","TI","TIEXT", "TICOL", "TI_OEUVRE", "TYPE", "NPRO", "CH", "LIB_SP", "TERME", "DESC_PRC",
                       "LIBELLE", "NOM", "LIEU", "TICORP", "TICORPANG", "ROLE_GENERIQUE"]
    file_name = "all_extracted"

with codecs.open(file_name + ".txt", "w", encoding='utf8') as out_file:
    if not args.extract_translated_items:
        for file in args.files:
            tree = ET.parse(file)
            root = tree.getroot()
            for tag in tags_to_process:
                for tag_to_proc in root.iter(tag):
                    s = tag_to_proc.text + "\n"
                    print(s)
                    out_file.write(s)
    else:
        for file in args.files:
            tree = ET.parse(file)
            root = tree.getroot()
            sources = []
            translations = []
            for i, source_tag in enumerate(source_tags):
                for tag_to_proc in root.iter(source_tag):
                    sources.append(tag_to_proc.text)
                for tag_to_proc in root.iter(translation_tags[i]):
                    translations.append(tag_to_proc.text)
            if len(sources) == len(translations):
                for i, source in enumerate(sources):
                    source_translation = source + "\t" + translations[i] + "\n"
                    out_file.write(source_translation)
            else:
                print("Error: number of sources and number of translations are not equal")

print("Finished")



