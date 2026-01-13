#include"../include/histogramme.h"


std::vector<long> calculerHistogramme(const cv::Mat& img){

    vector<long> h (256,0); 
    for(int i= 0; i< img.row; i++){
        for(int j=0; j< img.cols;j++){
            uchar intensite = img.at<uchar>(i,j); //on recuper l'intensité 
            h[intensite]++; 
        }
    }
    return h; 
}; 

