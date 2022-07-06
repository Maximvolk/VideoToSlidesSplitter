from PyQt5 import QtWidgets, QtGui
from video_processing import getVideoFramesCount, preparePreviewFrames


class PreviewTape(QtWidgets.QLabel):

    def __init__(self, parent, x, y, width):
        super().__init__()
        self.previewFrameSizeCoef = 0.15
        self.amountOfTapePxForSingleFrame = 15

        self.parent = parent
        self.x = x
        self.y = y
        self.width = width

        self.currentFrameIndex = 0
        self.previewFrames = []

        self.previewFrame = None
        self.frameWidth = None
        self.frameHeight = None

        self.setMouseTracking(True)
        self.setStyleSheet('background: ""; border-radius: 5px;')

    def setFrameSize(self, videoWidth, videoHeight):
        self.frameWidth = videoWidth * self.previewFrameSizeCoef
        self.frameHeight = videoHeight * self.previewFrameSizeCoef

    def preparePreview(self, videoPath):
        # we take every k-th frame of video and show it on certain tape part (amountOfTapePxForSignelFrame)
        everyNth = int(getVideoFramesCount(videoPath) / (self.width / self.amountOfTapePxForSingleFrame))
        self.previewFrames = preparePreviewFrames(videoPath, everyNth)

    def enterEvent(self, event):
        if not self.frameWidth:
            return
        
        self.previewFrame = QtWidgets.QLabel()
        self.previewFrame.setStyleSheet('background: "";')

        previewFrameX, previewFrameY = self._getPreviewFrameCoordinates(event.x())
        self.previewFrame.setGeometry(previewFrameX, previewFrameY, self.frameWidth, self.frameHeight)

        self.currentFrameIndex = self._getFrameIndexByX(event.x())
        self._setNthPreviewFrame(self.currentFrameIndex)

        self.previewFrame.setParent(self.parent)
        self.previewFrame.show()

    def leaveEvent(self, event):
        if not self.previewFrame:
            return

        self.previewFrame.hide()
        del self.previewFrame
        self.previewFrame = None

    def mouseMoveEvent(self, event):
        if not self.previewFrame:
            return

        previewFrameX, previewFrameY = self._getPreviewFrameCoordinates(event.x())
        self.previewFrame.move(previewFrameX, previewFrameY)

        n = self._getFrameIndexByX(event.x())
        if n == self.currentFrameIndex:
            return

        self.currentFrameIndex = n
        self._setNthPreviewFrame(n)

    def mousePressEvent(self, event):
        frame = self.previewFrames[self.currentFrameIndex]

    def _getPreviewFrameCoordinates(self, eventX):
        previewFrameX = self.x + eventX - self.frameWidth / 2
        previewFrameY = self.y - self.frameHeight - 10

        return previewFrameX, previewFrameY

    def _getFrameIndexByX(self, x):
        return int(x / self.amountOfTapePxForSingleFrame)

    def _setNthPreviewFrame(self, n):
        frame = self.previewFrames[n]
        height, width, _ = frame.shape

        image = QtGui.QImage(frame.data, width, height, width*3, QtGui.QImage.Format.Format_RGB888).rgbSwapped()
        self.previewFrame.setPixmap(QtGui.QPixmap(image))
        self.previewFrame.setScaledContents(True)
