"""A little imp, rigged with twelve bones and a looping walk clip.

`spawnite model make imp` runs this in an empty scene, then exports the whole
scene, so the script builds the model and nothing else. Blender is Z up and
the imp faces -Y, which the export turns into glTF's +Z front.
"""

import math

import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

scene = bpy.context.scene
scene.render.fps = 30
# 24 frames at 30 fps: a 0.8 s step cycle.
scene.frame_start = 0
scene.frame_end = 24


def add_material(name, color):
    material = bpy.data.materials.new(name)
    surface = next(
        node
        for node in material.node_tree.nodes
        if node.type == "BSDF_PRINCIPLED"
    )
    surface.inputs["Base Color"].default_value = (*color, 1)
    surface.inputs["Roughness"].default_value = 0.8
    return material


materials = [
    add_material("imp_body", (0.105, 0.05, 0.238)),
    add_material("imp_belly", (0.332, 0.227, 0.552)),
    add_material("accent", (1, 0.144, 0.014)),
    add_material("dark", (0.023, 0.016, 0.03)),
    add_material("bone", (0.863, 0.776, 0.597)),
]
BODY, BELLY, ACCENT, DARK, BONE = range(len(materials))

# Each bone: its head, its tail and its parent. The mesh parts below are
# bound rigidly, each to one bone.
bones = {
    "root": ((0, 0, 0), (0, 0, 0.1), None),
    "hips": ((0, 0, 0.2), (0, 0, 0.32), "root"),
    "spine": ((0, 0, 0.32), (0, 0, 0.44), "hips"),
    "head": ((0, 0, 0.44), (0, 0, 0.66), "spine"),
    "arm.L": ((0.17, 0, 0.42), (0.27, -0.02, 0.24), "spine"),
    "arm.R": ((-0.17, 0, 0.42), (-0.27, -0.02, 0.24), "spine"),
    "leg.L": ((0.09, 0, 0.2), (0.1, 0, 0.06), "hips"),
    "foot.L": ((0.1, 0, 0.06), (0.1, -0.1, 0.02), "leg.L"),
    "leg.R": ((-0.09, 0, 0.2), (-0.1, 0, 0.06), "hips"),
    "foot.R": ((-0.1, 0, 0.06), (-0.1, -0.1, 0.02), "leg.R"),
    "tail": ((0, 0.14, 0.24), (0, 0.3, 0.18), "hips"),
    "tail.001": ((0, 0.3, 0.18), (0, 0.44, 0.28), "tail"),
}
bone_names = list(bones)

mesh = bpy.data.meshes.new("imp")
body = bpy.data.objects.new("imp", mesh)
scene.collection.objects.link(body)
for material in materials:
    mesh.materials.append(material)
for name in bone_names:
    body.vertex_groups.new(name=name)

shape = bmesh.new()
weights = shape.verts.layers.deform.verify()


def bind(geometry, bone, material):
    """Gives the new part its material and binds it wholly to one bone."""
    group = bone_names.index(bone)
    for vertex in (item for item in geometry if isinstance(item, bmesh.types.BMVert)):
        vertex[weights][group] = 1.0
    for face in {face for vertex in geometry if isinstance(vertex, bmesh.types.BMVert) for face in vertex.link_faces}:
        face.material_index = material


def add_blob(bone, material, center, size, rotation=(0, 0, 0), segments=16, rings=12):
    """An ellipsoid: a sphere scaled to `size` radii and turned by `rotation`."""
    matrix = (
        Matrix.Translation(center)
        @ Euler(rotation).to_matrix().to_4x4()
        @ Matrix.Diagonal((*size, 1))
    )
    made = bmesh.ops.create_uvsphere(
        shape, u_segments=segments, v_segments=rings, radius=1, matrix=matrix
    )
    bind(made["verts"], bone, material)


def add_spike(bone, material, base, tip, radius, segments=12):
    """A cone from a round base at `base` to a point at `tip`."""
    direction = Vector(tip) - Vector(base)
    turn = direction.to_track_quat("Z", "Y").to_matrix().to_4x4()
    matrix = Matrix.Translation(Vector(base) + direction / 2) @ turn
    made = bmesh.ops.create_cone(
        shape,
        cap_ends=True,
        segments=segments,
        radius1=radius,
        radius2=0,
        depth=direction.length,
        matrix=matrix,
    )
    bind(made["verts"], bone, material)


# The body and its belly.
add_blob("hips", BODY, (0, 0.01, 0.3), (0.19, 0.16, 0.17))
add_blob("spine", BELLY, (0, -0.08, 0.3), (0.13, 0.09, 0.13))
add_blob("spine", BODY, (0, 0, 0.42), (0.16, 0.13, 0.09))

# The head: a round skull, glowing eyes, a dark mouth, horns and ears.
add_blob("head", BODY, (0, -0.02, 0.56), (0.15, 0.14, 0.13), segments=24, rings=16)
for side in (1, -1):
    add_blob("head", ACCENT, (0.055 * side, -0.14, 0.58), (0.032, 0.02, 0.028), segments=12, rings=8)
    add_blob("head", DARK, (0.055 * side, -0.155, 0.58), (0.012, 0.01, 0.014), segments=8, rings=6)
    add_spike("head", BONE, (0.07 * side, -0.01, 0.66), (0.14 * side, 0.03, 0.72), 0.03)
    add_spike("head", BODY, (0.13 * side, 0.0, 0.57), (0.21 * side, 0.03, 0.62), 0.035)
add_blob("head", DARK, (0, -0.13, 0.5), (0.06, 0.02, 0.02), segments=12, rings=8)
for side in (1, -1):
    add_spike("head", BONE, (0.03 * side, -0.14, 0.505), (0.03 * side, -0.15, 0.485), 0.008, segments=6)

# Arms, each ending in three claws.
for side, bone in ((1, "arm.L"), (-1, "arm.R")):
    add_blob(bone, BODY, (0.2 * side, -0.01, 0.34), (0.05, 0.05, 0.11), rotation=(0, -0.5 * side, 0), segments=12, rings=10)
    add_blob(bone, BODY, (0.25 * side, -0.02, 0.24), (0.045, 0.045, 0.045), segments=12, rings=8)
    for claw in (-1, 0, 1):
        add_spike(bone, DARK, (0.27 * side, -0.04 + 0.02 * claw, 0.21), (0.29 * side, -0.07 + 0.03 * claw, 0.17), 0.01, segments=6)

# Legs and wide dark feet.
for side, leg, foot in ((1, "leg.L", "foot.L"), (-1, "leg.R", "foot.R")):
    add_blob(leg, BODY, (0.095 * side, 0, 0.13), (0.055, 0.055, 0.09), segments=16, rings=10)
    add_blob(foot, DARK, (0.1 * side, -0.05, 0.03), (0.06, 0.09, 0.03), segments=16, rings=10)

# A tail curling up behind, with an arrowhead.
add_spike("tail", BODY, (0, 0.12, 0.25), (0, 0.31, 0.17), 0.035)
add_spike("tail.001", BODY, (0, 0.29, 0.17), (0, 0.44, 0.28), 0.025)
add_spike("tail.001", ACCENT, (0, 0.43, 0.27), (0, 0.5, 0.33), 0.045, segments=4)

shape.to_mesh(mesh)
shape.free()
for polygon in mesh.polygons:
    polygon.use_smooth = True

# The rig, with the body bound to it.
armature = bpy.data.objects.new("imp_rig", bpy.data.armatures.new("imp_rig"))
scene.collection.objects.link(armature)
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode="EDIT")
for name, (head, tail, parent) in bones.items():
    bone = armature.data.edit_bones.new(name)
    bone.head, bone.tail = head, tail
    if parent:
        bone.parent = armature.data.edit_bones[parent]
bpy.ops.object.mode_set(mode="OBJECT")
body.parent = armature
body.modifiers.new("rig", "ARMATURE").object = armature

# The walk: each value is keyed on the quarter steps, and the last pose is
# the first, so the clip loops.
steps = [0, 6, 12, 18, 24]


def key_swing(bone, axis, amplitude, phase=0.0, index=0):
    pose_bone = armature.pose.bones[bone]
    pose_bone.rotation_mode = "XYZ"
    for step, frame in enumerate(steps):
        rotation = [0.0, 0.0, 0.0]
        rotation[axis] = amplitude * math.sin(math.tau * (step / 4 + phase))
        pose_bone.rotation_euler = rotation
        pose_bone.keyframe_insert("rotation_euler", frame=frame)


def key_bob(bone, height):
    pose_bone = armature.pose.bones[bone]
    for step, frame in enumerate(steps):
        # Up twice in a cycle, once on each stride.
        pose_bone.location = (0, abs(math.sin(math.tau * step / 4)) * height, 0)
        pose_bone.keyframe_insert("location", frame=frame)


key_swing("leg.L", 0, math.radians(30))
key_swing("leg.R", 0, math.radians(30), phase=0.5)
key_swing("foot.L", 0, math.radians(15), phase=0.25)
key_swing("foot.R", 0, math.radians(15), phase=0.75)
key_swing("arm.L", 0, math.radians(25), phase=0.5)
key_swing("arm.R", 0, math.radians(25))
key_swing("spine", 1, math.radians(6))
key_swing("head", 1, math.radians(-4))
key_swing("tail", 2, math.radians(20))
key_swing("tail.001", 2, math.radians(25), phase=0.125)
key_bob("hips", 0.02)
armature.animation_data.action.name = "walk"
scene.frame_set(scene.frame_start)
