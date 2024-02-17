"""DataType provides a dataclass representation of a type with a default
value. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from vistutils.waitaminute import typeMsg


class DataType:
  """Data class representation of type with default value"""

  __common_defaults__ = {int : 0, float: .0, complex: 0j, str: '',
                         bool: False, list: [],
                         dict: dict(), set: set(), }

  @classmethod
  def _searchName(cls, name: str) -> type:
    """Finds a type object in global namespace"""

  @classmethod
  def _getCommonDefault(cls, ) -> dict:
    """Returns a dictionary where keys are types and values are suggested
    default values"""
    return cls.__common_defaults__

  @classmethod
  def _parse(cls, *args, **_) -> Any:
    """Parses positional arguments"""
    if all([isinstance(arg, str) for arg in args]):
      return (0, *args[:2],)
    if len(args) == 2:
      if not isinstance(args[0], type):
        if isinstance(args[1], type):
          return cls._parse(args[1], args[0])
        raise TypeError
      if not isinstance(args[1], args[0]):
        raise TypeError
      return (1, *args,)
    if len(args) == 1:
      if isinstance(args[0], type):
        commonDefaults = cls._getCommonDefault()
        defVal = commonDefaults.get(args[0], None)
        if defVal is not None:
          return cls._parse(args[0], defVal)
        defVal = args[0]()
        return cls._parse(args[0], defVal)
      return (1, type(args[0]), args[0])

  def __init__(self, *args) -> None:
    parsed = self._parse(*args)
    if parsed is None:
      raise ValueError
    parsed = (*parsed,)[:3]
    self.__data_type__ = None
    self.__default_value__ = None
    self.__data_type_name__ = None
    if parsed[0]:
      self.__data_type__, self.__default_value__ = parsed[1:3]
      self.__data_type_name__ = self.__data_type__.__qualname__
    else:
      self.__data_type_name__ = parsed[1]

  def getType(self) -> type:
    """Getter-function for type"""
    if self.__data_type__ is None:
      raise NotImplementedError
    return self.__data_type__

  def getDefault(self) -> Any:
    """Getter-function for default value"""
    if self.__default_value__ is None:
      raise RuntimeError
    valType = self.getType()
    if isinstance(self.__default_value__, valType):
      return self.__default_value__
    e = typeMsg('__default_value__', self.__default_value__, valType)
    raise TypeError(e)
