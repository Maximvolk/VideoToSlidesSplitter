#include <QtGui/QPixmap>
#include <QtGui/QBrush>
#include <QtGui/QColor>
#include <QtGui/QPen>
#include <QtWidgets/QGraphicsScene>
#include <QtWidgets/QGraphicsRectItem>
#include <QtWidgets/QGraphicsSceneMouseEvent>
#include "preview_scene.hpp"
#include "video_processing.hpp"


PreviewScene::PreviewScene(QObject* parent) : QGraphicsScene(parent)
{
    maxWidth = width();
    maxHeight = height();
    resetSelection();
}

void PreviewScene::createPreviewFromVideo(QString videoPath)
{
    QString previewPath = VideoProcessingQThread::getVideoFrame(videoPath);
    addPixmap(QPixmap(previewPath));

    maxWidth = width();
    maxHeight = height();
    resetSelection();
}

void PreviewScene::resetSelection()
{
    if (selectionRect)
        delete selectionRect;

    setX0(0);
    setY0(0);
    setW(maxWidth);
    setH(maxHeight);
}

void PreviewScene::removePreview()
{
    delete previewPixmapItem;
}

void PreviewScene::mousePressEvent(QGraphicsSceneMouseEvent* event)
{
    if (event->button() == Qt::LeftButton)
    {
        // Clear existing selection area
        if (selectionRect)
        {
            removeItem(selectionRect);
            resetSelection();
        }

        mouseLeftButtonPressed = true;
        mouseStartPosition = event->scenePos();

        selectionRect = new QGraphicsRectItem();
        selectionRect->setBrush(QBrush(QColor(158, 182, 255, 96)));
        selectionRect->setPen(QPen(QColor(158, 182, 255, 200), 1));
        addItem(selectionRect);
    }

    QGraphicsScene::mousePressEvent(event);
}

void PreviewScene::mouseMoveEvent(QGraphicsSceneMouseEvent* event)
{
    if (!mouseLeftButtonPressed)
    {
        QGraphicsScene::mouseMoveEvent(event);
        return;
    }

    // Form selection area
    QPointF scenePos = event->scenePos();

    if (scenePos.x() > mouseStartPosition.x())
    {
        if (scenePos.y() > mouseStartPosition.y())
        {
            setX0(mouseStartPosition.x());
            setY0(mouseStartPosition.y());
            setW(scenePos.x() - getX0());
            setH(scenePos.y() - getY0());
        }
        else
        {
            setX0(mouseStartPosition.x());
            setY0(scenePos.y());
            setW(scenePos.x() -getX0());
            setH(mouseStartPosition.y() - getY0());
        }
    }
    else
    {
        if (scenePos.y() > mouseStartPosition.y())
        {
            setX0(scenePos.x());
            setY0(mouseStartPosition.y());
            setW(mouseStartPosition.x() - getX0());
            setH(scenePos.y() - getY0());
        }
        else
        {
            setX0(scenePos.x());
            setY0(scenePos.y());
            setW(mouseStartPosition.x() - getX0());
            setH(mouseStartPosition.y() - getY0());
        }
    }

    selectionRect->setRect(getX0(), getY0(), getW(), getH());
    QGraphicsScene::mouseMoveEvent(event);
}

void PreviewScene::mouseReleaseEvent(QGraphicsSceneMouseEvent* event)
{
    if (event->button() == Qt::LeftButton)
        mouseLeftButtonPressed = false;

    QGraphicsScene::mouseReleaseEvent(event);
}
