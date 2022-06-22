#ifndef VIDEOPROCESSING_HPP
#define VIDEOPROCESSING_HPP

#include <QThread>


class VideoProcessingQThread: public QThread
{
    Q_OBJECT

public:
    VideoProcessingQThread(QString videoPath, int x, int y, int w, int h, QString outputDirectory = ".");
    ~VideoProcessingQThread();

    void stop();
    void run();
    std::vector<QString> getVideoImages() { return videoImages; };

    static QString getVideoFrame(const QString& filename);

signals:
    void progressUpdated(int progress);
    void processingFinished(int status);

private:
    QString videoPath;
    int x;
    int y;
    int w;
    int h;
    QString outputDirectory;

    bool active = true;
    std::vector<QString> videoImages;

    static const QString PREVIEW_PATH;
    static const QString IMAGE_PREFIX;
};

#endif // VIDEOPROCESSING_HPP
