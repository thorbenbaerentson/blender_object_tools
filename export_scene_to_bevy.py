import bpy
import os
from bpy.props import StringProperty
from mathutils import Vector

bl_info = {
    "name": "Export to bevy",
    "author": "Thorben Baerentson",
    "description": "Export current scene to bevy as gltf and prepare a repository of all items in the file as csv",
    "blender": (4, 00, 0),
    "category": "Object",
}


class ExportSceneToBevy(bpy.types.Panel):
    bl_idname = "object_export_to_bevy_panel"
    bl_label = "Bevy tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Bevy"

    def draw(self, context):
        self.layout.prop(context.scene, "Export_Path")

class ExportSceneToBevyPanel(bpy.types.Operator):
    """Export current scene to bevy as gltf and prepare a repository of all items in the file as csv"""
    bl_idname = "object.export_scene_to_bevy"
    bl_label = "Export to bevy"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
           
    # def invoke(self, context, event):
    #     wm = context.window_manager
    #     return wm.invoke_props_dialog(self)

    def execute(self, context):
        objects = ""
        file = context.scene["Export_Path"] + context.scene.name.lower() + ".csv"
        target = context.scene["Export_Path"] + context.scene.name.lower() + ".glb"

        for o in bpy.context.scene.objects:
            o.location = Vector((0.0, 0.0, 0.0))
            objects += o.name
            objects +=  "\n"
            o.select_set(state = True)        

        with open(file, "w") as text_file:
            text_file.write(objects)
       
        return bpy.ops.object.arrange_objects_on_grid()

def menu_func(self, context):
    self.layout.operator(ExportSceneToBevy.bl_idname, text = ExportSceneToBevy.bl_label)


# Register and add to the "object" menu.
def register():
    bpy.utils.register_class(ExportSceneToBevy)
    bpy.utils.register_class(ExportSceneToBevyPanel)
    bpy.types.Scene.Export_Path = StringProperty(name = "Path", description = "Choose a directory:", subtype = 'DIR_PATH')


def unregister():
    del bpy.types.Scene.Export_Path
    bpy.utils.unregister_class(ExportSceneToBevy)
    bpy.utils.unregister_class(ExportSceneToBevyPanel)