#include <opencv2/opencv.hpp>
#include <opencv2/video.hpp>
#include <QDir>
#include "hpdf.h"
#include "video_processing.hpp"
#include "images_similarity.hpp"


VideoProcessingQThread::VideoProcessingQThread(
        QString videoPath, int x, int y, int w, int h, QString outputDirectory) :
        QThread::QThread(),
        x(x), y(y), w(w), h(h), outputDirectory(outputDirectory){}

VideoProcessingQThread::~VideoProcessingQThread() { this->wait(); }

const QString VideoProcessingQThread::PREVIEW_PATH = "./preview.png";
const QString VideoProcessingQThread::IMAGE_PREFIX = "__vtss_img__";

void VideoProcessingQThread::stop()
{
    active = false;
    quit();
    wait();
    emit progressUpdated(0);
}

void VideoProcessingQThread::run()
{
    cv::VideoCapture capture(videoPath.toStdString());
    int framesCount = capture.get(cv::CAP_PROP_FRAME_COUNT);

    int framesRead = 0;
    int saveEveryN = 20;
    int imageCount = 0;

    cv::Mat previousImageGrayscale;
    cv::Mat imageGrayscale;

    int sameImagesCount = 0;
    cv::Mat frame;

    while (active)
    {
        capture.read(frame);
        framesRead += 1;

        if (frame.empty())
            break;

        if (framesRead < saveEveryN)
        {
            framesRead++;
            continue;
        }

        framesRead = 0;
        emit progressUpdated(int(capture.get(cv::CAP_PROP_POS_FRAMES) / framesCount * 100));

        frame = frame(cv::Rect(x, y, w, h));
        cv::cvtColor(frame, imageGrayscale, cv::COLOR_BGR2GRAY);

        if (previousImageGrayscale.empty())
        {
            previousImageGrayscale = imageGrayscale;
            continue;
        }

        if (structural_similarity(imageGrayscale, previousImageGrayscale) > 0.85)
            sameImagesCount++;
        else
            sameImagesCount = 0;

        previousImageGrayscale = imageGrayscale;

        if (sameImagesCount == 2)
        {
            imageCount++;

            QString filename = QString("%1%2.png").arg(IMAGE_PREFIX, QString::number(imageCount));
            QString imagePath = QDir(outputDirectory).filePath(filename);
            cv::imwrite(imagePath.toStdString(), frame);
        }
    }

    capture.release();

    if (active)
        createPdfFromImages(outputDirectory, videoPath);

    removeImages(outputDirectory);

    if (active)
        emit processingFinished(1);
}

void VideoProcessingQThread::createPdfFromImages(QString outputDirectory, QString videoPath)
{

}

void VideoProcessingQThread::removeImages(QString outputDirectory)
{

}

QString VideoProcessingQThread::getVideoFrame(const QString& filename)
{
    cv::VideoCapture capture(filename.toStdString());
    int framesRead = 0;

    cv::Mat frame;
    while (framesRead < 100)
    {
        capture.read(frame);
        framesRead += 1;

        if (frame.empty())
            throw std::runtime_error("Failed to read video frame");
    }

    cv::imwrite(PREVIEW_PATH.toStdString(), frame);
    capture.release();

    return PREVIEW_PATH;
}

std::vector<QString> VideoProcessingQThread::getImagesForPdf(QString outputDirectory)
{
    return { "" };
}
