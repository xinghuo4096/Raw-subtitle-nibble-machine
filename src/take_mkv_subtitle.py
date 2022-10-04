from os import path
import os
import sys

mpath = 'F:/1/Maggie.S01.1080p.HULU.WEBRip.DDP5.1.x264-SMURF[rartv]/'

mkv_info = r'D:/Tools/Mkv/mkvtoolnix/mkvinfo.exe'
mkv_extract = r'D:/Tools/Mkv/mkvtoolnix/mkvextract.exe'
os.chdir(mpath)
flist = os.listdir('.')
mkvlist = list()
for item in flist:
    if path.isfile(item):
        fname = os.path.splitext(item)[0]
        fext = os.path.splitext(item)[1]
        if fext == '.mkv':
            os.system(f'{mkv_info} "{item}"')
            extract_commondline = ' '.join(
                [mkv_extract, item, f'tracks  3:"{fname}.sdh.srt" '])
            os.system(extract_commondline)
