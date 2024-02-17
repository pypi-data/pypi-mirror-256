"""EZField provides a descriptor class for the EZData class. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from vistutils import monoSpace
from vistutils.fields import AbstractField

from morevistutils.waitaminute import typeMsg


class EZField(AbstractField):
  """EZField provides a descriptor class for the EZData class. """

  def __init__(self, type_: type, defVal: Any = None) -> None:
    AbstractField.__init__(self, )
    self.__value_type__ = None
    self.__default_value__ = None
    if defVal is None:
      if isinstance(type_, type):
        self.__value_type__ = type_
        self.__default_value__ = None
      else:
        self.__default_value__ = type_
        self.__value_type__ = type(type_)
    if isinstance(type_, type):
      if isinstance(defVal, type_):
        self.__default_value__ = defVal
        self.__value_type__ = type_
    if self.__value_type__ is None:
      raise TypeError

  def __prepare_owner__(self, owner: type) -> type:
    """Implementation of the abstract method"""
    existing = getattr(owner, '__ez_fields__', [])
    setattr(owner, '__ez_fields__', [*existing, self])
    return owner

  def __prepare_instance__(self, instance: Any) -> Any:
    """Prepares the instance"""
    pvtName = self._getPrivateName()
    defVal = self.__default_value__
    if defVal is None:
      defVal = self.__value_type__()
      # e = """Instance of '%s' was not created with default value!"""
      # raise ValueError(monoSpace(e % self.__class__.__qualname__))
    setattr(instance, pvtName, self.__default_value__)

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """Getter-function"""
    pvtName = self._getPrivateName()
    if hasattr(instance, pvtName, ):
      val = getattr(instance, pvtName)
      if isinstance(val, self.__value_type__):
        return val
      e = typeMsg('val', val, self.__value_type__)
      raise TypeError(e)
    if kwargs.get('_recursion', False):
      raise RecursionError
    self.__prepare_instance__(instance)
    return self.__get__(instance, owner, _recursion=True)

  def __set__(self, instance: Any, value: Any) -> None:
    """Setter-function"""
    pvtName = self._getPrivateName()
    try:
      setattr(instance, pvtName, self._typeGuard(value))
    except TypeError as typeError:
      e = typeMsg('value', value, self.__value_type__)
      raise TypeError(e) from typeError

  def __delete__(self, instance: Any) -> None:
    """Deleter function"""
    delattr(instance, self._getPrivateName())

  def _typeGuard(self, value: Any) -> Any:
    """Converts value to match field value type"""
    if self.__value_type__ not in [int, float, complex]:
      if isinstance(value, self.__value_type__):
        return value
      e = typeMsg('value', value, self.__value_type__)
      raise TypeError(e)
    if type(value) in [int, float, complex]:
      if self.__value_type__ is type(value):
        return value
      if self.__value_type__ is int:
        if type(value) is float:
          if (round(value) - value) ** 2 < 1e-08:
            return int(value)
          raise TypeError
        if type(value) is complex:
          if value.imag ** 2 < 1e-08:
            return int(value.real)
          if value.real ** 2 < 1e-08:
            return int(value.imag)
          raise TypeError
      if self.__value_type__ is float:
        if type(value) is complex:
          if value.imag ** 2 < 1e-08:
            return value.real
          if value.real ** 2 < 1e-08:
            return value.imag
          raise TypeError
        if type(value) is int:
          return float(value)
      if self.__value_type__ is complex:
        return value + 0j
    raise TypeError
