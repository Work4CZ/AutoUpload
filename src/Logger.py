import logging
import os
import traceback
import functools
import sys
from Interactor import tui
from datetime import datetime


class TUIHandler(logging.StreamHandler):

    def emit(self, record: logging.LogRecord):
        log_entry = self.format(record)
        tui.report_error(log_entry)


class LoggerMetaclass(type):
    """
    生成类的时生成一个类名作为参数的logger
    """

    def __init__(cls, name, bases, attrs):
        cls.logger = Logger(name)
        super().__init__(name, bases, attrs)


class Logger:
    """
    日志记录器
    
    在主程序中创建Logger实例
    """

    def __init__(self, class_name=None):
        """

        Args:
            class_name (str, optional): 发生错误的类名. Defaults to None.
            class_name为None时只输出到TUI
        """
        self.name = class_name
        self.logger = logging.getLogger(class_name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Log to file if log_file is provided
        if class_name:
            log_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', 'logs'))
            os.makedirs(log_dir, exist_ok=True)

            date_str = datetime.now().strftime("%Y-%m-%d")
            file_name = f"{date_str}.log"
            file_path = os.path.join(log_dir, file_name)

            file_handler = logging.FileHandler(file_path)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Always log to TUI
        tui_handler = TUIHandler()
        tui_handler.setLevel(logging.DEBUG)
        tui_handler.setFormatter(formatter)
        self.logger.addHandler(tui_handler)

    def log(self, level: str, message: str):
        """
        根据等级记录日志

        Args:
            level (str): info, warning, error, debug
            message (str): 写入的信息
        """
        log_method = getattr(self.logger, level, None)
        if callable(log_method):
            log_method(message)

    def log_exceptions(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                tb = traceback.extract_tb(sys.exc_info()[2])  # 获取 traceback 信息
                last_tb = tb[-1]
                message = (
                    f"The error is in lines {last_tb.lineno} to {last_tb.end_lineno} of file {last_tb.filename}, "
                    f"which has the code:'{last_tb.line}' in function {last_tb.name}. "
                    f"The local variable is: {last_tb.locals}.")

                self.log(
                    "error",
                    f"Exception occurred in {func.__name__}: {e}\n{message}")
                raise e

        return wrapper


pass
