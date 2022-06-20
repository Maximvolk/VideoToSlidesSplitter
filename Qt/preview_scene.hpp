#ifndef PREVIEWSCENE_HPP
#define PREVIEWSCENE_HPP

#include <QtWidgets/QGraphicsScene>
#include <QtWidgets/QGraphicsRectItem>


class PreviewScene : public QGraphicsScene
{
    Q_OBJECT

public:
    PreviewScene(QObject* parent);

    void createPreviewFromVideo(QString videoPath);
    void resetSelection();
    void removePreview();

    int getX0() { return x0; }
    void setX0(int value)
    {
        if (value < 0)
            x0 = 0;
        else
            x0 = value;
    }

    int getY0() { return y0; }
    void setY0(int value)
    {
        if (value < 0)
            y0 = 0;
        else
            y0 = value;
    }

    int getW() { return w; }
    void setW(int value)
    {
        if (x0 + value > maxWidth)
            w = maxWidth - x0;
        else
            w = value;
    }

    int getH() { return h; }
    void setH(int value)
    {
        if (y0 + value > maxHeight)
            h = maxHeight - y0;
        else
            h = value;
    }

protected:
    void mousePressEvent(QGraphicsSceneMouseEvent* event) override;
    void mouseMoveEvent(QGraphicsSceneMouseEvent* event) override;
    void mouseReleaseEvent(QGraphicsSceneMouseEvent* event) override;

private:
    bool mouseLeftButtonPressed = false;
    QPointF mouseStartPosition;
    QGraphicsRectItem* selectionRect {nullptr};
    QGraphicsPixmapItem* previewPixmapItem {nullptr};

    int maxWidth = (int)this->width();
    int maxHeight = (int)this->height();

    int x0;
    int y0;
    int w;
    int h;
};

#endif // PREVIEWSCENE_HPP
