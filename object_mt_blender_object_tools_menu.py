import bpy

class OBJECT_MT_BlenderObjectToolsMenu(bpy.types.Menu):
    bl_label = "Blender Object tools"
    bl_idname = "OBJECT_MT_BlenderObjectToolsMenu"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def draw(self, context):
        layout = self.layout

        # Call our custom operator by name. 
        layout.operator(
            "object.arrange_objects_on_grid", 
            text = "Arrange objects")
        
        layout.operator(
                "object.add_property_to_selected", 
                text = "Add property to selected")

def draw_menu(self, context):
    self.layout.menu(OBJECT_MT_BlenderObjectToolsMenu.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_MT_BlenderObjectToolsMenu)
    bpy.types.VIEW3D_MT_object.append(draw_menu)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(draw_menu)
    bpy.utils.unregister_class(OBJECT_MT_BlenderObjectToolsMenu)