from baidu_ce_fy import BaiduceEngine

if __name__ == "__main__":
    translator = BaiduceEngine(keypath="config/mykeys.json")
    text_to_translate = "When tomorrow turns in today, yesterday,\
        and someday that no more important in your memory,\
        we suddenly realize that we r pushed forward by time.\
        This is not a train in still in which you may \
        feel forward when another train goes by.\
        It is the truth that we've all grown up. And we become different."
    print("Translating...")
    translator.translate(text_to_translate, "en", "zh", 1)
    assert translator.rjson
    dst = translator.baidu_json2text(translator.rjson)
    assert dst
    print("Translation result:")
    print(dst)
   
