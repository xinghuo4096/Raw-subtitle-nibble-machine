'''
   查看mkv的信息和提取字幕
'''
import os
from os import path


def mkv_subtitle_extract(extract: bool = True):
    '''
    提取mkv字幕
    
    - 电影路径，mkvinfo，mkvextract路径。
    
    mpath = 'F:/1/testdir/'
    mkv_info = r'D:/Tools/Mkv/mkvtoolnix/mkvinfo.exe'
    mkv_extract = r'D:/Tools/Mkv/mkvtoolnix/mkvextract.exe'
    
    - 需要根据mkvinfo显示的字幕序号修改
    
    `f'tracks  3:"{fname}.sdh.srt" '`
      
    例子：
    
    提取第四条，序号为3的字幕,并存储为.sdh.srt
    'tracks  3:"{fname}.sdh.srt" '    
    
    '''

    mpath = 'F:/1/Reginald.the.Vampire.S01E01.Dead.Weight.1080p.SYFY.WEBRip.AAC2.0.H264-PMP[rarbg]/'
    mkv_info = r'D:/Tools/Mkv/mkvtoolnix/mkvinfo.exe'
    mkv_extract = r'D:/Tools/Mkv/mkvtoolnix/mkvextract.exe'
    os.chdir(mpath)
    flist = os.listdir('.')
    for item in flist:
        if path.isfile(item):
            fname = os.path.splitext(item)[0]
            fext = os.path.splitext(item)[1]
            if fext == '.mkv':
                os.system(f'{mkv_info} "{item}"')
                if extract:
                    extract_commondline = ' '.join(
                        [mkv_extract, item, f'tracks  2:"{fname}.en.srt" '])
                    os.system(extract_commondline)


mkv_subtitle_extract(False)
mkv_subtitle_extract()