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

    static void createPdfFromImages(QString outputDirectory, QString videoPath);
    static void removeImages(QString outputDirectory);
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

    static const QString PREVIEW_PATH;
    static const QString IMAGE_PREFIX;

    static std::vector<QString> getImagesForPdf(QString outputDirectory);
};

#endif // VIDEOPROCESSING_HPP
