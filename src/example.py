'''例子
单个和多字幕处理的雷子
'''
from clear_subtitle import clear_subtile_fun1, clear_subtile_fun2
from double_language_subtitle import make_double_lanague_subtitle


def main_batch():
    '''
    批处理
    '''
    for i in range(1, 9):
        print(i)
        fname = f'z:/tests/a/test.S01E{i:0>2}.'

        make_double_lanague_subtitle(media=f'movie {i}',
                                     from_sub=f'{fname}.en.srt',
                                     to_sub=f'{fname}.cn.srt',
                                     err_text=f'{fname}.err.txt',
                                     dict_text=f'{fname}.dict.txt')


def mymain():
    '''
    单个处理
    '''
    fname = 'z:/tests/a/Emily.the.Criminal.2022.1080p.AMZN.WEB-DL.DDP5.1.H.264-SMURF'
    clear_subtile_fun1(f'{fname}.en.srt', f'{fname}.en.2.srt')
    clear_subtile_fun2(f'{fname}.en.2.srt', f'{fname}.en.3.srt')
    make_double_lanague_subtitle(media=f'movie {fname}',
                                 from_sub=f'{fname}.en.3.srt',
                                 to_sub=f'{fname}.cn.srt',
                                 err_text=f'{fname}.err.txt',
                                 dict_text=f'{fname}.dict.txt')


mymain()
