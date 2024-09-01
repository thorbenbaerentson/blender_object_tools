# If these two lines cause in error inside you IDE: Don´t worry.
import bpy
from bpy.props import StringProperty, EnumProperty, IntProperty

# Needed to register each module.
import sys
import importlib

# This is a sample add-on to demonstrate how add-ons are implemented in Blender. The functionality itself is 
# redundant since blender already implents this behavior. However, it shows how to:
# - implemented an operator as an add-on, 
# - integrate it into the blender menus
# - how to separate an add-on into separate files and use them
#
# Therefore it can serve as a template for blender add-on development.
#
# Tips:
# If you start out with add-on development make sure to enable 'Python Tooltips' and 'Development Extras' under:
# Edit -> Preferences -> Interface.
# With the functionality enabled you can right click on a menu item and review its code. This is helpful,
# if you want to integrate your operators with the existing blender UI. 

# Provide Blender with Meta-Data for your add-on. This is required for single file add-ons. 
bl_info = {
    "name": "Blender Object tools",
    "author": "Thorben Baerentson",
    "description": "This addon contains several tools that makes managing objects easier.",
    "blender": (4, 00, 0),
    "category": "Object",
}

# Add further modules here. In this context each module must be a single python-file
# with its own register and unregister function.
# Further reading: 
# https://b3d.interplanety.org/en/creating-multifile-add-on-for-blender/
modulesNames = [
    'arrange_objects_on_grid',
    'add_property_to_selected',
    'object_mt_blender_object_tools_menu',
]

# Get the full name for each module and append it to modulesFullNames ...
modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
 
# ... then import or reload these modules.
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)

# Register all modules found using the register method defined in the imported module.
def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

# Unregister all modules we´ve imported using the unregister method defined in the imported module.
def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()