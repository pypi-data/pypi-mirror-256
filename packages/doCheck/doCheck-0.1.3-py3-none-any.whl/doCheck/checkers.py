import typing
import re

__all__ = ["BaseChecker","AnyChecker", "IntersectionChecker", "UnionChecker", 
           "ComplementaryChecker", "NotChecker", "LiteralChecker","EnumChecker",
           "RangeChecker","CallableChecker","RegexChecker","AttributeChecker","ItemChecker"]

class BaseChecker(object):
    """
    The base class of all checkers.
    """
    check: typing.Callable[[typing.Any],bool]
    def __and__(self, other:"BaseChecker") -> "IntersectionChecker":
        return IntersectionChecker(self, other)
    def __or__(self, __value: "BaseChecker") -> "UnionChecker":
        return UnionChecker(self, __value)
    def __invert__(self) -> "NotChecker":
        return NotChecker(self)
    def __not__(self) -> "NotChecker":
        return NotChecker(self)
    def __add__(self, other:"BaseChecker") -> "UnionChecker":
        return UnionChecker(self, other)
    def __sub__(self, other:"BaseChecker") -> "ComplementaryChecker":
        return ComplementaryChecker(self)
    def __neg__(self) -> "NotChecker":
        return NotChecker(self)
    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>"

class AnyChecker(BaseChecker):
    """
    Return true
    """
    def check(self,value):
        return True

_anyChecker=AnyChecker()

class IntersectionChecker(BaseChecker):
    """
    The intersection checker.
    It will return True if all checkers return True.
    """
    _checkers: typing.List[BaseChecker]
    def __init__(self, *checkers:BaseChecker):
        self._checkers = list(checkers)
    def check(self, value):
        for checker in self._checkers:
            if not checker.check(value):
                return False
        return True
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._checkers}>"

class UnionChecker(BaseChecker):
    """
    The union checker.
    It will return True if any checker return True.
    """
    _checkers: typing.List[BaseChecker]
    def __init__(self, *checkers:BaseChecker):
        self._checkers = list(checkers)
    def check(self, value):
        for checker in self._checkers:
            if checker.check(value):
                return True
        return False
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._checkers}>"

class ComplementaryChecker(BaseChecker):
    """
    The complementary checker.
    It will return True if the universal checker return True and the other checker return False.
    """
    _universalChecker: BaseChecker
    _otherChecker: UnionChecker
    def __init__(self, universalChecker:BaseChecker,*otherCheckers:BaseChecker):
        self._otherChecker = UnionChecker(*otherCheckers)
        self._universalChecker = universalChecker
    def check(self, value):
        return self._universalChecker.check(value) and not self._otherChecker.check(value)
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._universalChecker} - {self._otherChecker}>"

class NotChecker(BaseChecker):
    """
    The not checker.
    It will return True if the checker return False.
    """
    _checker: BaseChecker
    def __init__(self, checker:BaseChecker):
        self._checker = checker
    def check(self, value):
        return not self._checker.check(value)
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._checker}>"

class LiteralChecker(BaseChecker):
    """
    The literal checker.
    It will return True if the value is in the list of values.
    """
    _values:typing.List
    def __init__(self, *values):
        self._values = list(values)
    def check(self, value):
        return value in self._values
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._values}>"

EnumChecker=LiteralChecker #Another name for LiteralChecker

class TypeChecker(BaseChecker):
    """
    The type checker.
    It will return True if the value is in the list of types.
    """
    _type: typing.List[type]
    def __init__(self, *t:type):
        self._type = list(t)
    def check(self, value):
        for t in self._type:
            if isinstance(value,t):
                return True
        return False
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._type}>"

class RangeChecker(BaseChecker):
    """
    The range checker.
    It will return True if the value is in the range.
    """
    _min: int|float
    _max: int|float
    _leftClosed: bool
    _rightClosed: bool
    typeChecker=TypeChecker(int,float)
    def __init__(self, min:int|float, max:int|float,leftClosed:bool=True,rightClosed:bool=False):
        self._min = min
        self._max = max
        self._leftClosed = leftClosed
        self._rightClosed = rightClosed
    def check(self, value):
        return self.typeChecker.check(value) and self._min < value < self._max or (self._min == value and self._leftClosed) or (self._max == value and self._rightClosed)
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {'[' if self._leftClosed else '('}{self._min} , {self._max}{']' if self._rightClosed else ')'}>"

class CallableChecker(BaseChecker):
    """
    The callable checker.
    It will return True if the value is callable.
    """
    _callable: typing.Callable
    def check(self, value):
        return callable(value)

class RegexChecker(BaseChecker):
    """
    The regex checker.
    It will return True if the value is matched by the regex.
    """
    _regexPattern: re.Pattern
    _regex:str
    _flags:re._FlagsType
    _typeChecker=TypeChecker(str)
    def __init__(self, regex:str,flags:re._FlagsType=0):
        self._regexPattern = re.compile(regex,flags)
        self._regex = regex
        self._flags = flags
    def check(self, value):
        return  self._typeChecker.check(value) and self._regexPattern.match(value)
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._regex}/{self._flags}>"

class AttributeChecker(BaseChecker):
    """
    The Attribute  checker.
    It will return True if the value is a Attribute  and the value is matched by the Attribute Checker.
    """
    attributeName: str
    attributeChecker: BaseChecker
    def __init__(self, attributeName:str, attributeChecker:BaseChecker=_anyChecker):
        self.attributeChecker = attributeChecker
        self.attributeName = attributeName
    def check(self, value):
        if not hasattr(value, self.attributeName):
            return False
        return self.attributeChecker.check(getattr(value, self.attributeName))
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.attributeName}:{self.attributeChecker}>"
    
class ItemChecker(BaseChecker):
    """
    The Item checker.
    It will return True if the value is a Item and the value is matched by the Item Checker.
    """
    itemChecker: BaseChecker
    itemName: typing.Any
    def __init__(self, itemName:typing.Any, itemChecker:BaseChecker=_anyChecker):
        self.itemChecker = itemChecker
        self.itemName = itemName
    def check(self, value):
        try:
            return self.itemChecker.check(value[self.itemName])
        except:
            return False
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.itemName}:{self.itemChecker}>"
