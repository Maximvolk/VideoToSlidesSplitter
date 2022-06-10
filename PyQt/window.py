import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from video_processing import get_video_frame


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("window.ui", self)
        self._set_handlers()

    def _set_handlers(self):
        self.addVideoButton.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        video_path = QtWidgets.QFileDialog.getOpenFileName(self,
            'Open file',  '/Users/maximvolk/Source/VideoToSlidesSplitter',"Video files (*.mp4)")

        if not video_path[0]:
            return

        preview_path = get_video_frame(video_path[0])
        self.previewArea.setScaledContents(True)
        self.previewArea.setPixmap(QtGui.QPixmap(preview_path))


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
