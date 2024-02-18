import sys
import typing
import bpy.types

from . import types
from . import path
from . import ops
from . import msgbus
from . import app
from . import utils
from . import props

GenericType = typing.TypeVar("GenericType")
context: "bpy.types.Context"

data: "bpy.types.BlendData"
""" Access to Blender's internal data
"""
