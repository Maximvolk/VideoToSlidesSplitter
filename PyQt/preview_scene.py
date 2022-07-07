from PyQt5 import QtWidgets, QtGui, QtCore
from video_processing import getNthVideoFrame


class PreviewScene(QtWidgets.QGraphicsScene):

    def __init__(self):
        super().__init__()

        self.currentImage = None
        self.videoFramesCount = 0
        self.mouseLeftButtonPressed = False
        self.mouseStartPosition = None

        self.maxWidth = int(self.width())
        self.maxHeight = int(self.height())
        self.resetSelection()

    def createPreviewFromVideo(self, videoPath):
        currentFrame = getNthVideoFrame(videoPath, 100)
        self.setPreview(currentFrame)

    def setPreview(self, frame):
        if self.currentImage:
            self.removeItem(self.currentImage)

        height, width, _ = frame.shape
        image = QtGui.QImage(frame.data, width, height, width*3, QtGui.QImage.Format.Format_RGB888).rgbSwapped()
        self.currentImage = self.addPixmap(QtGui.QPixmap(image))

        self.maxWidth = int(self.width())
        self.maxHeight = int(self.height())
        self.resetSelection()

    def clear(self):
        if self.currentImage:
            self.removeItem(self.currentImage)
            self.currentImage = None
            
        super().clear()

    @property
    def x0(self):
        return self._x0

    @x0.setter
    def x0(self, value):
        if value < 0:
            self._x0 = 0
        else:
            self._x0 = value

    @property
    def y0(self):
        return self._y0

    @y0.setter
    def y0(self, value):
        if value < 0:
            self._y0 = 0
        else:
            self._y0 = value

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        if self.x0 + value > self.maxWidth:
            self._w = self.maxWidth - self.x0
        else:
            self._w = value

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        if self.y0 + value > self.maxHeight:
            self._h = self.maxHeight - self.y0
        else:
            self._h = value

    def resetSelection(self):
        self.selectionRect = None
        self.x0 = 0
        self.y0 = 0
        self.w = self.maxWidth
        self.h = self.maxHeight

    def mousePressEvent(self, event) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            # clear existing selection area
            if self.selectionRect:
                self.removeItem(self.selectionRect)
                self.resetSelection()

            self.mouseLeftButtonPressed = True
            self.mouseStartPosition = event.scenePos()

            self.selectionRect = QtWidgets.QGraphicsRectItem()
            self.selectionRect.setBrush(QtGui.QBrush(QtGui.QColor(158, 182, 255, 96)))
            self.selectionRect.setPen(QtGui.QPen(QtGui.QColor(158, 182, 255, 200), 1))
            self.addItem(self.selectionRect)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if not self.mouseLeftButtonPressed:
            super().mouseMoveEvent(event)
            return

        # form selection area
        scene_pos = event.scenePos()
        
        if scene_pos.x() > self.mouseStartPosition.x():
            if scene_pos.y() > self.mouseStartPosition.y():
                self.x0 = self.mouseStartPosition.x()
                self.y0 = self.mouseStartPosition.y()
                self.w = scene_pos.x() - self.x0
                self.h = scene_pos.y() - self.y0
            else:
                self.x0 = self.mouseStartPosition.x()
                self.y0 = scene_pos.y()
                self.w = scene_pos.x() - self.x0
                self.h = self.mouseStartPosition.y() - self.y0
        else:
            if scene_pos.y() > self.mouseStartPosition.y():
                self.x0 = scene_pos.x()
                self.y0 = self.mouseStartPosition.y()
                self.w = self.mouseStartPosition.x() - self.x0
                self.h = scene_pos.y() - self.y0
            else:
                self.x0 = scene_pos.x()
                self.y0 = scene_pos.y()
                self.w = self.mouseStartPosition.x() - self.x0
                self.h = self.mouseStartPosition.y() - self.y0

        self.selectionRect.setRect(self.x0, self.y0, self.w, self.h)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.mouseLeftButtonPressed = False

        super().mouseReleaseEvent(event)
