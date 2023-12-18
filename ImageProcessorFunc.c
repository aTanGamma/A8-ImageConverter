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


int* ResizeImage(int* Img, 
                 int InW, 
                 int InH, 
                 int OutW, 
                 int OutH){

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

int* AdjustColours(int* Palette,
                   int Len,
                   int H,
                   int S,
                   int V){

    int* Adjusted = (int*) malloc(Len * sizeof(int));

    double Hue, R, G, B, Saturation, Value, c, x, m, _R, _G, _B;

    for (int Entry = 0; Entry < Len; Entry += 3){

        R = Palette[Entry + 0] / 255.0;
        G = Palette[Entry + 1] / 255.0;
        B = Palette[Entry + 2] / 255.0;

        //Convert to HSV

        double MaxByte = fmax(R, fmax(G, B));
        double MinByte = fmin(R, fmin(G, B));

        double Diff = MaxByte - MinByte;

        if (Diff == 0){ //Calculate Hue

            Hue = 0;

        }else if (MaxByte == R){

            Hue = fmod(60*fmod( (G - B)/Diff, 6) + H, 360);

        }else if(MaxByte == G){

            Hue = fmod((60*((B - R)/Diff + 2) + H), 360);

        }else{

            Hue = fmod((60*((R - G)/Diff + 4) + H), 360);

        }

        if (MaxByte == 0){  //Calculate Saturation

            Saturation = 0;

        }else{

            Saturation = (Diff / MaxByte) * pow(2, S/50.0);
            
            
            if (Saturation > 1){
                Saturation = 1;
            }

        }

        Value = MaxByte * pow(2, V/50.0); //Calculate brightness

        if (Value > 1){
            Value = 1;
        }

        //Convert back to RGB

        c = Saturation * Value;
        x = c * (1 - fabs(fmod((Hue/60.0) , 2) - 1));
        m = Value - c;

        if(Hue < 60){
            _R = c;
            _G = x;
            _B = 0;

        }else if(Hue < 120){
            _R = x;
            _G = c;
            _B = 0;

        }else if(Hue < 180){
            _R = 0;
            _G = c;
            _B = x;

        }else if(Hue < 240){
            _R = 0;
            _G = x;
            _B = c;

        }else if(Hue < 300){
            _R = x;
            _G = 0;
            _B = c;

        }else{
            _R = c;
            _G = 0;
            _B = x;
        }

        R = (_R + m) * 255;
        G = (_G + m) * 255;
        B = (_B + m) * 255;

        Adjusted[Entry + 0] = (int)((_R + m) * 255);
        Adjusted[Entry + 1] = (int)((_G + m) * 255);
        Adjusted[Entry + 2] = (int)((_B + m) * 255);

    }

    return Adjusted;

}
