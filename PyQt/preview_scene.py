from PyQt5 import QtWidgets, QtGui, QtCore
from video_processing import getVideoFrame


class PreviewScene(QtWidgets.QGraphicsScene):

    def __init__(self):
        super().__init__()
        self.videoPath = None
        self.previewPath = None
        self.outputDirectory = None

        self.mouseLeftButtonPressed = False
        self.mouseStartPosition = None
        self.selectionArea = None

    def addVideo(self, video_path):
        self.videoPath = video_path
        self.previewPath = getVideoFrame(video_path)
        self.addPixmap(QtGui.QPixmap(self.previewPath))

    def removeVideo(self):
        self.videoPath = None
        self.previewPath = None

        for item in self.items():
            self.removeItem(item) 

    def mousePressEvent(self, event) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            # clear existing selection area
            if self.selectionArea:
                self.removeItem(self.selectionArea)

            self.mouseLeftButtonPressed = True
            self.mouseStartPosition = event.scenePos()

            self.selectionArea = QtWidgets.QGraphicsRectItem()
            self.selectionArea.setBrush(QtGui.QBrush(QtGui.QColor(158, 182, 255, 96)))
            self.selectionArea.setPen(QtGui.QPen(QtGui.QColor(158, 182, 255, 200), 1))
            self.addItem(self.selectionArea)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if not self.mouseLeftButtonPressed:
            super().mouseMoveEvent(event)
            return

        # form selection area
        scene_pos = event.scenePos()
        
        if scene_pos.x() > self.mouseStartPosition.x():
            if scene_pos.y() > self.mouseStartPosition.y():
                x0 = self.mouseStartPosition.x()
                y0 = self.mouseStartPosition.y()
                width = scene_pos.x() - x0
                height = scene_pos.y() - y0
            else:
                x0 = self.mouseStartPosition.x()
                y0 = scene_pos.y()
                width = scene_pos.x() - x0
                height = self.mouseStartPosition.y() - y0
        else:
            if scene_pos.y() > self.mouseStartPosition.y():
                x0 = scene_pos.x()
                y0 = self.mouseStartPosition.y()
                width = self.mouseStartPosition.x() - x0
                height = scene_pos.y() - y0
            else:
                x0 = scene_pos.x()
                y0 = scene_pos.y()
                width = self.mouseStartPosition.x() - x0
                height = self.mouseStartPosition.y() - y0

        self.selectionArea.setRect(x0, y0, width, height)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.mouseLeftButtonPressed = False

        super().mouseReleaseEvent(event)
