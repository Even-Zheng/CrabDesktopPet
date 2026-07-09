import sys
import math
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMenu
from PyQt6.QtCore import Qt, QTimer, QPoint, QSize
from PyQt6.QtGui import QMovie

from config import WINDOW, TIMING, DRAG_THRESHOLD


class CrabWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        flags = Qt.WindowType.FramelessWindowHint
        flags |= Qt.WindowType.WindowStaysOnTopHint
        flags |= Qt.WindowType.Tool
        
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        
        self.on_tick = lambda: None
        self.on_click = lambda: None
        self.on_drag_start = lambda: None
        self.on_drag_end = lambda: None
        self.on_right_click = lambda pos: None
        self.on_exit_requested = lambda: None
        
        self.context_menu = QMenu(self)
        self.context_menu.addAction("Exit", self._handle_exit)
        
        self.label = QLabel(self)
        self.movie = None
        self._pending_path = None
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(TIMING["check_interval"])
        
        self._mouse_down = False
        self._is_dragging = False
        self._press_start_pos = QPoint()
        self._drag_offset = QPoint()
        
        self.show()
    
    def _tick(self):
        if self._is_dragging:
            return
        try:
            self.on_tick()
        except Exception:
            pass
    
    def _handle_exit(self):
        try:
            self.on_exit_requested()
        except Exception:
            pass
    
    def _on_frame_changed(self, frame_number):
        if frame_number != 0:
            return
        
        self.movie.frameChanged.disconnect(self._on_frame_changed)
        
        pixmap = self.movie.currentPixmap()
        orig_w = pixmap.width()
        orig_h = pixmap.height()
        
        if orig_w <= 0 or orig_h <= 0:
            orig_w = 100
            orig_h = 100
        
        scale = 1 / 10
        new_width = int(orig_w * scale)
        new_height = int(orig_h * scale)
        new_width = max(10, new_width)
        new_height = max(10, new_height)
        
        self.movie.setScaledSize(QSize(new_width, new_height))
        
        self.label.setFixedSize(new_width, new_height)
        self.setFixedSize(new_width, new_height)
    
    def set_gif(self, path: str):
        if self.movie:
            self.movie.stop()
            self.label.setMovie(None)
            self.movie.deleteLater()
            self.movie = None
        
        self.movie = QMovie(path)
        self._pending_path = path
        
        self.movie.frameChanged.connect(self._on_frame_changed)
        
        self.label.setMovie(self.movie)
        self.movie.start()
    
    def get_screen_rect(self):
        return QApplication.primaryScreen().geometry()
    
    def get_taskbar_y(self):
        screen = self.get_screen_rect()
        ground_offset = 38
        return screen.height() - self.height() - ground_offset
    
    def snap_to_taskbar(self):
        screen = self.get_screen_rect()
        x = max(0, min(self.x(), screen.width() - self.width()))
        y = self.get_taskbar_y()
        self.move(x, y)
    
    def is_on_taskbar(self) -> bool:
        return abs(self.y() - self.get_taskbar_y()) < 10
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._mouse_down = True
            self._is_dragging = False
            self._press_start_pos = event.globalPosition().toPoint()
            self._drag_offset = event.pos()
        
        elif event.button() == Qt.MouseButton.RightButton:
            self.on_right_click(event.globalPosition().toPoint())
    
    def mouseMoveEvent(self, event):
        if not self._mouse_down:
            return
        
        current_pos = event.globalPosition().toPoint()
        dx = current_pos.x() - self._press_start_pos.x()
        dy = current_pos.y() - self._press_start_pos.y()
        moved_distance = math.hypot(dx, dy)
        
        if not self._is_dragging and moved_distance >= DRAG_THRESHOLD:
            self._is_dragging = True
            self.on_drag_start()
        
        if self._is_dragging:
            global_pos = event.globalPosition().toPoint()
            new_pos = global_pos - self._drag_offset
            
            screen = self.get_screen_rect()
            new_pos.setX(max(0, min(new_pos.x(), screen.width() - self.width())))
            new_pos.setY(max(0, min(new_pos.y(), screen.height() - self.height())))
            
            self.move(new_pos)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self._mouse_down:
                return
            
            self._mouse_down = False
            
            if self._is_dragging:
                self._is_dragging = False
                self.on_drag_end()
            else:
                self.on_click()
    
    def is_dragging(self) -> bool:
        return self._is_dragging