from pathlib import Path
import os
from stat import ST_CTIME

import cv2
from skimage.metrics import structural_similarity
from PyQt5 import QtCore
from PIL import Image


PREVIEW_PATH = "./preview.png"
IMAGE_PREFIX = "__vtss_img__"
OUTPUT_PREFIX = "Lecture_"


def getVideoFrame(filename):
    capture = cv2.VideoCapture(filename)
    framesRead = 0

    while framesRead < 100:
        success, frame = capture.read()
        framesRead += 1

        if not success:
            raise Exception("Failed to read video frame") 

    cv2.imwrite(PREVIEW_PATH, frame)
    capture.release()

    return PREVIEW_PATH


class VideoProcessingQThread(QtCore.QThread):

    progressUpdated = QtCore.pyqtSignal(int)
    processingFinished = QtCore.pyqtSignal(int)

    def __init__(self, videoPath, x, y, w, h, outputDirectory="."):
        self.videoPath = videoPath
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.outputDirectory = outputDirectory

        super().__init__()

    def __del__(self):
        self.wait()

    def terminate(self):
        removeImages(self.outputDirectory)
        self.progressUpdated.emit(0)

        if not self.isFinished:
            super().terminate()

    def run(self):
        capture = cv2.VideoCapture(self.videoPath)
        framesCount = capture.get(cv2.CAP_PROP_FRAME_COUNT)

        framesRead = 0
        saveEveryN = 20
        imageCount = 0

        previousImageGrayscale = None
        sameImagesCount = 0

        while True:
            success, frame = capture.read()

            if not success:
                break

            if framesRead < saveEveryN:
                framesRead += 1
                continue

            framesRead = 0
            self.progressUpdated.emit(int(capture.get(cv2.CAP_PROP_POS_FRAMES) / framesCount * 100))

            frame = frame[self.y: self.y + self.h, self.x: self.x + self.w]
            imageGrayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if previousImageGrayscale is None:
                previousImageGrayscale = imageGrayscale
                continue

            if structural_similarity(imageGrayscale, previousImageGrayscale) > 0.98:
                sameImagesCount += 1
            else:
                sameImagesCount = 0

            previousImageGrayscale = imageGrayscale

            if sameImagesCount == 2:
                imageCount += 1
                imagePath = str(Path(self.outputDirectory) / f"{IMAGE_PREFIX}{imageCount}.png")
                cv2.imwrite(imagePath, frame)

        capture.release()
        createPdfFromImages(self.outputDirectory, self.videoPath)
        removeImages(self.outputDirectory)
        self.processingFinished.emit(1)


def createPdfFromImages(outputDirectory, videoPath):
    videoPath = videoPath.replace("\\", "/")
    fileName = os.path.basename(videoPath).split('.')[0]
    images = []

    for item in _getImagesForPdf(outputDirectory):
        image = Image.open(str(Path(outputDirectory) / item)).convert('RGB')
        images.append(image)

    if len(images) == 0:
        return

    firstImage = images[0]
    outputFile = str(Path(outputDirectory) / f"{fileName}.pdf")
    firstImage.save(outputFile, save_all=True, append_images=images[1:])


def _getImagesForPdf(outputDirectory):
    # retrieve suitable files (with prefix) and sort by creation time
    files = [os.path.join(outputDirectory, item) for item in os.listdir(outputDirectory)]
    files = [(os.stat(item)[ST_CTIME], item) for item in files]
    files.sort()
    
    return [item[1] for item in files if IMAGE_PREFIX in item[1]]


def removeImages(outputDirectory):
    for item in os.listdir(outputDirectory):
        if IMAGE_PREFIX in item:
            os.remove(str(Path(outputDirectory) / item))
