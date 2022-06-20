#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QtWidgets/QGraphicsView>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QProgressBar>
#include "preview_scene.hpp"
#include "video_processing.hpp"


QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE


class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget* parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow* ui;
    QString videoPath;
    QString outputDirectory;
    VideoProcessingQThread* processingTask {nullptr};
    PreviewScene* previewScene;

    void updateProgress(int progress);
    void finishProcessing();

    void openAddVideoDialog();
    void removeVideo();
    void openChooseOutputDirectoryDialog();
    void startProcessing();
};
#endif // MAINWINDOW_H
