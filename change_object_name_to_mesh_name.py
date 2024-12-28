import bpy

bl_info = {
    "name": "Change object name to mesh name",
    "author": "Thorben Baerentson",
    "description": "Change the name of the object to the name of the first mesh, that can be found in the objects hierachy",
    "blender": (4, 00, 0),
    "category": "Object",
}

class ChangeObjectNameToMeshName(bpy.types.Operator):
    """Change the name of the object to the name of the first mesh, that can be found in the objects hierachy"""
    bl_idname = "object.change_object_name_to_mesh_name"
    bl_label = "Change object name to mesh name"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
       
    def get_material(self):
        for m in bpy.data.materials:
            if m.name == self.property_materials:
                return m
    
    def get_children(self, obj): 
        children = [] 
        for ob in bpy.data.objects: 
            if ob.parent == obj: 
                children.append(ob) 

        return children 

    def get_mesh_name(self, obj): 
        for o in self.get_children(obj):
            if o.type == 'MESH':
                return o.name
            
            r = self.get_mesh_name(o)
            if r is not None:
                return r
        
        None

    def execute(self, context):
        for o in context.selected_objects:
            name = self.get_mesh_name(o)
            if name is not None:
                o.name = name     
            
        return { "FINISHED" }
    
    def get_items(self, context):
        result = []
        for m in bpy.data.materials:
            result.append((m.name, m.name, "A material"))

        return result


def menu_func(self, context):
    self.layout.operator(ChangeObjectNameToMeshName.bl_idname, text = ChangeObjectNameToMeshName.bl_label)


# Register and add to the "object" menu.
def register():
    bpy.utils.register_class(ChangeObjectNameToMeshName)


def unregister():
    bpy.utils.unregister_class(ChangeObjectNameToMeshName)