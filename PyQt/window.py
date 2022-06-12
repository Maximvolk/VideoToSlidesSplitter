import sys
from PyQt5 import QtCore, QtWidgets, uic
from video_processing import VideoProcessingQThread
from preview_scene import PreviewScene


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("window.ui", self)
        self.setHandlers()

        self.videoPath = None
        self.outputDirectory = "."

        self.removeVideoButton.setEnabled(False)
        self.startButton.setEnabled(False)

        self.previewScene = PreviewScene()
        self.preview.setScene(self.previewScene)

    def updateProgress(self, progress):
        self.progressBar.setValue(progress)

    def finishProcessing(self):
        self.progressBar.reset()
        self.removeVideo()

        message = QtWidgets.QMessageBox()
        message.setWindowTitle("")
        message.setText("Processing finished!")
        message.exec_()

    def setHandlers(self):
        self.addVideoButton.clicked.connect(self.openAddVideoDialog)
        self.removeVideoButton.clicked.connect(self.removeVideo)
        self.chooseOutputDirectoryButton.clicked.connect(self.openChooseOutputDirectoryDialog)
        self.startButton.clicked.connect(self.startProcessing)

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
        self.chooseOutputDirectoryButton.setEnabled(True)

        self.videoPath = None
        self.previewScene.clear()
        self.previewScene.resetSelection()
        self.processingTask.stop()

    def openChooseOutputDirectoryDialog(self):
        outputDirectory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")

        if not outputDirectory:
            return

        self.outputDirectory = outputDirectory

    def startProcessing(self):
        self.processingTask = VideoProcessingQThread(self.videoPath, self.previewScene.x0,
            self.previewScene.y0, self.previewScene.w, self.previewScene.h, self.outputDirectory)

        self.processingTask.start()
        self.processingTask.progressUpdated.connect(self.updateProgress)
        self.processingTask.processingFinished.connect(self.finishProcessing)

        self.startButton.setEnabled(False)
        self.addVideoButton.setEnabled(False)
        self.chooseOutputDirectoryButton.setEnabled(False)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
