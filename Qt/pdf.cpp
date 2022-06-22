#include <stdio.h>
#include <filesystem>
#include <QtCore>
#include "pdf.hpp"


void Pdf::errorHandler(HPDF_STATUS error_no, HPDF_STATUS detail_no, void* user_data)
{
    printf("ERROR: error_no=%04X, detail_no=%u\n", (HPDF_UINT)error_no, (HPDF_UINT)detail_no);
}

void Pdf::createPdfFromImages(std::vector<QString> videoImages, QString outputDirectory,
                              QString videoPath, int width, int height)
{
    QString filepath = QFile(videoPath).fileName();
    QString filename = filepath.split(".").at(0) + ".pdf";

    HPDF_Doc pdf = HPDF_New(errorHandler, NULL);

    for (const QString& image : videoImages)
    {
        HPDF_Page page = HPDF_AddPage(pdf);
        HPDF_Page_SetWidth(page, width);
        HPDF_Page_SetHeight(page, height);

        HPDF_Image hpdfImage = HPDF_LoadPngImageFromFile(pdf, image.toStdString().c_str());
        HPDF_Page_DrawImage(page, hpdfImage, 0, 0, width, height);
    }

    QString pdfFilepath = QDir(outputDirectory).filePath(filename);
    HPDF_SaveToFile(pdf, pdfFilepath.toStdString().c_str());
    HPDF_Free(pdf);
}
