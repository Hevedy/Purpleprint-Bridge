bl_info = {
    "name": "Purpleprint Bridge (Unreal)",
    "blender": (4, 0, 0),
    "category": "Object",
    "version": (1, 1, 0),
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

from . import PurpleprintBridge
import bpy

classes = [
    PurpleprintBridge.CollectionItem,
    PurpleprintBridge.PurpleprintBridgePreferences,
    PurpleprintBridge.EXPORT_OT_entity_csv_unreal,
    PurpleprintBridge.EXPORT_OT_update_collection_list,
    PurpleprintBridge.EXPORT_PT_entity_csv_unreal_panel,
]

def register_scene_props():
    bpy.types.Scene.collection_filter = bpy.props.CollectionProperty(type=PurpleprintBridge.CollectionItem)
    bpy.types.Scene.export_mode = bpy.props.EnumProperty(
        name="Export Mode",
        description="Choose export mode",
        items=[
            ('ALL', "Export All", "Export all visible objects"),
            ('FILTERED', "Export By Collections", "Export only selected collections")
        ],
        default='ALL'
    )
    bpy.types.Scene.unreal_export_path = bpy.props.StringProperty(
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
