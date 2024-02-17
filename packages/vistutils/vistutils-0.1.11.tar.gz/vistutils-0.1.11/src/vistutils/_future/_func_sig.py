"""FuncSig instances represent a tuple of types. The functionality comes
from constructing directly from types or by inferring types from values
given. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any


class FuncSig:
  """FuncSig instances represent a tuple of types. The functionality comes
  from constructing directly from types or by inferring types from values
  given. """

  def __init__(self, *args, **kwargs) -> None:
    if all([isinstance(arg, type) for arg in args]):
      self._types = (*args,)
    else:
      self._types = (*[type(arg) for arg in args],)
    self.__iter_contents__ = None

  def __eq__(self, other: Any) -> bool:
    """Requires all types to match"""
    if isinstance(other, FuncSig):
      return True if self._types == other._types else False
    if isinstance(other, (tuple, list)):
      for thisType, otherType in zip(self, other):
        if thisType is not otherType:
          if not issubclass(otherType, thisType):
            if not issubclass(thisType, otherType):
              return False
      return True
    return NotImplemented

  def __iter__(self) -> FuncSig:
    """Implements iteration"""
    self.__iter_contents__ = [type_ for type_ in self._types]
    return self

  def __next__(self, ) -> type:
    """Implements iteration"""
    if self.__iter_contents__ is None:
      raise ValueError('Types not present!')
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __call__(self, *types) -> bool:
    """Allows calling to invoke comparison check"""
