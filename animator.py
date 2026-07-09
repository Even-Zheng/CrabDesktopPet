from enum import Enum, auto
from config import GIF_PATHS


class State(Enum):
    NONE = auto()
    AWAIT = auto()
    WALK = auto()
    RUN = auto()
    CLICK = auto()
    CATCH = auto()
    DROP = auto()
    BYE = auto()


class Animator:
    def __init__(self, window):
        self.window = window
        self.current = State.NONE
        self.current_gif = None
    
    def play_await(self, variant: int):
        self.current = State.AWAIT
        self.current_gif = f"await_{variant}"
        self.window.set_gif(GIF_PATHS["await"][self.current_gif])
    
    def play_walk(self, direction: str = ""):
        self.current = State.WALK
        self.current_gif = "walk"
        self.window.set_gif(GIF_PATHS["walk"])
    
    def play_run(self, direction: str = ""):
        self.current = State.RUN
        self.current_gif = "run"
        self.window.set_gif(GIF_PATHS["run"])
    
    def play_click(self, variant: str):
        self.current = State.CLICK
        self.current_gif = variant
        self.window.set_gif(GIF_PATHS["click"][variant])
    
    def play_catch(self):
        self.current = State.CATCH
        self.window.set_gif(GIF_PATHS["catch"])
    
    def play_drop(self):
        self.current = State.DROP
        self.window.set_gif(GIF_PATHS["drop"])
    
    def play_bye(self):
        self.current = State.BYE
        self.window.set_gif(GIF_PATHS["bye"])
    
    def get_state(self) -> State:
        return self.current