from sprite_ai.core.sprite import Sprite
from sprite_ai.default_states import POSSIBLE_STATES


class NativeUI:
    def __init__(self) -> None:

        self.sprite = Sprite(
            sprite_gui=sprite_gui,
            sprite_behaviour=sprite_behaviour,
        )
