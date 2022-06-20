#include <QtWidgets/QMessageBox>
#include <QtWidgets/QFileDialog>
#include <QtCore/Qt>
#include "main_window.hpp"
#include "./ui_main_window.h"
#include "video_processing.hpp"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent), ui(new Ui::MainWindow),
    outputDirectory(".")
{
    ui->setupUi(this);
    previewScene = new PreviewScene(ui->preview);

    ui->removeVideoButton->setEnabled(false);
    ui->startButton->setEnabled(false);
    ui->preview->setScene(previewScene);

    connect(ui->addVideoButton, &QPushButton::clicked, this, &MainWindow::openAddVideoDialog);
    connect(ui->removeVideoButton, &QPushButton::clicked, this, &MainWindow::removeVideo);
    connect(ui->chooseOutputDirectoryButton, &QPushButton::clicked, this, &MainWindow::openChooseOutputDirectoryDialog);
    connect(ui->startButton, &QPushButton::clicked, this, &MainWindow::startProcessing);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::updateProgress(int progress)
{
    ui->progressBar->setValue(progress);
}

void MainWindow::finishProcessing()
{
    ui->progressBar->reset();
    removeVideo();

    QMessageBox message;
    message.setWindowTitle("");
    message.setText("Processing finished!");
    message.exec();
}

void MainWindow::openAddVideoDialog()
{
    videoPath = QFileDialog::getOpenFileName(this, "Open file",
        "/Users/maximvolk/Source/VideoToSlidesSplitter", "Video files (*.mp4)");

    if (videoPath.isNull() || videoPath.isEmpty())
        return;

    ui->addVideoButton->setEnabled(false);
    ui->removeVideoButton->setEnabled(true);
    ui->startButton->setEnabled(true);

    previewScene->createPreviewFromVideo(videoPath);
    ui->preview->fitInView(previewScene->itemsBoundingRect(), Qt::KeepAspectRatio);
}

void MainWindow::removeVideo()
{
    ui->removeVideoButton->setEnabled(false);
    ui->startButton->setEnabled(false);
    ui->addVideoButton->setEnabled(true);
    ui->chooseOutputDirectoryButton->setEnabled(true);

    videoPath = NULL;
    previewScene->clear();
    previewScene->resetSelection();

    if (processingTask)
        processingTask->stop();
}

void MainWindow::openChooseOutputDirectoryDialog()
{
    QString directory = QFileDialog::getExistingDirectory(this, "Select Folder");

    if (outputDirectory.isNull() || outputDirectory.isEmpty())
        return;

    outputDirectory = directory;
}

void MainWindow::startProcessing()
{
    processingTask = new VideoProcessingQThread(videoPath, previewScene->getX0(), previewScene->getY0(),
        previewScene->getW(), previewScene->getH(), outputDirectory);

    processingTask->start();
    connect(processingTask, &VideoProcessingQThread::progressUpdated, this, &MainWindow::updateProgress);
    connect(processingTask, &VideoProcessingQThread::processingFinished, this, &MainWindow::finishProcessing);

    ui->startButton->setEnabled(false);
    ui->addVideoButton->setEnabled(false);
    ui->chooseOutputDirectoryButton->setEnabled(false);
}
