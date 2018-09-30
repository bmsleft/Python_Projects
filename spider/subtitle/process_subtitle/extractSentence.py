#-*- coding:utf-8 -*-

import os
import chardet
import re
import shutil


outBasePath = '/Users/bms/workspace/download/'


pattern_cn = re.compile(ur"([\u4e00-\u9FA5]+)")
pattern_jp1 = re.compile(ur"([\u3040-\u309F]+)")
pattern_jp2 = re.compile(ur"([\u30A0-\u30FF]+)")

pattern_illegals = [re.compile(ur"([\u00C0-\u2000]+)"),
                    re.compile(ur"([\u2240-\u2E70]+)"),
                    re.compile(ur"([\uE000-\uF8FF]+)")
                    ]
filters = ["字幕", "时间轴:", "校对:", "翻译:", "后期:", \
           "监制:", "禁止用作任何商业盈利行为", "http", "前情提要"\
           ]
regex_htmltag = re.compile(r'<[^>]+>', re.S)
regex_brace = re.compile(r'\{.*\}', re.S)
regex_slash = re.compile(r'\\\w', re.S)
regex_repeat = re.compile(r'[-=]{10}', re.S)


def process_sentence(sentence):
    gb_content = ''
    try:
        gb_content = sentence.decode('utf-8')
    except:
        # print "decpde error!"
        return ''

    for pattern_illegal in pattern_illegals:
        match_illegal = pattern_illegal.findall(gb_content)
        if len(match_illegal) > 0 :
            # print "illegal match : ", sentence
            return ''

    for filter in filters:
        try:
            sentence.index(filter)
            # print "filter keywors of ", filter
            return ''
        except:
            pass

    if re.match('.*第.*季.*', sentence) or \
            re.match('.*第.*集.*', sentence) or \
            re.match('.*第.*帧.*', sentence):
        # print "filter copora"
        return ''

    sentence = regex_htmltag.sub('', sentence)
    sentence = regex_brace.sub('', sentence)
    sentence = regex_slash.sub('', sentence)

    sentence = sentence.replace('-', '').strip()

    return sentence

def extract_sentence(sourcedir, outdir):
    for root, dirs, files in os.walk(sourcedir):
        if len(files) == 0 :
            return

        sentences = []
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
        os.makedirs(outdir)

        for index, file in enumerate(files):
            print "===processing: index:" , index, file
            f = open(root + '/' + file, 'r')
            content = f.read()
            f.close()
            encoding = chardet.detect(content)['encoding']
            try:
                for sentence in content.decode(encoding).split('\n'):
                    if len(sentence) > 0:
                        match_cn = pattern_cn.findall(sentence)
                        match_jp1 = pattern_jp1.findall(sentence)
                        match_jp2 = pattern_jp2.findall(sentence)
                        sentence = sentence.strip()

                        if len(match_cn) > 0 \
                            and len(match_jp1) == 0 \
                            and len(match_jp2) == 0 \
                            and len(sentence) > 1 \
                            and len(sentence.split(' ')) < 10:
                            # print sentence.encode('utf-8')=
                            temp = process_sentence(sentence.encode('utf-8'))
                            if '' != temp:
                                sentences.append(temp)
                                sentences.append('\n')
            finally:
                basenum = 25
                outfilename = outdir + '/sentences_out_' + str(index / basenum) + '.txt'
                with open(outfilename, 'a+') as f:
                    f.writelines(sentences)
                sentences = []


extract_sentence(outBasePath + 'srt', outBasePath + 'srt_out')










