#include"../include/histogramme.h"



std::vector<long> calculerHistogramme(const cv::Mat& img){

    std::vector<long> h (256,0); 
    for(int i= 0; i< img.rows; i++){
        for(int j=0; j< img.cols;j++){
            int intensite = img.at<uchar>(i,j); //on recuper l'intensité 
            h[intensite]++; 
        }
    }
    return h; 
}; 

std::vector<long> calculerHistoCumule(const std::vector<long>& h){

    std::vector<long> hc (256,0);
    long somme=0; 
    for(int i = 0; i<256;i++){ 
        somme+=h[i];
        hc[i]=somme; 

    }
    return hc;
};


void afficherHistogramme(const std::vector<long> &h, const std::string &nom){

    cv::Mat rendu (100, 256, CV_8UC1, cv::Scalar(255));

    //mis a l'echelle 
    long max= 0; 
    for(long val : h ){
        if( val > max){
            max=val; 
        }
    }

    for(int i=0; i<256;i++){

        int hauteurligne=(100*h[i])/max;   //produit en X
        cv::line(rendu,cv::Point(i, 100), cv::Point(i, 100 - hauteurligne), cv::Scalar(0)); // centre (0,0) en haut a gauche donc hauteur sur graph est 100-hauteur calculer
    }

    cv::imshow(nom,rendu);

};


cv::Mat etirementHistogramme(const cv::Mat& img){

    cv::Mat imgE=img.clone();
    std::vector<long> buff = calculerHistogramme(imgE);
    int min = getMinH(buff); //intensité la plus faible 
    int max = getMaxH(buff); //intensité la plus forte 

    if((min - max) == 0){ // pour evité de divisé par 0 apres 
        return imgE;
    }

    for(int i=0;i<imgE.rows;i++){
        for(int j=0;j<imgE.cols;j++){

            imgE.at<int>(i,j)= (imgE.at<uchar>(i,j) - min)/(max-min); //formule cours
        }
    }

    return imgE; 

};



