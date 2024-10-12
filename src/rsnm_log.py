import logging
import logging.config
from enum import Enum

# 定义不同日志级别的颜色


class LogColors(Enum):
    DEBUG = "\033[1;34m"  # 蓝色
    INFO = "\033[1;32m"  # 绿色
    WARNING = "\033[1;33m"  # 黄色
    ERROR = "\033[1;31m"  # 红色
    CRITICAL = "\033[1;35m"  # 品红色
    RESET_COLOR = "\033[0m"  # 重置颜色


# 日志配置字典
default_logging_conf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s[%(module)-20s] %(name)-15s %(levelname)-8s  %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": "rsnm_log.log",  # 日志文件路径
            "mode": "a",  # 追加模式
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,  # 不向上传播，因为我们已经设置了root logger
        }
    },
}


def setup_logging(logging_conf=default_logging_conf):
    """
    使用给定的配置字典来配置日志系统，并返回一个日志记录器。

    :param logging_conf: 一个字典，包含了日志配置的详细信息。
    :return: 配置好的日志记录器。
    """
    logging.config.dictConfig(logging_conf)
    return logging.getLogger(__name__)


if __name__ == "__main__":
    # 设置日志并获取日志记录器
    logger = setup_logging()
    logger.info("This message will go to both console and file from some_function.")
    logger.info("这条消息将同时发送到控制台和文件，来自 some_function 函数。")
