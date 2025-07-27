bl_info = {
    "name": "USD Object Scatter",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > USD Scatter",
    "description": "Scatter USD prototypes on terrain with options for weights, bounds, and min distance",
    "category": "Object"
}

import bpy
from bpy.props import StringProperty, FloatProperty, IntProperty, CollectionProperty, PointerProperty
from bpy.types import Panel, Operator, PropertyGroup

from .core.scatter import run_usd_scatter

class PrototypeItem(PropertyGroup):
    usd_path: StringProperty(name="USD Path")
    stage_path: StringProperty(name="Stage Path")
    weight: FloatProperty(name="Weight", min=0.0)

class ScatterProperties(PropertyGroup):
    output_path: StringProperty(name="Output USDA Path")
    terrain_asset: StringProperty(name="Terrain USDA File")
    terrain_path: StringProperty(name="Terrain Prim Path", default="/World/Terrain")
    num_instances: IntProperty(name="Number of Instances", default=20, min=1)
    min_distance: FloatProperty(name="Minimum Distance (optional)", default=0.0)
    bounds: FloatProperty(name="XY Bound (optional)", default=0.0)
    prototypes: CollectionProperty(type=PrototypeItem)

class OBJECT_PT_usd_scatter(Panel):
    bl_label = "USD Scatter"
    bl_idname = "OBJECT_PT_usd_scatter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'USD Scatter'

    def draw(self, context):
        layout = self.layout
        props = context.scene.scatter_props

        layout.prop(props, "output_path")
        layout.prop(props, "terrain_asset")
        layout.prop(props, "terrain_path")
        layout.prop(props, "num_instances")
        layout.prop(props, "min_distance")
        layout.prop(props, "bounds")

        layout.label(text="Prototypes")
        for proto in props.prototypes:
            box = layout.box()
            box.prop(proto, "usd_path")
            box.prop(proto, "stage_path")
            box.prop(proto, "weight")

        layout.operator("object.add_prototype")
        layout.operator("object.run_usd_scatter")

class OBJECT_OT_run_usd_scatter(Operator):
    bl_idname = "object.run_usd_scatter"
    bl_label = "Run USD Scatter"

    def execute(self, context):
        props = context.scene.scatter_props
        prototypes = []
        for p in props.prototypes:
            prototypes.append({
                "file": p.usd_path,
                "path": p.stage_path,
                "weight": p.weight
            })

        run_usd_scatter(
            output_path=props.output_path,
            terrain_asset_path=props.terrain_asset,
            terrain_prim_path=props.terrain_path,
            prototypes=prototypes,
            num_instances=props.num_instances,
            min_distance=props.min_distance if props.min_distance > 0 else None,
            bounds=props.bounds if props.bounds > 0 else None
        )
        return {'FINISHED'}

class OBJECT_OT_add_prototype(Operator):
    bl_idname = "object.add_prototype"
    bl_label = "Add Prototype"

    def execute(self, context):
        context.scene.scatter_props.prototypes.add()
        return {'FINISHED'}

classes = (
    PrototypeItem,
    ScatterProperties,
    OBJECT_PT_usd_scatter,
    OBJECT_OT_run_usd_scatter,
    OBJECT_OT_add_prototype,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.scatter_props = PointerProperty(type=ScatterProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.scatter_props