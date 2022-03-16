import json
from Translator import Media, MergeSentence, NormalSentence, Sentence, SpliteSentence, SubBlock, Subtitle, TranslationEngine, Translator, languages, save_file
from Srt import save_srt


def test_media():

    movie1 = Media('movie 1')
    movie1.add_subtitle('en', 'tests/test_srt1.srt')

    assert movie1.subtitles[0].language == 'en'

    sub = movie1.subtitles[0]
    assert isinstance(sub, Subtitle)

    sub.make_sentence()

    blks = sub.subblocks
    assert len(blks) == 15
    assert isinstance(blks[0].sentences, list)

    assert len(blks[0].sentences) == 1
    st1 = blks[0].sentences[0]
    assert isinstance(st1, Sentence)
    assert isinstance(st1, NormalSentence)
    assert st1.text == 'Thank you.'

    assert len(blks[1].sentences) == 1
    st1 = blks[1].sentences[0]
    assert isinstance(st1, Sentence)
    assert isinstance(st1, NormalSentence)
    assert st1.text == 'This time, thank you.'

    assert len(blks[2].sentences) == 1
    st1 = blks[2].sentences[0]
    assert isinstance(st1, Sentence)
    assert isinstance(st1, NormalSentence)
    assert st1.text == 'Okay.I gotta go.'

    assert len(blks[4].sentences) == 1
    st1 = blks[4].sentences[0]
    assert isinstance(st1, Sentence)
    assert isinstance(st1, NormalSentence)
    assert st1.text == 'Starting a capital raise.'

    assert len(blks[5].sentences) == 1
    st1 = blks[5].sentences[0]
    assert isinstance(st1, Sentence)
    assert isinstance(st1, MergeSentence)
    assert len(st1.subblocks) > 1
    assert len(st1.subblocks) == 3
    blk = blks[5]
    assert blk == st1.subblocks[0]
    assert blk != st1.subblocks[-1]
    assert st1.text == ''
    assert blk.text != st1.text
    assert blk.text == 'After our session,'

    assert len(blks[6].sentences) == 1
    st1 = blks[6].sentences[0]
    assert isinstance(st1, Sentence)
    assert isinstance(st1, MergeSentence)
    assert len(st1.subblocks) > 1
    assert len(st1.subblocks) == 3
    blk = blks[6]
    assert isinstance(blk, SubBlock)
    assert blk == st1.subblocks[1]
    assert blk != st1.subblocks[-1]
    assert st1.text == ''
    assert blk.text != st1.text
    assert blk.text == 'I had the sudden clarity that we were ready,'

    assert len(blks[7].sentences) == 1
    st1 = blks[7].sentences[0]
    assert isinstance(st1, Sentence)
    assert isinstance(st1, MergeSentence)
    assert len(st1.subblocks) > 1
    assert len(st1.subblocks) == 3
    blk = blks[7]
    assert isinstance(blk, SubBlock)
    assert blk == st1.subblocks[2]
    assert blk == st1.subblocks[-1]
    assert blk.text == 'that I was ready.' != st1.text
    assert st1.text == 'After our session,I had the sudden clarity that we were ready,that I was ready.'

    sub = movie1.subtitles[0]
    assert isinstance(sub, Subtitle)
    textlist = sub.get_sentences_text()

    fanyi_text_for_test = (
        '[[["谢谢你。\\n","Thank you.\\n",null,null,10,null,null,null,[[null,true]]],["这一次，谢谢。\\n","This time, thank you.\\n",null,null,3,null,null,[[]],[[["041e86f75565b6341f86f9972f755ac9","en_zh_2021q4.md"]],[null,true]]],["好吧，我得走了。\\n","Okay.I gotta go.\\n",null,null,3,null,null,[[]],[[["041e86f75565b6341f86f9972f755ac9","en_zh_2021q4.md"]],[null,true]]],["我正在去见瓦格斯的路上。\\n","I\'m on my way to meet Wags.\\n",null,null,3,null,null,[[]],[[["041e86f75565b6341f86f9972f755ac9","en_zh_2021q4.md"]],[null,true]]],["开始筹资。\\n","Starting a capital raise.\\n",null,null,3,null,null,[[]],[[["041e86f75565b6341f86f9972f755ac9","en_zh_2021q4.md"]],[null,true]]],["会议结束后，我突然明白我们准备好了，我准备好了。\\n","After our session,I had the sudden clarity that we were ready,that I was ready.\\n",null,null,3,null,null,[[]],[[["041e86f75565b6341f86f9972f755ac9","en_zh_2021q4.md"]],[null,true]]],["去拿他们。\\n","Go get \'em.\\n",null,null,3,null,null,[[]],[[["041e86f75565b6341f86f9972f755ac9","en_zh_2021q4.md"]],[null,true]]],["我将会。\\n","I will.\\n",null,null,1,null,null,null,[[null,true]]],["- 你是怎么进去的？ - 凭直觉。\\n","- How\'d you step into it?- On a hunch.\\n",null,null,3,null,null,[[]],[[["041e86f75565b6341f86f9972f755ac9","en_zh_2021q4.md"]],[null,true]]],["我是付钱给警察让问题消失的人。这就是我在这里所做的。\\n","I\'m the one who pays off the copsto make the problem go away.That\'s what I do here.\\n",null,null,3,null,null,[[]],[[["041e86f75565b6341f86f9972f755ac9","en_zh_2021q4.md"]],[null,true]]],["我是那个付清警察的人我突然明白我们已经准备好了，","I\'m the one who pays off the copsI had the sudden clarity that we were ready,",null,null,3,null,null,[[]],[[["041e86f75565b6341f86f9972f755ac9","en_zh_2021q4.md"]]]]],null,"en",null,null,null,1,[],[["en"],null,[1],["en"]]]',
        'utf-8')
    textpack = Translator.make_fanyi_packge(textlist)
    fanyi_text, fanyi_code = fanyi_text_for_test  # # fanyi_text_for_test  # TranslationEngine.fanyi_google( textpack[0], 'auto'    )  #fanyi_text_for_test  # # TranslationEngine.fanyi_google( textpack, 'auto')  #

    assert fanyi_text == fanyi_text_for_test[0]
    fdict = Translator.make_fanyi_dict(fanyi_text)

    subcn = movie1.add_language_subtitle("zh-CN,en")
    assert subcn == movie1.subtitles[1]
    assert isinstance(subcn, Subtitle)

    err_texts = Translator.translate_byte_dict(subcn, fdict)
    if len(err_texts):
        raise Exception('err_texts.')
    assert len(subcn.subblocks) == 15
    blks = subcn.subblocks
    blks[0].text == '谢谢你。'
    blks[2].text == '好的。我要走了'

    blks[5].text == '会议结束后，'
    blks[6].text == '我突然明白我们准备好了，'
    blks[7].text == '我准备好了。'
    blks[9].text == '我将会。'

    #
    subcn = movie1.add_language_subtitle("zh-CN,en")
    assert subcn == movie1.subtitles[2]
    assert isinstance(subcn, Subtitle)

    err_texts = Translator.translate_byte_dict(subcn, fdict)
    if err_texts:
        raise Exception('err_texts.')
    assert len(subcn.subblocks) == 15
    blks = subcn.subblocks
    blks[0].text == '谢谢你。'
    blks[2].text == '好的。我要走了'

    blks[5].text == '会议结束后，我突然明白我们准备好了，我准备好了。'
    blks[6].text == '会议结束后，我突然明白我们准备好了，我准备好了。'
    blks[7].text == '会议结束后，我突然明白我们准备好了，我准备好了。'
    blks[9].text == '会议结束后，我突然明白我们准备好了，我准备好了。'
    blks[9].text == '我将会。'

    save_srt('outdata/test_srt1_new_cnen.srt', subcn.subblocks)

    #
    movie1 = Media('movie 2')
    movie1.add_subtitle('en', 'tests/a12en.srt')
    assert movie1.subtitles[0].language == 'en'

    sub = movie1.subtitles[0]
    assert isinstance(sub, Subtitle)

    sub.make_sentence()
    blks = sub.subblocks
    assert len(blks) > 100

    sub = movie1.subtitles[0]
    assert isinstance(sub, Subtitle)
    textlist = sub.get_sentences_text()
    textpack = Translator.make_fanyi_packge(textlist)
    fdict = dict()
    #这里是一组包，需要一个一个的翻译。
    for item in textpack:
        fanyiret = TranslationEngine.fanyi_google(item, 'auto')
        fanyi_text, fanyi_code = fanyiret
        dict1 = Translator.make_fanyi_dict(fanyi_text)
        fdict.update(dict1)

    subcn = movie1.add_language_subtitle("zh-CN")
    assert subcn == movie1.subtitles[1]
    assert isinstance(subcn, Subtitle)

    err_texts = Translator.translate_byte_dict(subcn, fdict)
    if len(err_texts) > 0:
        save_file('outdata/a12en_new_cn_err_text.txt', '\n'.join(err_texts))
    assert len(subcn.subblocks) > 100

    save_srt('outdata/a12en_new_cn.srt', subcn.subblocks)

    strlist = ['{0}----{1}'.format(x, fdict[x]) for x in list(fdict)]

    save_file('outdata/a12en_new_cn_fdict.txt', '\n'.join(strlist))
    print()


def main():
    test_media()


if __name__ == '__main__':
    main()
