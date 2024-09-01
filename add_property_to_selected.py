import bpy
from bpy.props import StringProperty, EnumProperty, IntProperty

bl_info = {
    "name": "Add property to selected",
    "author": "Thorben Baerentson",
    "description": "Add or set a property value on all selected objects under object or data",
    "blender": (4, 00, 0),
    "category": "Object",
}

class AddPropertyToSelected(bpy.types.Operator):
    """Add or set a property value on all selected objects under object or data"""
    bl_idname = "object.add_property_to_selected"
    bl_label = "Add property to selected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        for o in context.selected_objects:
            if self.property_space == "Object":
                o[self.property_name] = self.property_value
                continue
            
            if self.property_space == "Data":
                o.data[self.property_name] = self.property_value
                continue
            
            
        return { "FINISHED" }
    
    def get_items(self, context):
        return (
            ("Object", "Object", "Store under object"),
            ("Data", "Data", "Store under data"),
        )
    
    property_name : StringProperty(default = "Type", name = "Type")
    property_value : StringProperty(default = "Test", name = "Value")
    property_space : EnumProperty(items = get_items, name = "Property space")


def menu_func(self, context):
    self.layout.operator(AddPropertyToSelected.bl_idname, text = AddPropertyToSelected.bl_label)


# Register and add to the "object" menu.
def register():
    bpy.utils.register_class(AddPropertyToSelected)


def unregister():
    bpy.utils.unregister_class(AddPropertyToSelected)