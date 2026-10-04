# A rig, its clips and a walk

[The imp](imp.py) is a working rigged model: twelve bones, a mesh bound to them, and a `walk` clip that loops. Read it before you rig anything, and build from its shape rather than from memory.

## The rig

- Make an armature object and add its bones in edit mode from a table of head, tail and parent, as the imp's `bones` does. Name each bone for its body part, with `.L` and `.R` for the sides, such as `arm.L`.
- Put a root bone at the origin and hang every other bone from it.
- Bind the mesh with one vertex group per bone, named as the bone. Then parent the mesh to the armature and give it an Armature modifier that points at it.
- A model built from separate parts, such as a knight's armour or a robot, binds each part wholly to one bone, with weight 1, as the imp does. A body with one smooth skin blends the weights where two bones meet.

## Clips

- Name each action for what it does, such as `walk`, `idle` or `attack`: each action is one clip, named as the action is. The first keyframe makes an action, so rename it: `armature.animation_data.action.name = "walk"`.
- For a second clip, make a new action, assign it, key it, then assign the first one back:

    ```python
    walk = armature.animation_data.action
    idle = bpy.data.actions.new("idle")
    armature.animation_data.action = idle
    # Key the idle here.
    armature.animation_data.action = walk
    ```

- End a clip that loops on the pose it starts on.
- Key with `keyframe_insert`, as the imp does. To change the curves it made, such as their interpolation, reach them through the action's slot: `bpy_extras.anim_utils.action_get_channelbag_for_slot(action, slot).fcurves`, with `slot` from `armature.animation_data.action_slot`. Blender 5 has no `action.fcurves`.
- Set `scene.render.fps` and the frame range to fit the clips. The imp's walk is 24 frames at 30 fps, one cycle of two steps in 0.8 s.
- A pose bone's location is in the bone's own space, where Y runs along the bone. On a bone that points up, such as the imp's hips, Y is up.
- End the script on `scene.frame_set(scene.frame_start)`, as the imp does, so the still shows the first pose.

## A walk cycle

A walk stays in place: the game moves the model, and the clip moves only its body. The imp keys every value on the quarter steps of one cycle, with the following motion:

- The legs swing forward and back, half a cycle apart.
- Each foot swings a quarter cycle behind its leg, so it lifts after the leg passes.
- Each arm swings against the leg on its side.
- The hips rise twice a cycle, once on each stride.
- The spine and the head sway a little, and what trails, such as a tail or a cape, swings behind.

The imp's `key_swing` and `key_bob` do this in a few lines each. Copy them, and give a heavier model, such as a knight in armour, a smaller swing and a slower cycle.
