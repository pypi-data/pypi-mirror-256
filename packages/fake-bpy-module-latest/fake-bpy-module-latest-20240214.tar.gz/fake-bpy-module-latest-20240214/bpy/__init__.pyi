import sys
import typing
import bpy.types

from . import ops
from . import types
from . import path
from . import msgbus
from . import app
from . import props
from . import utils

GenericType = typing.TypeVar("GenericType")
context: "bpy.types.Context"

data: "bpy.types.BlendData"
""" Access to Blender's internal data
"""
