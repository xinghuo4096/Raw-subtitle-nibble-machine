'''例子
单个和多字幕处理的例子

会出错的情况

1. 句子太长，多数是歌词，
需要手动修字幕，把歌词结尾加句号“.”

2. 字幕文字部分，以数字开头
比如，如下：
```
........year
2000
```
需要修改srt文件里对于内容
如修复为：
`........year 2000`

'''
import os

from Srt import Srt, merge_ass_tofile
from clear_subtitle import clear_subtile_fun1, clear_subtile_fun2
from double_language_subtitle import make_double_lanague_subtitle


def main_batch():
    '''
    批处理
    '''
    for i in range(1, 5):
        print(i)
        fname = f'z:/tests/a/testmovie.S01E{i:0>2}.1080p.WEB.H264'

        clear_subtile_fun1(f'{fname}.en.srt', f'{fname}.en.2.srt')
        clear_subtile_fun2(f'{fname}.en.2.srt', f'{fname}.en.3.srt')
        make_double_lanague_subtitle(media=f'movie {fname}',
                                     from_sub=f'{fname}.en.3.srt',
                                     to_sub=f'{fname}.cn.srt',
                                     err_text=f'{fname}.err.txt',
                                     dict_text=f'{fname}.dict.txt')

        merge_ass_tofile(
            first_subtitle_fname=f'{fname}.cn.srt',
            second_subtitle_fname=f'{fname}.en.3.srt',
            new_subtitle_fname=f'{fname}.cnen.ass',
            unalign_subtitle_fname=f'{fname}.unalgin.txt',
            ass_template_fname=('../SrtMergeBox/indata'
                                '/ass_template_cn_en_1280.txt'),
            ass_head_fname='../SrtMergeBox/indata/ass_info_head_cn_en_1280.txt',
            mark1='',
            mark2='',
            mini_time=Srt.MINI_MERGE_TIME,
            max_cnsubtitle=26)


def main_batch2():
    '''
    批处理2
    需要有
    '../SrtMergeBox/indata'
    '/ass_template_cn_en_1280.txt'等文件
    
    文件格式如下：
    
    文件名.en.srt   
     fname = item[:-7]
     sub_ext = item[-6:-4]
     fext = item[-3:] 
 
    
    文件名.sdh.srt
     fname = item[:-8]
     sub_ext = item[-7:-4]
     fext = item[-3:]
    '''
    mpath = 'z:/tests/a/'
    os.chdir(mpath)

    flist = os.listdir('.')
    i = 1
    for item in flist:

        if os.path.isfile(item):
            sub_type = 'en'
            fname = item[:-(3 + 2 + len(sub_type))]
            sub_ext = item[-(4 + len(sub_type)):-4]
            fext = item[-3:]

            if fext == 'srt' and sub_ext == sub_type:
                clear_subtile_fun1(f'{fname}.{sub_type}.srt',
                                   f'{fname}.en.2.srt')
                clear_subtile_fun2(f'{fname}.en.2.srt', f'{fname}.en.3.srt')
                make_double_lanague_subtitle(media=f'movie {fname}',
                                             from_sub=f'{fname}.en.3.srt',
                                             to_sub=f'{fname}.cn.srt',
                                             err_text=f'{fname}.err.txt',
                                             dict_text=f'{fname}.dict.txt')

                merge_ass_tofile(
                    first_subtitle_fname=f'{fname}.cn.srt',
                    second_subtitle_fname=f'{fname}.en.3.srt',
                    new_subtitle_fname=f'{fname}.cnen.ass',
                    unalign_subtitle_fname=f'{fname}.unalgin.txt',
                    ass_template_fname=('../SrtMergeBox/indata'
                                        '/ass_template_cn_en_1280.txt'),
                    ass_head_fname=('../SrtMergeBox/indata'
                                    '/ass_info_head_cn_en_1280.txt'),
                    mark1='',
                    mark2='',
                    mini_time=Srt.MINI_MERGE_TIME,
                    max_cnsubtitle=26)

                print(i, 'ok.', fname)
                i = i + 1


def mymain():
    '''
    单个处理
    '''
    fname = 'z:/tests/a/test.movie'
    clear_subtile_fun1(f'{fname}.en.srt', f'{fname}.en.2.srt')
    clear_subtile_fun2(f'{fname}.en.2.srt', f'{fname}.en.3.srt')
    make_double_lanague_subtitle(media=f'movie {fname}',
                                 from_sub=f'{fname}.en.3.srt',
                                 to_sub=f'{fname}.cn.srt',
                                 err_text=f'{fname}.err.txt',
                                 dict_text=f'{fname}.dict.txt',
                                 sleep_time=30)

    merge_ass_tofile(
        first_subtitle_fname=f'{fname}.cn.srt',
        second_subtitle_fname=f'{fname}.en.3.srt',
        new_subtitle_fname=f'{fname}.cnen.ass',
        unalign_subtitle_fname=f'{fname}.unalgin.txt',
        ass_template_fname='../SrtMergeBox/indata/ass_template_cn_en_1280.txt',
        ass_head_fname='../SrtMergeBox/indata/ass_info_head_cn_en_1280.txt',
        mark1='',
        mark2='',
        mini_time=Srt.MINI_MERGE_TIME,
        max_cnsubtitle=26)


main_batch2()
