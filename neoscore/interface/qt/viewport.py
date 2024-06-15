from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QPointF, Qt, QEvent
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QGestureEvent, QPinchGesture

from neoscore.core.key_event import KeyEventType
from neoscore.core.mouse_event import MouseEventType
from neoscore.interface.qt.converters import (
    q_key_event_to_key_event,
    q_mouse_event_to_mouse_event,
)

_NO_DRAG = 0
_SCROLL_HAND_DRAG = 1
_NO_VIEWPORT_UPDATE = 3
_SCROLL_BAR_AS_NEEDED = 0
_SCROLL_BAR_ALWAYS_OFF = 1
_FOCUS_POLICY_STRONG_FOCUS = 0x1 | 0x2 | 0x8
_FOCUS_POLICY_NO_FOCUS = 0

MIN_ZOOM_VALUE = 0.5
MAX_ZOOM_VALUE = 50


class Viewport(QtWidgets.QGraphicsView):
    """A QGraphicsView configured for use in interactive neoscore scenes.

    Includes some basic hacky features.
    """

    def __init__(self, scene: QtWidgets.QGraphicsScene):
        super().__init__(scene)
        # Default configs
        self.setViewport(QtWidgets.QOpenGLWidget())
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        # Automatic viewport updates are disabled. Updates are performed
        # manually in the main window refresh function.
        self.set_auto_interaction(True)
        self.setViewportUpdateMode(_NO_VIEWPORT_UPDATE)  # noqa
        self.mouse_event_handler = None
        self.key_event_handler = None
        self.setInteractive(True)
        self.grabGesture(Qt.PinchGesture)
        self.zoom_level = 1.0

    def set_auto_interaction(self, enabled: bool):
        """Set whether mouse and scrollbar interaction is enabled."""
        self.auto_interaction_enabled = enabled
        self.setDragMode(_NO_DRAG)
        if enabled:
            self.setHorizontalScrollBarPolicy(_SCROLL_BAR_AS_NEEDED)  # noqa
            self.setVerticalScrollBarPolicy(_SCROLL_BAR_AS_NEEDED)  # noqa
        else:
            self.setHorizontalScrollBarPolicy(_SCROLL_BAR_ALWAYS_OFF)  # noqa
            self.setVerticalScrollBarPolicy(_SCROLL_BAR_ALWAYS_OFF)  # noqa

    def wheelEvent(self, event):
        """Implementation of Qt event hook for zooming with the mouse wheel."""
        if not self.auto_interaction_enabled:
            return
        
        modifiers = event.modifiers()
        zoom_in_factor = 0.9
        zoom_out_factor = 1 / zoom_in_factor

        if modifiers == Qt.ControlModifier: # Mouse wheel zooms when Ctrl/Cmd is pressed
            # Set zoom factors based on mouse wheel movement
            wheel_delta = event.angleDelta().y()
            if wheel_delta > 0:
                zoom_factor = zoom_in_factor
            else:
                zoom_factor = zoom_out_factor
            new_zoom_level = self.zoom_level * zoom_factor
            if self.is_zoom_within_bounds(new_zoom_level):
                self.zoom_level = new_zoom_level
                # Save the scene pos
                old_pos = self.mapToScene(event.pos())
                # Zoom
                self.scale(zoom_factor, zoom_factor)
                # Get the new pos
                new_pos = self.mapToScene(event.pos())
                # Move scene to old pos
                delta = new_pos - old_pos
                self.translate(delta.x(), delta.y())
        else: # Mousewheel scrolls otherwise
            # Get and set scroll values
            delta = event.angleDelta()
            if modifiers == Qt.ShiftModifier: # Mouse wheel + Shift = horizontal scrolling
                horizontal_steps = delta.y() / 120
                vertical_steps = 0
            else: # Otherwise normal vertical scrolling behavior
                horizontal_steps = delta.x() / 120
                vertical_steps = delta.y() / 120

            # Scroll horizontally if horizontal delta is present
            if horizontal_steps != 0:
                horizontal_value = self.horizontalScrollBar().value() - int(horizontal_steps * self.horizontalScrollBar().singleStep())
                self.horizontalScrollBar().setValue(horizontal_value)

            # Scroll vertically if vertical delta is present
            if vertical_steps != 0:
                vertical_value = self.verticalScrollBar().value() - int(vertical_steps * self.verticalScrollBar().singleStep())
                self.verticalScrollBar().setValue(vertical_value)

        # Accept the event to indicate that it has been handled
        event.accept()

    def gestureEvent(self, event: QGestureEvent):
        """Get input from pinch gestures."""
        if not self.auto_interaction_enabled:
            return False
        
        if pinch := event.gesture(Qt.PinchGesture):
            self.handlePinch(pinch)
            event.accept()
            return True
        
        return super().gestureEvent(event)
    
    def handlePinch(self, gesture: QPinchGesture):
        """Update viewport zoom from pinch gesture values."""
        change_flags = gesture.changeFlags()
        if change_flags & QPinchGesture.ScaleFactorChanged:
            scale_factor = gesture.scaleFactor()
            new_zoom_level = self.zoom_level * scale_factor
            if self.is_zoom_within_bounds(new_zoom_level):
                self.zoom_level = new_zoom_level
                old_pos = self.mapToScene(gesture.centerPoint().toPoint())
                self.scale(scale_factor, scale_factor)
                new_pos = self.mapToScene(gesture.centerPoint().toPoint())
                delta = new_pos - old_pos
                self.translate(delta.x(), delta.y())

    def is_zoom_within_bounds(self, zoom_level: float) -> bool:
        """Check if the zoom level is within the allowed bounds."""
        return MIN_ZOOM_VALUE <= zoom_level <= MAX_ZOOM_VALUE

    def scrollContentsBy(self, *args):
        """Override of superclass scroll action to trigger a viewport update."""
        super().scrollContentsBy(*args)
        self.viewport().update()

    def window_document_pos(self) -> QPointF:
        return self.mapToScene(0, 0)

    # Input event handler overrides

    def mouseMoveEvent(self, e):
        if self.mouse_event_handler:
            self.mouse_event_handler(
                q_mouse_event_to_mouse_event(
                    e, MouseEventType.MOVE, self.window_document_pos()
                )
            )
        if self.auto_interaction_enabled:
            super().mouseMoveEvent(e)
        # Explicitly update the viewport
        self.viewport().update()

    def mousePressEvent(self, e):
        if self.mouse_event_handler:
            self.mouse_event_handler(
                q_mouse_event_to_mouse_event(
                    e, MouseEventType.PRESS, self.window_document_pos()
                )
            )
        if self.auto_interaction_enabled:
            super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        if self.mouse_event_handler:
            self.mouse_event_handler(
                q_mouse_event_to_mouse_event(
                    e, MouseEventType.RELEASE, self.window_document_pos()
                )
            )
        if self.auto_interaction_enabled:
            super().mouseReleaseEvent(e)

    def mouseDoubleClickEvent(self, e):
        if self.mouse_event_handler:
            self.mouse_event_handler(
                q_mouse_event_to_mouse_event(
                    e, MouseEventType.DOUBLE_CLICK, self.window_document_pos()
                )
            )
        if self.auto_interaction_enabled:
            super().mouseDoubleClickEvent(e)

    def keyPressEvent(self, e):
        if self.key_event_handler:
            self.key_event_handler(q_key_event_to_key_event(e, KeyEventType.PRESS))
        if self.auto_interaction_enabled:
            super().keyPressEvent(e)

    def keyReleaseEvent(self, e):
        if self.key_event_handler:
            self.key_event_handler(q_key_event_to_key_event(e, KeyEventType.RELEASE))
        if self.auto_interaction_enabled:
            super().keyPressEvent(e)

    def event(self, e):
        """Override the event method of QGestureEvent to handle pinch zoom functionality."""
        if e.type() == QEvent.Gesture:
            return self.gestureEvent(e)
        return super().event(e)

    # End of input event handler overrides
