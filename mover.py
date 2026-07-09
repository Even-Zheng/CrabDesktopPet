import random
from config import MOVE


class Mover:
    def __init__(self, window):
        self.window = window
        self.mode = None
        self.direction = -1
        self.speed = 0
        self.target_distance = 0
        self.traveled = 0
        self.start_x = 0
    
    def start_walk(self):
        self.mode = "walk"
        self.direction = -1
        self.speed = MOVE["walk_speed"]
        self.target_distance = 200
        self.traveled = 0
        self.start_x = self.window.x()
    
    def start_run(self):
        self.mode = "run"
        self.direction = -1
        self.speed = MOVE["run_speed"]
        self.target_distance = 400
        self.traveled = 0
        self.start_x = self.window.x()
    
    def start_drop(self):
        self.mode = "drop"
        self.speed = MOVE["drop_speed"]
    
    def stop(self):
        self.mode = None
        self.speed = 0
        self.target_distance = 0
        self.traveled = 0
        self.start_x = 0
        self.direction = -1
    
    def update(self) -> bool:
        if not self.mode:
            return False
        
        if self.mode in ("walk", "run"):
            dx = self.direction * self.speed
            new_x = self.window.x() + dx
            self.traveled += abs(dx)
            
            screen = self.window.get_screen_rect()
            w = self.window.width()
            
            if new_x <= 0:
                new_x = 0
                self.direction = 1
            elif new_x >= screen.width() - w:
                new_x = screen.width() - w
                self.direction = -1
            
            self.window.move(new_x, self.window.y())
            
            if self.traveled >= self.target_distance:
                self.stop()
                return True
        
        elif self.mode == "drop":
            new_y = self.window.y() + self.speed
            target_y = self.window.get_taskbar_y()
            
            if new_y >= target_y:
                self.window.move(self.window.x(), target_y)
                self.stop()
                return True
            else:
                self.window.move(self.window.x(), new_y)
        
        return False
    
    def is_moving(self) -> bool:
        return self.mode is not None