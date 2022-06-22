#ifndef PDF_HPP
#define PDF_HPP
#include <QtCore>
#include <hpdf.h>


namespace Pdf
{
void errorHandler(HPDF_STATUS error_no, HPDF_STATUS detail_no, void* user_data);
void createPdfFromImages(std::vector<QString> videoImages, QString outputDirectory,
                         QString videoPath, int width, int height);
}

#endif // PDF_HPP
