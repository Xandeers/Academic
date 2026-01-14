#ifndef _HISTOGRAMME_
#define _HISTOGRAMME_

#include "../include/outils.h"
#include <opencv2/opencv.hpp>
#include<iostream>
#include <vector>


// histogramme brut h(°) parcourt une img et compte le nb de pixel pour chaque intensité de 0 à 255 
std::vector<long> calculerHistogramme(const cv::Mat& img);

// histogramme cumulé HC(l)  donne le nombre de pixel ayant un valeur inferieur ou egale à un niveua de gris donné 
std::vector<long> calculerHistoCumule(const std::vector<long>& h);


//afficher l'histogramme
void afficherHistogramme(const std::vector<long> &h, const std::string &nom);


cv::Mat etirementHistogramme(const cv::Mat& img);


#endif