#include "../include/outils.h"


// chaque indice du vector reprensente l'intensité donc la plus petite intensité de l'image reprensente le plus petite indice avec une valeur differnt de 0
long getMinH(const std::vector<long> &h){

    int i=0;
    while(i<256 && h[i]==0){
        i++;
    }
    return i;

};

// chaque indice du vector reprensente l'intensité donc la plus grande intensité de l'image reprensente le plus grand indice avec une valeur differnt de 0

long getMaxH(const std::vector<long> &h){

    int i= 255; 

    while(i>=0 && h[i]==0){
        i--;
    }
    return i;

};
