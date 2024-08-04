from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtGui import QBrush, QColor, QPainterPath, QCursor

class ResizableGraphicsItem(QGraphicsItem):
    handle_size = 3.0

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges)
        self.resizing_handle = None
        self.handles = []

    def boundingRect(self):
        return QRectF(0, 0, 100, 100)  # Example bounding rect

    def paint(self, painter, option, widget):
        brush = QBrush(QColor(255, 0, 0, 128))
        painter.setBrush(brush)
        painter.drawRect(self.boundingRect())

    def hoverMoveEvent(self, event):
        print("Hover Move Event")
        if self.isSelected():
            handles = self.get_handles()
            for handle in handles:
                if handle.contains(event.pos()):
                    self.setCursor(Qt.SizeFDiagCursor)
                    return
        super().hoverMoveEvent(event)
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        print("Mouse Press Event")
        if self.isSelected():
            handles = self.get_handles()
            for i, handle in enumerate(handles):
                if handle.contains(event.pos()):
                    self.start_resize(i)
                    return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        print("Mouse Move Event")
        if self.resizing_handle is not None:
            self.resize(event.pos())
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        print("Mouse Release Event")
        self.stop_resize()
        super().mouseReleaseEvent(event)

    def get_handles(self):
        print("Get Handles")
        rect = self.boundingRect()
        return [QRectF(rect.right() - self.handle_size / 2, rect.bottom() - self.handle_size / 2, self.handle_size, self.handle_size)]

    def start_resize(self, handle_index):
        print("Start Resize")
        self.resizing_handle = handle_index
        self.start_pos = self.mapToScene(self.get_handles()[handle_index].center())
        self.original_size = self.boundingRect().size()

    def resize(self, pos):
        print("Resize")
        current_pos = self.mapToScene(pos)
        delta = current_pos - self.start_pos
        new_size = self.original_size + QPointF(delta.x(), delta.y())
        self.prepareGeometryChange()
        self.setRect(QRectF(self.rect().topLeft(), new_size))

    def stop_resize(self):
        print("Stop Resize")
        self.resizing_handle = None
