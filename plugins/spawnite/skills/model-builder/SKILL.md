---
name: model-builder
description: Make a 3D model for a game in Blender, such as a character, a creature, a prop or a building, as a script the game keeps. Use it when someone asks to make or change a model, such as "make a knight model", in a project that new_game wrote, or when a game needs a model the asset library does not have.
argument-hint: <the model>
---

You make the model the creator asked for: $ARGUMENTS

A model made here is two files in the game. `models/<name>.py` is a Python script that builds the model with Blender's `bpy`, and `public/assets/<name>.glb` is the model file. You write the script, and `make_model` runs it in the creator's Blender with no window, exports the file and renders a still. The script is the model's one source, so never write the GLB another way.

The name is lowercase words joined by dashes, such as `fire-imp`. It names the script, the file and the model the game places.

## The loop

1. Read the Models page with `read_wiki`, page `learn/models`: the contract every model meets.
2. Write `models/<name>.py`. Before the first script, read [references/finished.md](references/finished.md). For a model that moves, read [references/rig.md](references/rig.md) too.
3. Call `make_model` with the name. When the script throws, the reply is Blender's traceback, which names the script's line: fix it and call again.
4. Look at the still it returns, then at the model in the game, as below. Check the reply's triangles and clips against the contract.
5. Change the script and go back to step 3 until the model looks finished from every side the game shows.

When it is done, show the creator the still and the game screenshot, and say what the model has: its height, its triangles and its clips.

## The script

- Blender starts from an empty scene, and `make_model` exports the whole scene. Build the model and nothing else: no camera, no light, no floor.
- Blender is Z up. Face the model toward −Y, Blender's Front view, and stand it on the origin, in the middle of its footprint.
- End the script with the model built. Do not export, and do not call `sys.exit` or `quit_blender`: that ends Blender before `make_model` exports, and the reply says so.
- A run stops after 5 minutes.
- Write for Blender 5, whose Python differs from most examples online. A new material has its node tree already, so leave `use_nodes` alone. An action keeps its F-curves in layers, so `action.fcurves` fails: [references/rig.md](references/rig.md) says how to reach them.

## See it in the game

Look at the model on a map of its own, so the game's own levels stay as they are. Take the following steps:

1. Write a map named `showroom` with `add_map`, once. When its reply gives lines to paste, paste them where it says.
2. Stand the model on it with `place_props`: `{ "<name>": { "model": "assets/<name>.glb", "position": [0, 0] } }`. A model named by its file needs no registration.
3. Call `screenshot` with the map `showroom` and the camera `{ "angle": "iso", "around": [min, max] }`, then the angles `front` and `back`. `min` and `max` are the model's `bounds.min` and `bounds.max` in `src/models.json`. Frame the box rather than the prop's name, which frames a 4 m box whatever the model's size.

The still shows the shape and each material's base colour, and no roughness, metal or glow. The game shows what the player sees: the engine's light, roughness and glow, and the model's size.

A map's props play none of a model's clips, so the showroom stands the model in its rest pose. In the game, an entity loops one clip by its name: `<Entity model="assets/<name>.glb" animation="walk" />`. Tell the creator which clips the file has, and that the game plays each one by that name.

## Watch it in Blender

When the creator asks to watch the model take shape in their open Blender, build it there too, with the `blender` server of the `blender-live` plugin. [Blender](https://wiki.spawnite.com/learn/blender/#watch-a-model-being-built) on the wiki says how the creator sets it up. The server runs your code in the creator's Blender with no guard, so touch nothing of theirs.

1. Check the server. Call its `get_blendfile_summary_path_info` tool, and use that server's tools for every step below. Find the server by that tool rather than by its name: another Blender server can also be named `blender`, and it has an `execute_blender_code` of its own. When no such tool is listed, tell the creator to set up live mode from the wiki page, and build with no window as usual. When the call fails with `Cannot connect to Blender`, ask the creator to open Blender, with the MCP add-on's Auto Start ticked.
2. Keep the creator's file. The same call returns `filepath` and `is_dirty`. When `is_dirty` is true, ask the creator whether to save first, and build nothing until they answer. On yes, run `bpy.ops.wm.save_mainfile()` with the server's `execute_blender_code`; Blender keeps the previous save as `<file>.blend1`. A file with no `filepath` has never been saved, so ask the creator to save it from Blender's File menu.
3. Build in a scene of your own. After each `make_model` that succeeds, run the script with the server's `execute_blender_code`, giving the script's absolute path:

    ```python
    import bpy

    name = "<name> (model-builder)"
    scene = bpy.data.scenes.get(name) or bpy.data.scenes.new(name)
    for obj in list(scene.objects):
        bpy.data.objects.remove(obj)
    window = bpy.context.window_manager.windows[0]
    window.scene = scene
    with bpy.context.temp_override(window=window, scene=scene, view_layer=scene.view_layers[0]):
        exec(open("<absolute path of models/<name>.py>").read(), {})
    result = {"objects": sorted(obj.name for obj in scene.objects)}
    ```

    This clears only the scene it made, and shows that scene in the creator's window. The override gives the script that window, without which operators such as `bpy.ops.object.mode_set` fail with `Context missing active object`. Clear nothing else in their Blender.

The game's file still comes from `make_model`, and the loop still checks its still and the game. When the model is done, tell the creator the scene's name, and that the scene menu at the top of Blender's window switches back to their own.
