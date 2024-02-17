"""The applyEnv function loads the environment files and applies their
data to the current environment. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

from vistutils import loadEnv


def applyEnv() -> None:
  """The applyEnv function loads the environment files and applies their
  data to the current environment. """

  data = loadEnv()
  for (key, val) in data.items():
    os.environ[key] = val
