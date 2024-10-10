import random
import time

from plyer import notification


def time_to_pause():
    # 计算用户工作的时间
    # 记录开始工作时间
    start_time = time.time()
    # 总工作时间初始化为0
    total_time = 0

    for i in range(2):
        try:
            print(f"提醒开始: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
            # 定义休息提醒的消息列表
            messages = [
                "休息一下吧，你的眼睛需要放松！",
                "是时候站起来活动一下了！",
                "休息5分钟，让你的大脑休息一下。",
                "记得喝水，保持水分！",
                "休息时间到，远离屏幕，保护视力。",
            ]

            # 计算1小时10分钟的随机值
            one_hour = 3600  # 1小时的秒数
            ten_minutes = random.randint(1, 10) * 60  # 1到10分钟的随机秒数
            total_seconds = one_hour + ten_minutes
            session_time = total_seconds

            # 设置定时器
            time_to_wait = time.time() + total_seconds
            
            print(f"休息时间: {total_seconds // 60} 分钟")
            time.sleep(total_seconds)

            total_time += session_time  # 累加到总工作时间

            # 随机选择一条消息
            reminder = random.choice(messages)
            # 构建更加人性化的详细提醒信息
            detail = f"""
    亲爱的用户，{reminder}

    您已经工作了很长一段时间。根据我们的记录，
    您是在 {time.ctime(start_time)} 开始工作的。
    现在，您已经连续工作了 {total_time // 60} 分钟。
    本次工作了 {session_time // 60} 分钟。

    是时候休息一下了！

    我们为您准备了一些休息建议：
    {reminder}

    短暂休息可以帮助您恢复精力，提高工作效率。记得在休息后继续您的工作。

    祝您工作愉快！
    """

            # 发送toast通知
            notification.notify(
                title="休息提醒",
                message=detail,
                app_icon=None,  # 可以设置图标路径
                timeout=6,  # 通知显示时间
                app_name="休息提醒",  # 应用名称
                ticker="休息提醒",  # 通知标题
            )

            print(f"提醒已发送: {detail}")
        except Exception as e:
            print(f"发生错误: {e}")


if __name__ == "__main__":
    time_to_pause()
