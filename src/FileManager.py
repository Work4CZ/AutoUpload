import csv
from typing import Any
from Logger import Logger, LoggerMetaclass
import os
from abc import ABC, abstractmethod
from tempfile import TemporaryFile



class FileManager(ABC, metaclass=LoggerMetaclass):
    def __init__(self):
        self.directory = os.getcwd()

    def __getattribute__(self, __name: str) -> Any:
        """
        实例方法调用捕获

        Args:
            __name (str): 

        Returns:
            Method of being decorated
        """        
        attr = super().__getattribute__(__name)
        if callable(attr):
            return self.logger.log_exceptions(attr)
        return attr
        
    
    def read(self, filename):
        """Read a file and return its contents."""
        pass

    @abstractmethod
    def write(self, filename, content):
        """Write the content to a file."""
        pass

    def create_temporary_file(self):
        """Create a temporary file and return it."""
        return TemporaryFile()

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
    def read(self, filename):
        self.filename = filename
        filepath = 
        with open(filename, "r") as file:
            
            return file.read()

    def write(self, filename, content):
        with open(filename, "w") as file:
            file.write(content)


class TableManager(FileManager):
    def read(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            return list(reader)

    def write(self, filename, content):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(content)


class TemporaryManager(FileManager):
    def read(self, filename):
        with open(filename, 'r') as file:
            return file.read()

    def write(self, filename, content):
        with TemporaryFile('w+t') as temp_file:
            temp_file.write(content)
            temp_file.seek(0)
            return temp_file.name
