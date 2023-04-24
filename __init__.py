import bpy
from bpy.utils import (register_class, unregister_class)
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
import subprocess
import os
import sys

bl_info = {
    "name": "Export Panda3D BAM",
    "description": "Exports to Panda3D BAM",
    "author": "Addon by Theanine3D. blend2bam by Moguri",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "category": "Import-Export",
    "location": "File > Export",
    "support": "COMMUNITY"
}

class BAMPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    python_path: StringProperty(
        name="Python Path",
        description="Absolute path of the Python executable used by Panda3D. Usually inside the 'python' folder in your main Panda3D installation folder",
        default="C:\\Panda3D\\python\\python.exe",
        subtype='FILE_PATH'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "python_path")

def display_msg_box(message="", title="Info", icon='INFO'):
    ''' Open a pop-up message box to notify the user of something               '''
    ''' Example:                                                                '''
    ''' display_msg_box("This is a message", "This is a custom title", "ERROR") '''

    def draw(self, context):
        lines = message.split("\n")
        for line in lines:
            self.layout.label(text=line)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def writeBAM(context, filepath, selected_only, material_mode, physics_engine, pipeline, no_srgb, texture_mode, anim_mode, invisible_coll):
    blender_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    current_filepath = bpy.data.filepath
    if current_filepath == "":
        display_msg_box(message="You must first save your Blender file to your hard drive.", title="Info", icon='INFO')
        return {'FINISHED'}
    current_dir = os.path.dirname(current_filepath)
    current_filename = os.path.basename(current_filepath)
    source_file = bpy.data.filepath
    # if selected_only:
    #     new_filename = os.path.splitext(current_filename)[0] + "_TMP" + os.path.splitext(current_filename)[1]
    #     new_filepath = os.path.join(current_dir, new_filename)
    #     selected_objects = bpy.context.selected_objects
    #     bpy.ops.wm.save_as_mainfile(filepath=new_filepath, check_existing=False, copy=False)
    #     for obj in bpy.context.selected_objects:
    #         obj.select_set(False)
    #         if obj not in selected_objects:
    #             try:
    #                 bpy.data.objects.remove(obj)
    #             except:
    #                 continue
    #     bpy.ops.wm.open_mainfile(filepath=current_filepath)
    #     source_file = os.path.basename(new_filepath)
    command = [bpy.context.preferences.addons[__name__].preferences.python_path, "-m", "blend2bam", source_file, filepath, "--material-mode", material_mode, "--physics-engine", physics_engine, "--blender-dir", blender_dir, "--pipeline", pipeline, "--textures", texture_mode, "--animations", anim_mode, "--invisible-collisions-collection", invisible_coll]
    if no_srgb:
        command.append("--no-srgb")
    
    subprocess.Popen(command, shell=True)

    print("\nCleaning up...\n")
    # os.remove(new_filepath)

    return {'FINISHED'}

class ExportBAM(Operator, ExportHelper):
    """Exports to the Panda3D BAM format"""
    bl_idname = "export.bam"
    bl_label = "Panda3D (.bam)"

    filename_ext = ".bam"

    filter_glob: StringProperty(
        default="*.bam",
        options={'HIDDEN'},
        maxlen=255,
    )

    selected_only: BoolProperty(
        name="Selected Only",
        description="Exports only the currently selected objects, instead of the whole scene",
        default=False,
    )
    material_mode: EnumProperty(
        name="Material Mode",
        description="The mode for exporting materials - physically-based or legacy (default: pbr)",
        items=(
            ('legacy', "Legacy", "The older legacy (non-PBR) material mode in Panda3D"),
            ('pbr', "PBR", "The newer physically-based material mode in Panda3D"),
        ),
        default='pbr',
    )
    physics_engine: EnumProperty(
        name="Physics Engine",
        description="The physics engine to build collision solids for (default: builtin)",
        items=(
            ('builtin', "Built-In", "The built-in physics engine in Panda3D"),
            ('bullet', "Bullet", "Bullet is a third-party open source physics engine used in many games and simulations"),
        ),
        default='builtin',
    )
    pipeline: EnumProperty(
        name="Pipeline",
        description="the backend pipeline used to convert files (default: gltf)",
        items=(
            ('gltf', "gltf", "glTF - GL Transmission Format"),
            ('egg', "egg", "egg - 3D model format used by Panda3D"),
        ),
        default='gltf',
    )
    no_srgb: BoolProperty(
        name="No sRGB",
        description="If checked, textures will not be loaded as sRGB textures (only for glTF pipelines) (default: Disabled)",
        default=False,
    )
    texture_mode: EnumProperty(
        name="Texture Mode",
        description="How to handle external textures (default: Reference)",
        items=(
            ('ref', "Reference", "References textures via their original file path"),
            ('copy', "Copy", "Copies textures to the destination folder"),
            ('embed', "Embed", "Embeds textures into the resulting exported BAM"),
        ),
        default='ref',
    )
    anim_mode: EnumProperty(
        name="Animation Mode",
        description="How to handle animations (default: Embed)",
        items=(
            ('embed', "Embed", "Embeds textures into the resulting exported BAM"),
            ('separate', "Separate", "Separates animations into individual files"),
            ('skip', "Skip", "Skips animation export entirely"),
        ),
        default='embed',
    )
    invisible_coll: StringProperty(
        name="Invisible Collection",
        description="Name of a collection in Blender whose collision objects will be exported without a visible geom node (default: InvisibleCollisions)",
        default="InvisibleCollisions",
    )

    def execute(self, context):
        return writeBAM(context, self.filepath, self.selected_only, self.material_mode, self.physics_engine, self.pipeline, self.no_srgb, self.texture_mode, self.anim_mode, self.invisible_coll)

def menu_func_export(self, context):
    self.layout.operator(ExportBAM.bl_idname, text="Panda3D (.bam)")

def register():
    bpy.utils.register_class(ExportBAM)
    bpy.utils.register_class(BAMPrefs)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportBAM)
    bpy.utils.unregister_class(BAMPrefs)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    bpy.ops.export.writeBAM('INVOKE_DEFAULT')
