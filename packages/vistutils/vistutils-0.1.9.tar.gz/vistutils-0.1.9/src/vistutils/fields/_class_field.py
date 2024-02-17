"""TypedField requires a strongly typed field."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Callable, Never

from vistutils.waitaminute import typeMsg

from vistutils.fields import AbstractField


class ClassField(AbstractField):
  """TypedField requires a strongly typed field."""

  def GET(self, callMeMaybe: Callable) -> Callable:
    """Decorates the intended getter function. The class body does not
    have access to the __get__ until after class creation time."""
    setattr(self, '__creator_function__', callMeMaybe)
    return callMeMaybe

  def __instantiate_inner_class__(self, instance: Any, owner: type) -> None:
    """Instantiates the inner class. """
    if self.__creator_function__ is not None:
      if callable(self.__creator_function__):
        if hasattr(self.__creator_function__, '__self__'):
          return self.__creator_function__(instance, owner)
        return self.__creator_function__(self, instance, owner)
      e = typeMsg('__creator_function__', self.__creator_function__,
                  Callable)
      raise TypeError(e)
    innerClass = self._getInnerClass()
    return innerClass(self, instance, owner)

  def _getInnerClass(self) -> type:
    """Getter-function for the inner-class"""
    return self.__inner_class__

  def __init__(self, innerClass: Any, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs)
    self.__inner_class__ = None
    self.__inner_creator__ = None
    self.__default_inner_instance__ = None
    self.__inner_class__ = None
    self.__creator_function__ = None
    if innerClass is None:
      e = """Inner class must be specified explicitly!"""
      raise ValueError(e)
    if isinstance(innerClass, type):
      self.__inner_class__ = innerClass
    else:
      e = typeMsg('innerClass', innerClass, type)
      raise TypeError(e)
    for arg in args:
      if callable(arg) and self.__creator_function__ is None:
        self.__creator_function__ = arg

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """Getter-function implementation"""
    pvtName = self._getPrivateName()
    if instance is None:
      return self.__inner_class__
    if hasattr(instance, pvtName):
      return getattr(instance, pvtName)
    if instance is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__instantiate_inner_class__(instance, owner)
      return self.__get__(instance, owner, _recursion=True)

  def __set__(self, instance: Any, value: Any) -> Never:
    """Not yet implemented!"""
    raise NotImplementedError

  def __delete__(self, instance: Any, ) -> Never:
    """Not yet implemented!"""
    raise NotImplementedError
