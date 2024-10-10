import logging
import logging.config





# 日志配置字典
default_logging_conf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {"format": "%(asctime)s[%(module)-20s] %(name)-15s %(levelname)-8s  %(message)s"},
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