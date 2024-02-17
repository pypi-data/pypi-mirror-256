"""The EZMeta is the metaclass used by the EZData class ensuring the
dataclass behaviour. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from icecream import ic
from vistutils import monoSpace
from vistutils.metas import AbstractMetaclass, Bases

from morevistutils.ezdata import EZSpace, EZField

ic.configureOutput(includeContext=True)


class EZMeta(AbstractMetaclass):
  """The EZMeta is the metaclass used by the EZData class ensuring the
  dataclass behaviour. """

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> EZSpace:
    """Creates the namespace object"""
    return EZSpace(mcls, name, bases, **kwargs)

  def __new__(mcls, name: str, bases: Bases, namespace: EZSpace,
              **kwargs) -> type:
    """Creates the dataclass"""
    for base in bases:
      if base.__qualname__ != 'EZData':
        e = """EZData is the only allowed baseclass!"""
        raise TypeError(e)
    slots = namespace.getAnnotations()
    calls = namespace.getCallables()
    for (name, slot) in slots.items():
      if name in calls:
        e = """Duplicated name between slot and callable!"""
        raise NameError(e)
    if '__init__' in calls and name != 'EZData':
      e = """Subclasses of EZData are not allowed to implement __init__!"""
      raise AttributeError(monoSpace(e))
    cls = AbstractMetaclass.__new__(mcls, name, (), calls, **kwargs)
    ezFields = {}
    for (key, val) in slots.items():
      field = EZField(val)
      setattr(cls, key, field)
      ezFields |= {key: field}
    setattr(cls, '__ez_fields__', ezFields)
    return cls

  def __init__(cls, name, _, attrs, **kwargs) -> None:
    AbstractMetaclass.__init__(cls, name, (), attrs, **kwargs)

  def __call__(cls, *args, **kwargs) -> Any:
    ezFields = getattr(cls, '__ez_fields__')
    self = object.__new__(cls)
    for (arg, (key, field)) in zip(args, ezFields.items()):
      field.__set__(self, EZField._typeGuard(field, arg))
    return self

  def __str__(cls, ) -> str:
    """String representation"""
    clsName = cls.__qualname__
    names = [arg.__field_name__ for arg in getattr(cls, '__ez_fields__')]
    fieldNames = ', '.join(names)
    return '%s(%s)' % (clsName, fieldNames)
