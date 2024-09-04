# Table of Contents
- [Introduction](#blender-object-tools)
- [Operators](#operators)
    - [Arrange Objects On Grid](#arrange-objects-on-grid)
    - [Add property to selected](#add-property-to-selected)
- [Known Issues](#known-issues)

# Blender Object Tools
This extension contains operators for Blender that help managing objects in bulk.

# Operators
All operators can be found under Objects :arrow_right: Blender Object Tools in the 'Layout' tab. Keep in mind, that at least one object has to be selected in order for the operators to work.

## Arrange Objects On Grid
This operator uses a simple heuristic to arrange all selected objects on a plane taking with and height of the objects into account. This should arrange all objects so that there are no overlapping objects. The origin of the plane is always the scene origin. 

## Add property to selected
Takes a property name and value and adds this property value on all selected objects. Properties can be added to the object or the data tab. Property values will be exported alongside the object if blender exports .glft or .glb files. Game engines like [Bevy](https://bevyengine.org/) import these property values when loading .gltfs (see [Load gltf extras](https://bevyengine.org/examples/3d-rendering/load-gltf-extras)). This enables us to pump data from Blender to a game engine. 

Think of adding a property called 'Collider' to all objects and setting it to true for all objects, that should serve as a collider. When loading a .gltf you could replace all of objects with a physics object, if the 'Collider' value is true and use a regular mesh renderer if not. This opens up almost infinite possibilities to interact with a game engine from Blender. Actually this should enable us to turn Blender into a Level Editor for engines like [Bevy](https://bevyengine.org/).

# Known Issues
- The menu item 'Asset Tools' should be grayed out when no object is selected. However, implementing 'poll' for a menu object does not seam to suffice in order to achive it.  
- The objects are not move exactly to the origin, there is still an offset. 
