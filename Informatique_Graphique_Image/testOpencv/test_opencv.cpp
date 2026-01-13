#include <iostream>
#include <opencv2/opencv.hpp>

int main() {
    // Test 1 : Afficher la version
    std::cout << "=== TEST OPENCV ===" << std::endl;
    std::cout << "Version compile-time: " << CV_VERSION << std::endl;
    
    // Test 2 : Vérifier les modules disponibles
    #ifdef HAVE_OPENCV_CORE
        std::cout << "OpenCV Core: OK" << std::endl;
    #endif
    
    #ifdef HAVE_OPENCV_HIGHGUI
        std::cout << "OpenCV HighGUI: OK" << std::endl;
    #endif
    
    #ifdef HAVE_OPENCV_IMGCODECS
        std::cout << "OpenCV ImgCodecs: OK" << std::endl;
    #endif
    
    // Test 3 : Créer une image simple
    cv::Mat testImage(100, 100, CV_8UC3, cv::Scalar(0, 0, 255)); // Image rouge
    std::cout << "Image créée: " << testImage.cols << "x" << testImage.rows << std::endl;
    
    // Test 4 : Afficher l'image
    cv::imshow("Test OpenCV", testImage);
    
    // Test 5 : Attendre
    std::cout << "Fenêtre affichée. Appuyez sur une touche..." << std::endl;
    cv::waitKey(0);
    
    std::cout << "Test réussi !" << std::endl;
    return 0;
}