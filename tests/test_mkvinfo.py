import os
import re
import subprocess


def run_mkvinfo(cmd):
    '''
    _summary_运行mkvinfo

    Args:
        cmd (_type_): _description_

    Returns:
        _type_: _description_
    '''
    ret = subprocess.check_output(cmd,
                                  encoding='utf-8',
                                  universal_newlines=True)
    return ret


track_number_re = re.compile(r'\d+')


def main():
    '''
    main
    '''
    test_info = '+ EBML head\n|+ Document type: matroska\n|+ Document type version: 1\n|+ Document type read version: 1\n+ Segment: size 2365536139\n|+ Seek head (subentries will be skipped)\n|+ EBML void: size 4027\n|+ Segment information\n| + Timestamp scale: 1000000\n| + Multiplexing application: libebml v0.7.7 + libmatroska v0.8.1\n| + Writing application: mkvmerge v2.2.0 (\'Turn It On Again\') built on Mar  4 2008 12:58:26\n| + Duration: 01:33:09.568000000\n| + Date: 2011-05-23 02:53:41 UTC\n| + Segment UID: 0x84 0xd9 0xc2 0x56 0x7b 0x17 0xcd 0xc2 0xbf 0x3e 0xab 0xbb 0xf1 0x7d 0xd8 0x48\n|+ Tracks\n| + Track\n|  + Track number: 1 (track ID for mkvmerge & mkvextract: 0)\n|  + Track UID: 1\n|  + Track type: video\n|  + "Enabled" flag: 1\n|  + "Default track" flag: 1\n|  + "Forced display" flag: 0\n|  + "Lacing" flag: 0\n|  + Minimum cache: 1\n|  + Timestamp scale: 1\n|  + Maximum block additional ID: 0\n|  + Codec ID: V_MPEG4/ISO/AVC\n|  + Codec decode all: 1\n|  + Codec\'s private data: size 39 (H.264 profile: High @L3.1)\n|  + Default duration: 00:00:00.041708299 (23.976 frames/fields per second for a video track)\n|  + Language: eng\n|  + Name: 帝国出品\n|  + Video track\n|   + Pixel width: 1280\n|   + Pixel height: 720\n|   + Interlaced: 0\n|   + Display width: 16\n|   + Display height: 9\n| + Track\n|  + Track number: 2 (track ID for mkvmerge & mkvextract: 1)\n|  + Track UID: 1530909330\n|  + Track type: audio\n|  + "Enabled" flag: 1\n|  + "Default track" flag: 1\n|  + "Forced display" flag: 0\n|  + "Lacing" flag: 1\n|  + Minimum cache: 0\n|  + Timestamp scale: 1\n|  + Maximum block additional ID: 0\n|  + Codec ID: A_AC3\n|  + Codec decode all: 1\n|  + Default duration: 00:00:00.032000000 (31.250 frames/fields per second for a video track)\n|  + Language: eng\n|  + Name: 英语\n|  + Audio track\n|   + Sampling frequency: 48000\n|   + Channels: 6\n| + Track\n|  + Track number: 3 (track ID for mkvmerge & mkvextract: 2)\n|  + Track UID: 128934551\n|  + Track type: audio\n|  + "Enabled" flag: 1\n|  + "Default track" flag: 0\n|  + "Forced display" flag: 0\n|  + "Lacing" flag: 1\n|  + Minimum cache: 0\n|  + Timestamp scale: 1\n|  + Maximum block additional ID: 0\n|  + Codec ID: A_AC3\n|  + Codec decode all: 1\n|  + Default duration: 00:00:00.032000000 (31.250 frames/fields per second for a video track)\n|  + Language: chi\n|  + Name: 国语\n|  + Audio track\n|   + Sampling frequency: 48000\n|   + Channels: 6\n| + Track\n|  + Track number: 4 (track ID for mkvmerge & mkvextract: 3)\n|  + Track UID: 2284312751\n|  + Track type: subtitles\n|  + "Enabled" flag: 1\n|  + "Default track" flag: 1\n|  + "Forced display" flag: 0\n|  + "Lacing" flag: 0\n|  + Minimum cache: 0\n|  + Timestamp scale: 1\n|  + Maximum block additional ID: 0\n|  + Codec ID: S_TEXT/ASS\n|  + Codec decode all: 1\n|  + Codec\'s private data: size 854\n|  + Language: eng\n|  + Name: 中英文\n| + Track\n|  + Track number: 5 (track ID for mkvmerge & mkvextract: 4)\n|  + Track UID: 3714309271\n|  + Track type: subtitles\n|  + "Enabled" flag: 1\n|  + "Default track" flag: 0\n|  + "Forced display" flag: 0\n|  + "Lacing" flag: 0\n|  + Minimum cache: 0\n|  + Timestamp scale: 1\n|  + Maximum block additional ID: 0\n|  + Codec ID: S_TEXT/ASS\n|  + Codec decode all: 1\n|  + Codec\'s private data: size 544\n|  + Language: chi\n|  + Name: 中文\n|+ EBML void: size 1024\n|+ Cluster\n'
    mkvinfo = r'E:\Temp\mkvtoolnix\mkvinfo.exe'
    mvkinfo_args = [
        '--ui-language en', '--command-line-charset utf-8',
        '--output-charset utf-8'
    ]
    fmkv = 'test.mkv'

    arg1 = f'{mkvinfo} {" ".join(mvkinfo_args)} "{fmkv}"'
    info = arg1
    info = test_info
    #run_mkvinfo(arg1)

    info_splite_1 = re.compile(r'^\+ ', re.MULTILINE)
    info_splite_2 = re.compile(r'^\|\+ ', re.MULTILINE)
    info_splite_3 = re.compile(r'^\| \+ ', re.MULTILINE)
    info_splite_4 = re.compile(r'^\|  \+ ', re.MULTILINE)

    info_1 = list(filter(None, info_splite_1.split(info)))
    assert len(info_1) > 1
    assert info_1[1].startswith('Segment')

    temp = [x for x in info_1 if x.startswith('Segment')]
    assert len(temp) > 0
    info_segment = temp[0]

    info_2 = list(filter(None, info_splite_2.split(info_segment)))
    assert len(info_2) > 0
    temp = [x for x in info_2 if x.startswith('Tracks')]
    assert len(temp) > 0
    info_tracks = temp[0]

    info_3 = list(filter(None, info_splite_3.split(info_tracks)))
    assert len(info_3) > 0

    temp = [x for x in info_3 if x.startswith('Track\n')]
    tracks = temp
    assert len(tracks) > 0

    tlist = list()
    for item in tracks:
        temp1 = info_splite_4.split(item)
        temp1 = make_track(temp1)
        tlist.append(temp1)

    print()


def make_track(list1):
    '''
    make track

    Args:
        str1 (str): _description_
    '''
    for item in list1:
        if item.startswith('Track number'):
            tn1 = track_number_re.findall(item)
        if item.startswith('Track type'):
            temp = item.split(':')
            ttype = temp[1].strip()

        if item.startswith('Language'):
            temp = item.split(':')
            tl = temp[1].strip()
        if item.startswith('Name'):
            temp = item.split(':')
            tn = temp[1].strip()
        if item.startswith('Codec ID'):
            temp = item.split(':')
            tci = temp[1].strip()

    track1 = Track(tn1[0], ttype, tl, tn, tci)
    return track1


class Track():
    '''
    mkv track
    '''

    def __init__(self, track_number, track_type, track_language, track_name,
                 track_codec_id):
        self.number = int(track_number)
        self.mkvextract_id = self.number - 1
        self.track_type = track_type
        self.language = track_language
        self.name = track_name
        self.codec_id = track_codec_id


#-----------------
main()
