import random
from config import TIMING, PROB


class IdleSystem:
    def __init__(self, window, animator, mover):
        self.window = window
        self.animator = animator
        self.mover = mover
        
        self.idle_timer = 0
        self.await_timer = 0
        self.is_awaiting = False
        
        self.await_variant = 1
    
    def reset_idle_timer(self):
        self.idle_timer = 0
    
    def update(self, dt: int, is_busy: bool):
        if is_busy:
            self.idle_timer = 0
            return None
        
        self.idle_timer += dt
        
        if self.is_awaiting:
            self.await_timer -= dt
            if self.await_timer <= 0:
                self.is_awaiting = False
                return "await_finished"
            return None
        
        if self.idle_timer >= TIMING["idle_threshold"]:
            self.idle_timer = 0
            return "need_decision"
        
        return None
    
    def do_decision(self):
        if random.random() < PROB["await_chance"]:
            self._start_await()
            return "await"
        else:
            if random.random() < PROB["walk_chance"]:
                self._start_walk()
                return "walk"
            else:
                self._start_run()
                return "run"
    
    def _start_await(self):
        self.is_awaiting = True
        self.await_variant = random.randint(1, 5)
        self.await_timer = TIMING["await_duration"]
        self.animator.play_await(self.await_variant)
    
    def _start_walk(self):
        self.animator.play_walk()
        self.mover.start_walk()
    
    def _start_run(self):
        self.animator.play_run()
        self.mover.start_run()
    
    def snap_to_taskbar_if_needed(self):
        if not self.window.is_on_taskbar() and not self.mover.is_moving():
            self.window.snap_to_taskbar()