"""The EZSpace provides the namespace object used by the EZMeta metaclass
to create the EZData class."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import builtins

from icecream import ic

from morevistutils.metas import BaseNamespace

ic.configureOutput(includeContext=True)


class EZSpace(BaseNamespace):
  """The EZSpace provides the namespace object used by the EZMeta metaclass
  to create the EZData class."""

  @staticmethod
  def _getGlobals() -> dict:
    """Getter-function for globals"""
    base = {}
    for (key, val) in builtins.__dict__.items():
      if isinstance(val, type):
        base |= {key: val}
    return {**globals(), **base}

  def getCallables(self) -> dict:
    """Getter-function for the dictionary containing the functions"""
    out = {}
    for (key, val) in dict.items(self, ):
      if callable(val):
        out |= {key: val}
    return out

  @classmethod
  def resolveType(cls, typeName: str) -> type:
    """Resolves the name to the type"""
    if isinstance(typeName, type):
      return typeName
    type_ = cls._getGlobals().get(typeName, None)
    if type_ is None:
      raise NameError(typeName)
    if isinstance(type_, type):
      return type_
    raise TypeError(typeName)

  def getAnnotations(self) -> dict:
    """Getter-function for annotations."""
    out = {}
    annotations_ = BaseNamespace.getAnnotations(self)

    for (key, val) in annotations_.items():
      out |= {key: self.resolveType(val)}
    return out
