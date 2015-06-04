# -*- coding: utf-8 -*-

import json
import codecs
import os
import sys
from dateutil.parser import parse


# save the json file into xml type
STR = '''<doc id="%s">
<meta-info>
    <tag name="host">%s</tag>
    <tag name="date">%s</tag>
    <tag name="url">%s</tag>
    <tag name="title">%s</tag>
    <tag name="source-encoding">%s</tag>
</meta-info>
<text>
    %s
</text>
</doc>
'''


def change2XML(inname, outfile):
    news_file = open(inname, 'r')
    js = json.load(news_file)
    newid = js["date"]+"-"+js["newsId"]
    source = js["source"]
    date = parse(js["date"]).date()
    link = js["contents"]["link"]
    title = unicode(js["contents"]["title"])
    passage = unicode(js["contents"]["passage"])
    outfile.write(STR % (newid, source, date, link, title, "UTF-8", passage))


def changeFiles(dirname, outname):
    names = os.listdir(dirname)
    outfile = codecs.open(outname, "w", "utf-8")
    for name in names:
        inname = dirname + os.sep + name
        change2XML(inname, outfile)
    print("total %d file(s) save into %s" % (len(names), outname))
    outfile.close()

def changeDir(indirname, outdirname):
    '''
    比如：
    默认保存路径如下
    docs/
        news.163.com/
            20150529/
                2244534.json

    :param indirname: json保存文件根目录
    :param outdirname: 输出文件根目录
    :return:
    '''
    if not os.path.exists(outdirname):
        os.makedirs(outdirname)
    names = os.listdir(indirname)
    for news_name in names:
        print(news_name)
        dir_path = indirname + os.sep + news_name
        if os.path.isdir(dir_path):
            time_names = os.listdir(dir_path)
            for time_name in time_names:
                dir_path2 = indirname + os.sep + news_name + os.sep + time_name
                if os.path.isdir(dir_path2):
                    outname = outdirname + os.sep + news_name + "." + time_name + ".xml"
                    changeFiles(dir_path2, outname)



if __name__ == "__main__":
    #changeDir("docs/", "outdir")
    if len(sys.argv) != 3:
        print("Usage:\n python save2xml.py indirname outdirname")
        exit(0)
    indirname = sys.argv[1]
    outdirname = sys.argv[2]
    print("saving into dir %s " % outdirname)
    changeDir(indirname, outdirname)

