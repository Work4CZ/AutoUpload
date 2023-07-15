from Logger import Logger


class LoggerMetaclass(type):

    def __init__(cls, name, bases, attrs):
        cls.logger = Logger(name)
        super().__init__(name, bases, attrs)


class Abc(metaclass=LoggerMetaclass):

    def __getattribute__(self, __name: str):
        attr = super().__getattribute__(__name)
        if callable(attr):
            return self.logger.log_exceptions(attr)
        return attr


class Test(Abc):

    def test(self):
        print(1 / 0)


t = Test()
t.test()
