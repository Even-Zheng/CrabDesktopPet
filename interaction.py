import random
from PyQt6.QtCore import QPoint

from config import TIMING, DRAG_THRESHOLD


class InteractionManager:
    def __init__(self, window, animator, mover, app_ref):
        self.window = window
        self.animator = animator
        self.mover = mover
        self.app = app_ref
        
        self.click_timer = 0
        self.is_click_playing = False
        
        self.is_dragging = False
        self.catch_start_pos = QPoint()
        
        self.is_exiting = False
        
        self._setup_hooks()
    
    def _setup_hooks(self):
        self.window.on_click = self._on_click
        self.window.on_drag_start = self._on_drag_start
        self.window.on_drag_end = self._on_drag_end
        self.window.on_right_click = self._on_right_click
        self.window.on_exit_requested = self._on_exit
    
    def _on_click(self):
        if self.is_exiting or self.is_dragging or self.is_click_playing:
            return
        
        self._do_click()
    
    def _do_click(self):
        self.is_dragging = False
        variant = random.choice(["click_1", "click_2"])
        self.animator.play_click(variant)
        self.is_click_playing = True
        self.click_timer = TIMING["click_duration"]
    
    def _on_drag_start(self):
        if self.is_exiting:
            return
        self.is_dragging = True
        self.catch_start_pos = self.window.pos()
        self.mover.stop()
        self.animator.play_catch()
    
    def _on_drag_end(self):
        if not self.is_dragging:
            return
        
        self.is_dragging = False
        
        moved_distance = abs(self.window.x() - self.catch_start_pos.x()) + \
                        abs(self.window.y() - self.catch_start_pos.y())
        
        if moved_distance < DRAG_THRESHOLD:
            self._do_click()
        else:
            self._do_drop()
    
    def _do_drop(self):
        self.animator.play_drop()
        self.mover.start_drop()
    
    def _on_right_click(self, pos):
        if self.is_exiting:
            return
        self.window.context_menu.exec(pos)
    
    def _on_exit(self):
        self.is_exiting = True
        self.mover.stop()
        self.animator.play_bye()
        self.app.start_bye_timer()
    
    def update(self, dt: int):
        if self.is_click_playing:
            self.click_timer -= dt
            if self.click_timer <= 0:
                self.is_click_playing = False
                return "click_finished"
        return None
    
    def is_busy(self) -> bool:
        return self.is_dragging or self.is_click_playing or self.is_exiting