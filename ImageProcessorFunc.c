#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int* FormatImg(int *Cols, 
               int *Img, 
               int W, 
               int H, 
               int Mode){

    int *Out = (int*) malloc(W*H*3 * sizeof(int));

    switch(Mode){

        case 0:

            for (int i = 0; i < H; i++){
                for (int j = 0; j < W; j++){

                    Out[3*i*W + 3*j + 0] = Cols[0 + (Img[i*W + j] * 3)];
                    Out[3*i*W + 3*j + 1] = Cols[1 + (Img[i*W + j] * 3)];
                    Out[3*i*W + 3*j + 2] = Cols[2 + (Img[i*W + j] * 3)];

                }
            }
            break;
    
        case 2:
    
            for (int i = 0; i < H; i++){
                for (int j = 0; j < W; j++){

                    Out[3*i*W + 3*j + 0] = Cols[12 + 0 + (Img[i*W + j] * 3)];
                    Out[3*i*W + 3*j + 1] = Cols[12 + 1 + (Img[i*W + j] * 3)];
                    Out[3*i*W + 3*j + 2] = Cols[12 + 2 + (Img[i*W + j] * 3)];

                }
            }
            break;

        case 4:

            for (int i = 0; i < H; i++){
                for (int j = 0; j < W; j++){

                    Out[3*i*W + 3*j + 0] = Cols[60 + 0 + (Img[i*W + j] * 3)];
                    Out[3*i*W + 3*j + 1] = Cols[60 + 1 + (Img[i*W + j] * 3)];
                    Out[3*i*W + 3*j + 2] = Cols[60 + 2 + (Img[i*W + j] * 3)];

                }
            }
            break;
    }
    return Out;
}


int* ColourDistance(int* ImgPalette, 
                    int* UserPalette, 
                    int ImgPalLength, 
                    int UsrPalLength){

    int* RawDist = (int*) malloc(ImgPalLength * UsrPalLength * sizeof(int));
    int* Out = (int*) malloc(ImgPalLength * UsrPalLength * sizeof(int) / 4);

    for(int ImgCol = 0; ImgCol < ImgPalLength/3; ImgCol++){
        for(int UsrCol = 0; UsrCol < UsrPalLength/3; UsrCol++){

            double dR_Sq = pow(ImgPalette[3*ImgCol + 0] - UserPalette[3*UsrCol + 0], 2);
            double dG_Sq = pow(ImgPalette[3*ImgCol + 1] - UserPalette[3*UsrCol + 1], 2);
            double dB_Sq = pow(ImgPalette[3*ImgCol + 2] - UserPalette[3*UsrCol + 2], 2);

            double Dist = sqrt(dR_Sq + dG_Sq + dB_Sq) * 1000;

            RawDist[ImgCol*UsrPalLength + UsrCol] = (unsigned int)Dist;

        }
    }

    for(int ImgCol = 0; ImgCol < ImgPalLength/3; ImgCol++){

        int MinVal = RawDist[ImgCol*UsrPalLength];
        int index = 0;

        for(int UsrCol = 1; UsrCol < UsrPalLength/3; UsrCol++){  

            if (RawDist[ImgCol*UsrPalLength + UsrCol] < MinVal){

                MinVal = RawDist[ImgCol*UsrPalLength + UsrCol];

                index = UsrCol;
            }
        }
    
        Out[ImgCol] = index;
    
    }

    return Out;

}


int* ResizeImage(int* Img, int InW, int InH, int OutW, int OutH){

    double xPxStep = (double)InW / (double)OutW;
    double yPxStep = (double)InH / (double)OutH;    

    int* Resized = (int*) malloc(OutW * OutH * sizeof(int));

    for(int Row = 0; Row < OutH; Row++){
        for(int Px = 0; Px < OutW; Px++){

            Resized[Row*OutW + Px] = Img[(int)(InW*floor(Row*yPxStep) + Px*xPxStep)];

        }

    }


    return Resized;
}