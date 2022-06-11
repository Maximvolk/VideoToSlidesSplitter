import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from video_processing import getVideoFrame
from preview_scene import PreviewScene


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("window.ui", self)
        self.setHandlers()

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
        
        self.addVideoButton.setEnabled(False)
        self.previewScene.addVideo(videoPath[0])
        self.preview.fitInView(self.previewScene.itemsBoundingRect(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio)
    
    def removeVideo(self):
        self.previewScene.removeVideo()
        self.addVideoButton.setEnabled(True)

    def openChooseOutputDirectoryDialog(self):
        outputDirectory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")

        if not outputDirectory:
            return

        self.previewScene.outputDirectory = outputDirectory


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
