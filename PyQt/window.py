import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from video_processing import getVideoFrame
from preview_scene import PreviewScene


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("window.ui", self)
        self.setHandlers()

        self.videoPath = None
        self.outputDirectory = None

        self.removeVideoButton.setEnabled(False)
        self.startButton.setEnabled(False)

        self.previewScene = PreviewScene()
        self.preview.setScene(self.previewScene)

    def setHandlers(self):
        self.addVideoButton.clicked.connect(self.openAddVideoDialog)
        self.removeVideoButton.clicked.connect(self.removeVideo)
        self.chooseOutputDirectoryButton.clicked.connect(self.openChooseOutputDirectoryDialog)

    def openAddVideoDialog(self):
        videoPath = QtWidgets.QFileDialog.getOpenFileName(self,
            "Open file", "/Users/maximvolk/Source/VideoToSlidesSplitter", "Video files (*.mp4)")
        
        if not videoPath[0]:
            return
        
        self.videoPath = videoPath[0]
        self.addVideoButton.setEnabled(False)
        self.removeVideoButton.setEnabled(True)
        self.startButton.setEnabled(True)

        self.previewScene.createPreviewFromVideo(videoPath[0])
        self.preview.fitInView(self.previewScene.itemsBoundingRect(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio)
    
    def removeVideo(self):
        self.removeVideoButton.setEnabled(False)
        self.startButton.setEnabled(False)
        self.addVideoButton.setEnabled(True)
        
        self.videoPath = None
        self.previewScene.clear()

    def openChooseOutputDirectoryDialog(self):
        outputDirectory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")

        if not outputDirectory:
            return

        print(outputDirectory)
        self.outputDirectory = outputDirectory


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
