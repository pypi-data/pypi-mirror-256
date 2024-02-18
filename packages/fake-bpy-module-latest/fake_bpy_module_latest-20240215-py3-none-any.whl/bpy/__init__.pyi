import sys
import typing
import bpy.types

from . import types
from . import ops
from . import props
from . import path
from . import msgbus
from . import utils
from . import app

GenericType = typing.TypeVar("GenericType")
context: "bpy.types.Context"

data: "bpy.types.BlendData"
""" Access to Blender's internal data
"""
