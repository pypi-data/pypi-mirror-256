"""The loadEnv function loads the environment files located at project
root."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from morevistutils import getEnvFiles


def loadEnv() -> dict:
  """The loadEnv function loads the environment files located at project
  root."""

  with open(getEnvFiles(), 'r') as f:
    lines = f.readlines()

  lines = [line.strip() for line in lines]
  lines = [line for line in lines if not line.startswith('#')]
  lines = [line for line in lines if '=' in line]

  data = {}
  for line in lines:
    for (i, char) in enumerate(line):
      if char == '=':
        data[line[:i]] = line[i + 1:]
        break

  return data
