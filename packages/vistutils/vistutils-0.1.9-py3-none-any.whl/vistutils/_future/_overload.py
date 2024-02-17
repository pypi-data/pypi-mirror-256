"""The overload function decorates methods in class bodies that are to be
overloaded."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable


def overload(*types) -> Callable:
  """The overload function decorates methods in class bodies that are to be
  overloaded. That function is created by this function, which is why this
  function must not be called when used as a decorator. """

  def decorate(callMeMaybe: Callable) -> Callable:
    """This function actually does the decorating."""

    def __set_name__(self, owner: type, name: str) -> None:
      """By setting this method on the decorated method, we can bring in all
      required functionality for function overloading. """

      clsName = owner.__qualname__
      pvtName = '__overloaded_%s_%s__' % (name, clsName)
      existing = getattr(owner, pvtName, {})
      existing |= {tuple(types): callMeMaybe}
      setattr(owner, pvtName, existing)

    setattr(callMeMaybe, '__overload_signature__', (*types,))
    setattr(callMeMaybe, '__set_name__', __set_name__)
    return callMeMaybe

  return decorate
