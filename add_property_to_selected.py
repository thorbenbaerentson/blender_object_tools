import bpy
from bpy.props import StringProperty, EnumProperty, IntProperty, FloatProperty, BoolProperty

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
    
    def strtobool (self, val):
        """Convert a string representation of truth to true (1) or false (0).
        True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
        are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
        'val' is anything else.
        """
        val = val.lower()
        if val in ('y', 'yes', 't', 'true', 'on', '1'):
            return True
        elif val in ('n', 'no', 'f', 'false', 'off', '0'):
            return False
        else:
            raise ValueError("invalid truth value %r" % (val,))

    def execute(self, context):
        for o in context.selected_objects:
            value = None
            if self.property_type == "String":
                value = self.property_value
            
            if self.property_type == "Integer":
                value = int(self.property_value)

            if self.property_type == "Float":
                value = float(self.property_value)

            if self.property_type == "Bool":
                value = self.strtobool(self.property_value)
            
            if self.property_space == "Object":
                o[self.property_name] = value
                continue
            
            if self.property_space == "Data":
                o.data[self.property_name] = value
                continue
            
        return { "FINISHED" }
    
    def get_property_spaces(self, context):
        return (
            ("Object", "Object", "Store under object"),
            ("Data", "Data", "Store under data"),
        )
    
    def get_property_types(self, context):
        return (
            ("String", "String", "String"),
            ("Integer", "Integer", "Integer"),
            ("Float", "Float", "Float"),
            ("Bool", "Bool", "Bool"),
        )
    
    property_name : StringProperty(default = "Name", name = "Property Name")
    property_value : StringProperty(default = "Test", name = "Value")
    property_type : EnumProperty(items = get_property_types, name = "Property type")
    property_space : EnumProperty(items = get_property_spaces, name = "Property space")


def menu_func(self, context):
    self.layout.operator(AddPropertyToSelected.bl_idname, text = AddPropertyToSelected.bl_label)


# Register and add to the "object" menu.
def register():
    bpy.utils.register_class(AddPropertyToSelected)


def unregister():
    bpy.utils.unregister_class(AddPropertyToSelected)