import bpy
import math

from bpy.props import StringProperty, EnumProperty, IntProperty
from queue import PriorityQueue

bl_info = {
    "name": "Arrange objects on grid",
    "author": "Thorben Baerentson",
    "description": "Tries to arrange all selected objects on a grid based on the dimension of the object.",
    "blender": (4, 00, 0),
    "category": "Object",
}

class ComparatorableItem:
    def __init__(self, object):
        self.object = object

    def __lt__(self, other):
        return self.object.name < other.object.name

class ArrangeObjectsOnGrid(bpy.types.Operator):
    """Tries to arrange all selected objects on a grid based on the dimension of the object."""
    bl_idname = "object.arrange_objects_on_grid"
    bl_label = "Arrange objects on grid"
    
    margin = 2.0

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
    
    def execute(self, context):
        objects = PriorityQueue()
        obj_count = 0
        overall_y = 0.0
        
        for o in context.selected_objects:
            # Ignore empties, we cannot see them anyway.
            if o.type == "EMPTY":
                continue
            
            # We expect all objects to be parented to an empty. 
            # If the parent is not None and parent is not an empty
            # the current object is not a 'main' object.
            if o.parent is not None and o.parent.type != "EMPTY":
                continue
            
            objects.put((o.dimensions.y, ComparatorableItem(o)))
            obj_count += 1
            overall_y = max(o.dimensions.y, overall_y)        
            
        columns = int(math.ceil(math.sqrt(obj_count)))
        rows = columns
        
        column_max = -1.0
        next_x = 0.0
        next_y = 0.0
        row = 0
        max_y = overall_y * 3
        
        while not objects.empty():
            o = objects.get()[1].object
            if o.dimensions is None:
                continue
                
            o.location = (next_x, next_y + o.dimensions.y, 0)
            
            column_max = max(column_max, o.dimensions.x)
            next_y += o.dimensions.y + self.margin
            row += 1
            
            if next_y >= max_y:
                next_y = 0.0
                next_x += column_max + self.margin
            
        return { "FINISHED" }


def menu_func(self, context):
    self.layout.operator(ArrangeObjectsOnGrid.bl_idname, text = ArrangeObjectsOnGrid.bl_label)

# Register and add to the "object" menu.
def register():
    bpy.utils.register_class(ArrangeObjectsOnGrid)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ArrangeObjectsOnGrid)
    bpy.types.VIEW3D_MT_object.remove(menu_func)