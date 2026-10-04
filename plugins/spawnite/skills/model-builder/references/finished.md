# A model that looks finished

A model looks finished when its outline reads from the game's camera, its parts are shaped rather than boxed, and its colours belong together. Check each of the following before you show the creator.

## Shapes past boxes

- Start from the outline the player sees, and make what the thing is known by larger than life: a knight's crest, pauldrons and shield, a tower's roof and battlements.
- Build each part from the primitive nearest its shape, placed by a matrix, as [the imp](imp.py) builds every part with `bmesh.ops.create_uvsphere` and `bmesh.ops.create_cone`. A sphere scaled on each axis makes a torso, a head or a boot. A cone makes a horn, a spike or, with four segments, a blade. A cone with two equal radii is a cylinder.
- Give a hard-edged part, such as armour, a crate or a wall, a Bevel modifier, so its edges catch the light: `width` about 1 cm and 2 `segments`.
- Make a symmetric part once and mirror it, with a Mirror modifier or a loop over `side in (1, -1)`, as the imp does.
- Shade round parts smooth with `polygon.use_smooth = True`, and leave flat faces flat.
- Let parts overlap rather than joining them into one surface: the player never sees inside.
- Add the detail that shows from the game's camera: a trim in a second colour, eyes, a belt, rivets. Skip detail smaller than a few pixels there.

## The triangle budget

`make_model` counts the triangles the file draws, and the imp draws 4,578.

The segments decide the count. A UV sphere of `u` segments and `v` rings draws `2 × u × (v − 1)` triangles, so each of the imp's 16 by 12 body parts draws 352. Give round parts the fewest segments that still look round from the game's camera. Each level of a Subdivision Surface modifier draws four times the triangles, so keep it off a whole model.

## Applied transforms

Keep every object at location zero, rotation zero and scale one, and put sizes and turns in the mesh. The imp does this by passing a matrix to each `bmesh` operation. For a part made another way, apply its transform with `bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)` while it is selected and active.

A modifier works in its object's own space, so on a scaled object a bevel stretches with the scale. A rig's bones stand where you made them, so a scale left on its mesh moves each part away from the bone that bends it. Apply transforms before you add modifiers and before you bind a mesh to a rig.

## Materials the engine draws

- Set each colour on the material's Principled BSDF node, which you find by its type: `next(node for node in material.node_tree.nodes if node.type == "BSDF_PRINCIPLED")`. Set its `Base Color`, `Roughness` and `Metallic` inputs. The export writes these as the glTF material the engine draws.
- For a part that glows, such as eyes, a gem or a flame, set `Emission Color` and `Emission Strength` on the same node.
- Keep texture nodes such as Noise or Voronoi out of a material. The export writes only image textures and drops the rest, so the game never shows them. A second colour is a second material, set on faces with `material_index`, as the imp does.
- Pick a palette of four to six colours: a main colour, a darker one for trims and undersides, a light one, and one accent. `Base Color` takes linear values, so convert an sRGB colour first: each channel is about `(value / 255) ** 2.2`.

Check roughness, metal and glow in the game screenshot. A metallic surface reflects the scene's sky. A map shot has none, and neither has a `World` with no `look`, so metal there draws almost black. When the scene the model stands in sets a `look`, keep the metal and judge it in that scene. When the scene sets none, the player sees the black too, so give steel `Metallic` 0, a light grey and a low roughness.
