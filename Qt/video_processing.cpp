#include "video_processing.hpp"
#include <opencv2/opencv.hpp>
#include <opencv2/video.hpp>


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
