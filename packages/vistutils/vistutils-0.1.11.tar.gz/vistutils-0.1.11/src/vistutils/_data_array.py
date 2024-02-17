"""DataArray exposes collected rospy data to the Qt framework. This allows
the data collection from rospy to operate at different rates than the
painting updates on the Qt framework."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import time

from PySide6.QtCore import QRectF, QRect, QPointF

from morevistutils.waitaminute import typeMsg


class DataArray:
  """DataArray exposes collected rospy data to the Qt framework. This allows
  the data collection from rospy to operate at different rates than the
  painting updates on the Qt framework."""

  def __init__(self, *args, **kwargs) -> None:
    self._times = []
    self._values = []
    self._maxLength = 32
    self._tMin = 0
    self._tMax = 10
    self._xMin = 0
    self._xMax = 50

  def callback(self, value: float) -> None:
    """Callback receiving data. This should be disconnected from the paint
    events."""
    if not value == value:
      return
    self._times.append(time.time())
    self._values.append(value)
    if len(self._times) != len(self._values):
      raise ValueError
    while len(self._times) > self._maxLength:
      self._times.pop(0)
      self._values.pop(0)

  def getTimes(self) -> list:
    """Getter-function for the list of times"""
    if not self._times:
      return []
    tMin = min(self._times)
    return [t - tMin for t in self._times]

  def getValues(self) -> list:
    """Getter-function for the list of values"""
    if not self._values:
      return []
    return [v for v in self._values]

  def getUnitValues(self) -> tuple[list, list]:
    """Getter-function for the list of points"""
    T, X = self.getTimes(), self.getValues()
    if not T or not X:
      return [], []
    t0, t1, x0, x1 = min(T), max(T), min(X), max(X)
    if (t1 - t0) * (x1 - x0) < 1e-08:
      raise ZeroDivisionError
    T, X = [t - t0 for t in T], [x - x0 for x in X]
    T, X = [t / (t1 - t0) for t in T], [x / (x1 - x0) for x in X]
    return T, X

  def getPoints(self, pixelSpace: QRectF) -> list:
    """Getter-function for the points"""
    if isinstance(pixelSpace, QRect):
      return self.getPoints(pixelSpace.toRectF())
    if not isinstance(pixelSpace, QRectF):
      e = typeMsg('pixelSpace', pixelSpace, QRectF)
      raise TypeError(e)
    uT, uX = self.getUnitValues()
    width, height = pixelSpace.width(), pixelSpace.height()
    if not uT or not uX:
      return []
    out = []
    for (ut, ux) in zip(uT, uX):
      t, x = ut * width, ux * height
      out.append(QPointF(t, x))
    return out
