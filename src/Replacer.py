from abc import ABC, abstractmethod, abstractmethod
from typing import Any, Tuple, List
from Logger import LoggerMetaclass


class AbstractReplacer(ABC, metaclass=LoggerMetaclass):
    """
    抽象的替换器类。
    """

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

    @abstractmethod
    def process(self, line_variable: str) -> Tuple[str, bool]:
        """
        处理行变量，返回处理后的行变量和一个布尔值，表示是否已经处理完毕。

        Args:
            line_variable (str): 需要被处理的行变量。

        Returns:
            Tuple[str, bool]: 处理后的行变量和一个布尔值，表示是否已经处理完毕。
        """
        pass
    

    @staticmethod
    @abstractmethod
    def is_valid(line_variable: str) -> bool:
        """验证行变量是否符合当前替换器的语法。"""
        pass


class AbstractReplacerFactory(ABC):
    """
    抽象的替换器工厂类。
    """
    @abstractmethod
    def create(self) -> AbstractReplacer:
        """创建并返回一个替换器对象。"""
        pass
    
    
class LineReplacerFactory():
    """
    行替换器工厂类。
    """
    
    def create(self, replacers: List[AbstractReplacer]) -> LineReplacer:
        """
        创建并返回一个行替换器对象。

        Args:
            replacers (List[AbstractReplacer]): 用于处理行变量的替换器列表。

        Returns:
            LineReplacer: 行替换器对象。
        """
        pass
    
    
class TemplateReplacerFactory():
    """
    模板替换器工厂类。
    """
    def create(self, line_replacer: LineReplacer) -> TemplateReplacer:
        """
        创建并返回一个模板替换器对象。

        Args:
            line_replacer (LineReplacer): 用于处理行的行替换器。

        Returns:
            TemplateReplacer: 模板替换器对象。
        """
        pass
    
    
class DirectReplacer(AbstractReplacer):
    """
    直接替换器，将行模版中的变量直接替换为行变量的内容。
    直接替换器应该是责任链中的最后一位。
    """
    def process(self, line_variable: str) -> Tuple[str, bool]:
        return super().process(line_variable)

    @staticmethod
    def is_valid(line_variable: str) -> bool:
        return "$" not in line_variable


class StatementReplacer(AbstractReplacer):
    """
    语句替换器，对$ $内语句进行求值再替换。
    """
    def replace(self, line_template: str, line_variables: list[str]) -> str:
