import sys
import traceback
from PyQt6.QtWidgets import QApplication

from config import TIMING
from window import CrabWindow
from animator import Animator, State
from mover import Mover
from interaction import InteractionManager
from idle_system import IdleSystem


class CrabPet:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = CrabWindow()
        
        self.animator = Animator(self.window)
        self.mover = Mover(self.window)
        self.interaction = InteractionManager(self.window, self.animator, self.mover, self)
        self.idle = IdleSystem(self.window, self.animator, self.mover)
        
        self.bye_timer = 0
        
        self.window.on_tick = self.main_loop
        
        self.window.snap_to_taskbar()
        self.idle._start_await()
    
    def main_loop(self):
        try:
            dt = TIMING["check_interval"]
            
            if self.animator.get_state() == State.BYE:
                self.bye_timer -= dt
                if self.bye_timer <= 0:
                    self.app.quit()
                return
            
            if self.mover.is_moving():
                move_done = self.mover.update()
                if move_done:
                    self.window.snap_to_taskbar()
                    self.idle.do_decision()
                return
            
            interaction_result = self.interaction.update(dt)
            
            if interaction_result == "click_finished":
                self.window.snap_to_taskbar()
                self.idle.do_decision()
                return
            
            idle_result = self.idle.update(dt, self.interaction.is_busy())
            
            if idle_result == "need_decision":
                self.idle.do_decision()
            elif idle_result == "await_finished":
                self.idle.do_decision()
            
            self.idle.snap_to_taskbar_if_needed()
        except Exception:
            pass
    
    def start_bye_timer(self):
        self.bye_timer = TIMING["bye_duration"]
    
    def run(self):
        return self.app.exec()


if __name__ == "__main__":
    try:
        pet = CrabPet()
        sys.exit(pet.run())
    except Exception:
        with open("crash.log", "w") as f:
            traceback.print_exc(file=f)
        raise