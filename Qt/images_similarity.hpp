#ifndef IMAGES_SIMILARITY_HPP
#define IMAGES_SIMILARITY_HPP
#include <opencv2/core.hpp>


namespace ImageComparison
{
double structural_similarity(cv::Mat& firstImage, cv::Mat& secondImage);
}
#endif // IMAGES_SIMILARITY_HPP
