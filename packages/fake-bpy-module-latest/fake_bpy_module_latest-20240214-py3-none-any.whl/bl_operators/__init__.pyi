import sys
import typing
from . import vertexpaint_dirt
from . import constraint
from . import sequencer
from . import node
from . import image
from . import uvcalc_lightmap
from . import freestyle
from . import uvcalc_transform
from . import mesh
from . import geometry_nodes
from . import object_quick_effects
from . import bmesh
from . import object_align
from . import assets
from . import screen_play_rendered_anim
from . import wm
from . import file
from . import console
from . import anim
from . import object
from . import uvcalc_follow_active
from . import clip
from . import userpref
from . import add_mesh_torus
from . import rigidbody
from . import presets
from . import object_randomize_transform
from . import view3d
from . import spreadsheet

GenericType = typing.TypeVar("GenericType")

def register(): ...
def unregister(): ...
