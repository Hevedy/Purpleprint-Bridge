bl_info = {
    "name": "Purpleprint Bridge (Unreal)",
    "blender": (4, 0, 0),
    "category": "Object",
    "version": (1, 4),
    "author": "Hevedy",
    "description": "Export entities visible to Unreal Engine CSV",
    "license": "GPL-3.0"
}

# ===========================================================================
# Purpleprint - Bridge (Blender/Unreal) by Hevedy <https://github.com/Hevedy>
# Repo <https://github.com/Hevedy/Purpleprint-Bridge>
# 
# GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
# Copyright (c) 2015-2025 Hevedy <https://www.hevedy.com/>
# ===========================================================================
# 
# ================================================
# PurpleprintBridge.py
# ================================================
# 
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this script.  If not, see <https://www.gnu.org/licenses/>.

import bpy
import csv
import math
import os
from bpy.props import BoolProperty, StringProperty, CollectionProperty, PointerProperty, EnumProperty
from bpy.types import PropertyGroup, UIList

class CollectionItem(PropertyGroup):
    name: StringProperty()
    use: BoolProperty(default=False)

class PurpleprintBridgePreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Collection filter moved to main panel.")

class EXPORT_OT_entity_csv_unreal(bpy.types.Operator):
    bl_idname = "export.entity_csv_unreal"
    bl_label = "Export Purple CSV"
    bl_description = "Export visible entities in viewport to CSV"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        path = context.scene.unreal_export_path
        if not path:
            path = bpy.path.abspath("//purpleprint_entities.csv")
            #self.report({'ERROR'}, "No export path set. Use 'Set Export Path' first.")
            #return {'CANCELLED'}

        rows = []
        index = 1

        def collect_objects(obj):
            # Only export non hiden to render objects and non null
            if obj.hide_render:
                return []
            
            collected = []

            for child in obj.children:
                collected += collect_objects(child)

            if obj.type != 'EMPTY' and obj.data is not None:
                collected.append(obj)

            return collected

        export_mode = context.scene.export_mode
        allowed_collections = [item.name for item in context.scene.collection_filter if item.use]

        def is_in_allowed_collection(obj):
            return any(col.name in allowed_collections for col in obj.users_collection)

        # Get all valid objects and childs
        all_objects = []
        for obj in context.scene.objects:
            if obj.parent is None:
                all_objects += collect_objects(obj)

        for obj in all_objects:
            if obj.type == 'EMPTY' or obj.data is None:
                continue  # skip empty
            if export_mode == 'FILTERED' and not is_in_allowed_collection(obj):
                continue
            
            name = obj.name
            model_name = obj.data.name
            entity_type = f"{obj.type} ({model_name})"

            mat = obj.matrix_world
            loc = mat.to_translation()
            rot = mat.to_euler()
            scale = mat.to_scale()

            # Apply Unreal unit scale (Blender units are in meters, Unreal uses centimeters)
            loc_cm = loc * 100
            scale_cm = scale * 100

            # Unreal format
            location = f"(X={loc_cm.x:.6f},Y={loc_cm.y:.6f},Z={loc_cm.z:.6f})"
            # Convert radians to degrees, reorder rotation as Pitch(Y), Yaw(Z), Roll(X)
            pitch = math.degrees(rot.x)
            yaw = math.degrees(rot.z)
            roll = math.degrees(rot.y)
            rotation = f"(Pitch={pitch:.6f},Yaw={yaw:.6f},Roll={roll:.6f})"
            scale_str = f"(X={scale_cm.x:.6f},Y={scale_cm.y:.6f},Z={scale_cm.z:.6f})"

            row = [f"Row_{index}", name, entity_type, location, rotation, scale_str]
            rows.append(row)
            index += 1

        # Default root if not defined
        #if not self.filepath:
        #    self.filepath = bpy.path.abspath("//export_entities.csv")

        try:
            with open(path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(["---", "Name", "Type", "Location", "Rotation", "Scale"])
                writer.writerows(rows)
            self.report({'INFO'}, f"CSV exported: {path}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to write CSV: {str(e)}")
            return {'CANCELLED'}

        return {'FINISHED'}


class EXPORT_OT_update_collection_list(bpy.types.Operator):
    bl_idname = "export.update_collection_list"
    bl_label = "Update Collection List"

    def execute(self, context):
        scene = context.scene
        scene.collection_filter.clear()
        for col in bpy.data.collections:
            item = scene.collection_filter.add()
            item.name = col.name
            item.use = False
        return {'FINISHED'}

class EXPORT_PT_entity_csv_unreal_panel(bpy.types.Panel):
    bl_label = "Purpleprint Bridge (Unreal)"
    bl_idname = "EXPORT_PT_entity_csv_unreal_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Purpleprint Bridge'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.separator()

        # Export Mode
        row = layout.row(align=True)
        row.prop(scene, "export_mode", expand=True)

        if scene.export_mode == 'FILTERED':
            # Update
            layout.operator("export.update_collection_list", icon='FILE_REFRESH')

            # Collections list
            box = layout.box()
            for item in scene.collection_filter:
                row = box.row()
                row.prop(item, "use", text=item.name, toggle=True)

        layout.separator()
        layout.operator("export.entity_csv_unreal", icon='EXPORT')
        layout.separator()
        layout.prop(scene, "unreal_export_path")

classes = [
    CollectionItem,
    PurpleprintBridgePreferences,
    EXPORT_OT_entity_csv_unreal,
    EXPORT_OT_update_collection_list,
    EXPORT_PT_entity_csv_unreal_panel,
]

def register_scene_props():
    bpy.types.Scene.collection_filter = CollectionProperty(type=CollectionItem)
    bpy.types.Scene.export_mode = EnumProperty(
        name="Export Mode",
        description="Choose export mode",
        items=[
            ('ALL', "Export All", "Export all visible objects"),
            ('FILTERED', "Export By Collections", "Export only selected collections")
        ],
        default='ALL'
    )
    bpy.types.Scene.unreal_export_path = StringProperty(
        name="CSV Export Path",
        description="File path for exporting CSV",
        subtype='FILE_PATH'
    )

def unregister_scene_props():
    del bpy.types.Scene.unreal_export_path
    del bpy.types.Scene.collection_filter
    del bpy.types.Scene.export_mode

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_scene_props()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    unregister_scene_props()

if __name__ == "__main__":
    register()
