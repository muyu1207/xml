__author__ = 'yanina'
'''
Перед запуском скрипт и конфигурационный файл сложить в одну папку. В этой папке создать подпапку [files], куда сложить все xml-файлы, которые нужно обработать.
Запускать в командной строке:
имя_скрипта -c имя_конфигурационного_файла [параметры]

имя_конфигурационного_файла* – xml-файл, где прописаны теги, которые нужно переводить. Сейчас из него извлекаются только теги с transType = 2 (translate).
параметры (можно указывать только один параметр):
-t  извлечь текст из тега RES (сам текст программы) 
-n  извлечь текст из тега NOM (имена людей) 
-p  извлечь текст из тега LIEU (географические названия)
-o  извлечь текст из всех остальных тегов, которые перечислены в конфигурационном файле (то есть все, кроме RES, NOM, LIEU)
Если запускать без параметров, то извлечется текст из всех тегов, которые перечислены в конфигурационном файле с пометкой 2.
*Если запускать с параметрами -t, -n или -p, то указывать конфигурационный файл нет необходимости.
'''


import xml.etree.ElementTree as ET
import codecs
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-c', nargs = 1, dest = "config_file") #configuration file, where the tags that should be translated are listed
parser.add_argument('-t', action="store_true", dest = "extract_text") #extract only text in RES tag
parser.add_argument('-o', action="store_true", dest = "extract_other") #extract the text in other interesting tags (TI,TIEXT, TICOL, TI_OEUVRE, TYPE, NPRO, CH, LIB_SP, TERME, DESC_PRC, LIBELLE, INSERT)
parser.add_argument('-n', action="store_true", dest = "extract_names") #extract only names in NOM tag
parser.add_argument('-p', action="store_true", dest = "extract_places") #extract only places in LIEU tag
args = parser.parse_args()

tree = ET.parse(args.config_file[0])
root = tree.getroot()
all_tags_to_process = []

for conf in root.iter('config_item'):
    tag = conf.find('xpath').get('value').strip('/')
    translation_type = conf.find('transType').get('value')
    if translation_type == "2":
        all_tags_to_process.append(tag)

if args.extract_text:
    tags_to_process = ["RES"]
    file_name = "text_only"
elif args.extract_other:
    tags_to_process = list(all_tags_to_process)
    for i in ["RES", "NOM", "LIEU"]:
        if i in tags_to_process:
            tags_to_process.remove(i)
    file_name = "other"
elif args.extract_names:
    tags_to_process = ["NOM"]
    file_name = "names"
elif args.extract_places:
    tags_to_process = ["LIEU"]
    file_name = "places"
else:
    tags_to_process = all_tags_to_process
    file_name = "all_extracted"

with codecs.open(file_name + ".txt", "w", encoding='utf8') as out_file:
    for file in os.listdir('files'):
        tree = ET.parse('./files/' + file)
        root = tree.getroot()
        for tag in tags_to_process:
            for tag_to_proc in root.iter(tag):
                if tag_to_proc.text != None:
                    s = tag_to_proc.text + "\n"
                    out_file.write(s)

print("Finished")
