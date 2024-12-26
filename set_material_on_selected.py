import bpy
from bpy.props import StringProperty, EnumProperty, IntProperty

bl_info = {
    "name": "Change material on selected",
    "author": "Thorben Baerentson",
    "description": "Set the material on all selected objects to a specific one",
    "blender": (4, 00, 0),
    "category": "Object",
}

class ChangeMaterialOnSelected(bpy.types.Operator):
    """Set the material on all selected objects to a specific one"""
    bl_idname = "object.change_material_on_selected"
    bl_label = "Change material on selected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def get_material(self):
        for m in bpy.data.materials:
            if m.name == self.property_materials:
                return m

    def execute(self, context):
        for o in context.selected_objects:
            if o.type == 'MESH' :
                o.data.materials[self.property_material_id] = self.get_material()      
            
        return { "FINISHED" }
    
    def get_items(self, context):
        result = []
        for m in bpy.data.materials:
            result.append((m.name, m.name, "A material"))

        return result
    
    property_material_id : IntProperty(default = 0, name = "Material index")
    property_materials : EnumProperty(items = get_items, name = "Material")


def menu_func(self, context):
    self.layout.operator(ChangeMaterialOnSelected.bl_idname, text = ChangeMaterialOnSelected.bl_label)


# Register and add to the "object" menu.
def register():
    bpy.utils.register_class(ChangeMaterialOnSelected)


def unregister():
    bpy.utils.unregister_class(ChangeMaterialOnSelected)