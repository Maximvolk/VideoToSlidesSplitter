import sys
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from preview_tape import PreviewTape
from video_processing import VideoProcessingQThread, getVideoFramesCount
from preview_scene import PreviewScene


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("window.ui", self)
        self.setHandlers()

        self.previewTape = PreviewTape(self, 260, 370, 511)
        self.previewTape.setParent(self)
        self.previewTape.setGeometry(260, 370, 511, 21)
        self.previewTape.hide()

        self.loaderPath = "loader.gif"
        self.videoPath = None
        self.outputDirectory = "."
        self.processingTask = None

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
        self.previewTape.setFrameSize(self.previewScene.maxWidth, self.previewScene.maxHeight)

        # self.addLoader()
        self.previewTape.preparePreview(videoPath[0])
        # self.removeLoader()

        self.previewTape.show()
        self.preview.fitInView(self.previewScene.itemsBoundingRect(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio)
    
    def removeVideo(self):
        self.removeVideoButton.setEnabled(False)
        self.startButton.setEnabled(False)
        self.addVideoButton.setEnabled(True)
        self.chooseOutputDirectoryButton.setEnabled(True)

        self.previewTape.hide()
        self.videoPath = None
        self.previewScene.clear()
        self.previewScene.resetSelection()

        if self.processingTask:
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

    def addLoader(self):
        loadingDialog = QtWidgets.QDialog()
        loadingDialog.setWindowTitle("");
        loadingDialog.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        loadingLabel = QtWidgets.QLabel()
        loadingMovie = QtGui.QMovie(self.loaderPath)

        loadingLabel.setMovie(loadingMovie)
        loadingMovie.start()
        loadingDialog.exec_()

    def removeLoader(self):
        self.loaderLabe.hide()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
