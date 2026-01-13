#ifndef _HISTOGRAMME_
#define _HISTOGRAMME_

#include <opencv2/opencv.hpp>
#include <vector>

// histogramme brut h(°) parcourt une img et compte le nb de pixel pour chaque intensité de 0 à 255 
std::vector<long> calculerHistogramme(const cv::Mat& img);

// histogramme cumulé HC(l)  donne le nombre de pixel ayant un valeur inferieur ou egale à un niveua de gris donné 
std::vector<double> calculerHistoCumule(const std::vector<long>& h, int nbPixels);

// Applique l'étirement (expansion) 
cv::Mat etirementContraste(const cv::Mat& img);

// Applique l'égalisation 
cv::Mat egalisationHisto(const cv::Mat& img);


#endif