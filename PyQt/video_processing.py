import cv2
from pathlib import Path
from skimage.metrics import structural_similarity


PREVIEW_PATH = "./preview.png"


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


def processVideo(videoPath, outputDirectory="/Users/maximvolk/Lecture1"):
    capture = cv2.VideoCapture(videoPath)

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
            imagePath = str(Path(outputDirectory) / f"img_{imageCount}.png")
            cv2.imwrite(imagePath, frame)

    capture.release()
