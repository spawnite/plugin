# Camera

Ask: should the camera follow the player, or show the whole play area? Recommend what the prompt asks for. When it says nothing, recommend following the player, unless the games under **Inspiration** show the whole area. `engine/entities/camera` says what each does.

The keys walk the character in the camera's frame, and the player can drag the camera round. A round must not depend on the camera's angle: start the character facing what matters, and check what is in frame at the start of more than one round.

Prove it: screenshots of the start of the first round and of a second round, with what the player needs in frame in both.
