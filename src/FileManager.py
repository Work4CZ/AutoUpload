import csv
from typing import Any, TextIO
from Logger import LoggerMetaclass
import os
from abc import ABC, abstractmethod
from Observer import Observer

class FileManager(ABC, metaclass=LoggerMetaclass):

    def __init__(self):
        self.directory = os.getcwd()

    def __getattribute__(self, __name: str) -> Any:
        """
        实例方法调用捕获

        Args:
            __name (str): 

        Returns:
            Method of being decorated.
        """
        attr = super().__getattribute__(__name)
        if callable(attr):
            return self.logger.log_exceptions(attr)
        return attr

    def read(self, filename):
        """Read a file and return its contents."""
        pass

    @abstractmethod
    def write(self, filename: str, content):
        """Write the content to a file."""
        pass

    def create_temporary_file(self):
        """Create a temporary file and return it."""
        return NamedTemporaryFile(NamedTemporaryFile:"") # TODO 修改为一般临时文件类

    def create_file_manager(type_identifier):
        if type_identifier == "template":
            return TemplateManager()
        elif type_identifier == "table":
            return TableManager()
        elif type_identifier == "temporary":
            return TemporaryManager()
        else:
            raise ValueError(f"Unknown type identifier: {type_identifier}")


class TemplateManager(FileManager):
    def __init__(self):
        super().__init__()
        self.directory = os.path.join(self.directory, "templates")
        
        
    def read(self, filename: str) -> list:
        """
        Read a template file to return as a list.

        Args:
            filename (str): 不包含扩展名，文件名作为上传唯一标识符。

        Returns:
            list: Code template saved as a list.
        """
        self.filename = filename
        self.filepath = os.path.join(self.directory,
                                     f"{self.filename}.py")
        with open(self.filepath, "r", encoding="utf-8") as file:
            return file.readlines()

    def replace(self):
        pass
    
    def write(self, filename, content: list):
        temp = TemporaryManager()


class TableManager(FileManager):
    
    def __init__(self):
        super().__init__()
        self.directory = os.path.join(self.directory, "csv")

    def read(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            return list(reader)

    def repalce(self):
        pass

    def write(self, filename, content):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(content)


class TemporaryManager(FileManager):
    def __init__(self):
        super().__init__()
        self.directory = os.path.join(self.directory, "Temp")
        self.file = self.create_temporary_file()
        
    def create_temporary_file(self, filename: str="text.py") -> TextIO:
        self.filepath = os.path.join(self.directory, filename)
        return open(self.filepath, "w", encoding="utf-8")

    def read(self, filename):
        with open(filename, 'r') as file:
            return file.read()

    def write(self, filename, content):

