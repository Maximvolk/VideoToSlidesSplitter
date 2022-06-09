import cv2
from pathlib import Path
from skimage.metrics import structural_similarity


PREVIEW_PATH = "./preview.png"

def get_video_frame(filename):
    capture = cv2.VideoCapture(filename)
    frames_read = 0

    while frames_read < 100:
        success, frame = capture.read()
        frames_read += 1

        if not success:
            raise Exception("Failed to read video frame") 

    cv2.imwrite(PREVIEW_PATH, frame)
    capture.release()
    
    return PREVIEW_PATH


def are_images_the_same(first_img, second_img):
    if first_img is None or second_img is None:
        return False

    return structural_similarity(first_img, second_img) > 0.98


def get_image_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def process_video():
    slides_directory = "/Users/maximvolk/Lecture1"
    capture = cv2.VideoCapture("../video.mp4")

    frames_read = 0
    save_every_n = 20
    image_count = 0

    previous_image_grayscale = None
    same_images_count = 0

    while True:
        success, frame = capture.read()

        if not success:
            break

        if frames_read < save_every_n:
            frames_read += 1
            continue

        frames_read = 0
        image_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if previous_image_grayscale is None:
            previous_image_grayscale = image_grayscale
            continue

        if structural_similarity(image_grayscale, previous_image_grayscale) > 0.98:
            same_images_count += 1
        else:
            same_images_count = 0

        previous_image_grayscale = image_grayscale

        if same_images_count == 2:
            image_count += 1
            image_path = str(Path(slides_directory) / f"img_{image_count}.png")
            cv2.imwrite(image_path, frame)

    capture.release()
