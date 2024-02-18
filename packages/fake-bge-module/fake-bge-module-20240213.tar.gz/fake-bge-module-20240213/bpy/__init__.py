import sys
import typing
import bpy.types

from . import ops
from . import types
from . import path
from . import app
from . import props
from . import utils
from . import msgbus

GenericType = typing.TypeVar("GenericType")
context: 'bpy.types.Context' = None

data: 'bpy.types.BlendData' = None
''' Access to Blender's internal data
'''
