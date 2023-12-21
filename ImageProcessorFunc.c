#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void FormatImg(int *Cols, 
               int *Img, 
               unsigned char *Out,
               int W, 
               int H, 
               int Mode){

    //int *Out = (int*) malloc(W*H*3 * sizeof(int));

    switch(Mode){

        case 0:

            for (int i = 0; i < H; i++){
                for (int j = 0; j < W; j++){

                    Out[3*(i*W + j) + 0] = Cols[0 + (Img[i*W + j] * 3)];
                    Out[3*(i*W + j) + 1] = Cols[1 + (Img[i*W + j] * 3)];
                    Out[3*(i*W + j) + 2] = Cols[2 + (Img[i*W + j] * 3)];

                    //printf("%d\t%d\t%d\t%d\t%d\t%d\n", i, j, 3*i*W + 3*j, Out[3*i*W + 3*j + 0], Out[3*i*W + 3*j + 1], Out[3*i*W + 3*j + 2]);
                    //printf("%d\t%d\t%d\n", i, j, 3*i*W + 3*j);


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

    return;
}


void ColourDistance(int* ImgPalette, 
                    int* UserPalette, 
                    int* OutPalette,
                    int ImgPalLength, 
                    int UsrPalLength){

    int* RawDist = (int*) malloc(ImgPalLength * UsrPalLength * sizeof(int));

    double dR_Sq, dG_Sq, dB_Sq, Dist;

    for(int ImgCol = 0; ImgCol < ImgPalLength/3; ImgCol++){
        for(int UsrCol = 0; UsrCol < UsrPalLength/3; UsrCol++){

            dR_Sq = pow(ImgPalette[3*ImgCol + 0] - UserPalette[3*UsrCol + 0], 2);
            dG_Sq = pow(ImgPalette[3*ImgCol + 1] - UserPalette[3*UsrCol + 1], 2);
            dB_Sq = pow(ImgPalette[3*ImgCol + 2] - UserPalette[3*UsrCol + 2], 2);

            Dist = sqrt(dR_Sq + dG_Sq + dB_Sq) * 1000;

            RawDist[ImgCol*UsrPalLength + UsrCol] = (unsigned int)Dist;

        }
    }

    int MinVal, index;

    for(int ImgCol = 0; ImgCol < ImgPalLength/3; ImgCol++){

        MinVal = RawDist[ImgCol*UsrPalLength];
        index = 0;

        for(int UsrCol = 1; UsrCol < UsrPalLength/3; UsrCol++){  

            if (RawDist[ImgCol*UsrPalLength + UsrCol] < MinVal){

                MinVal = RawDist[ImgCol*UsrPalLength + UsrCol];

                index = UsrCol;
            }
        }
    
        OutPalette[ImgCol] = index;
    
    }

    free(RawDist);
    return;

}


void ResizeImage(int* Img, 
                 int InW, 
                 int InH, 
                 int* Resized,
                 int OutW, 
                 int OutH){

    double xPxStep = (double)InW / (double)OutW;
    double yPxStep = (double)InH / (double)OutH;    

    for(int Row = 0; Row < OutH; Row++){
        for(int Px = 0; Px < OutW; Px++){

            Resized[Row*OutW + Px] = Img[(int)(InW*floor(Row*yPxStep) + Px*xPxStep)];
            
        }

    }


    return;
}

void AdjustColours(int* Palette,
                   int* Adjusted,
                   int Len,
                   int H,
                   int S,
                   int V){

    double Hue, R, G, B, Saturation, Value, c, x, m, _R, _G, _B, MaxByte, MinByte, Diff;

    for (int Entry = 0; Entry < Len; Entry += 3){


        R = Palette[Entry + 0] / 255.0;
        G = Palette[Entry + 1] / 255.0;
        B = Palette[Entry + 2] / 255.0;

        //Convert to HSV

        MaxByte = fmax(R, fmax(G, B));
        MinByte = fmin(R, fmin(G, B));

        Diff = MaxByte - MinByte;

        if (Diff == 0){ //Calculate Hue

            Hue = 0;

        }else if (MaxByte == R){

            Hue = fmod(60*fmod( (G - B)/Diff, 6) + H, 360);

        }else if(MaxByte == G){

            Hue = fmod(60*((B - R)/Diff + 2) + H, 360);

        }else if(MaxByte == B){

            Hue = fmod(60*((R - G)/Diff + 4) + H, 360);

        }

        if(Hue < 0){

            Hue += 360;

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

        Adjusted[Entry + 0] = (int)((_R + m) * 255);
        Adjusted[Entry + 1] = (int)((_G + m) * 255);
        Adjusted[Entry + 2] = (int)((_B + m) * 255);

    }

    return;

}


void ParseColours(char* Colour,
                  int* rgbOut,
                  int NoEntries,
                  int LenEntry){


    char R[3], G[3], B[3];
    int Red, Green, Blue; 

    for (int Col = 0; Col < NoEntries * LenEntry * 2; Col += LenEntry*2 ){

        R[0] = Colour[Col+2];
        R[1] = Colour[Col+4];
        R[2] = '\0';

        G[0] = Colour[Col+6];
        G[1] = Colour[Col+8];
        G[2] = '\0';

        B[0] = Colour[Col+10];
        B[1] = Colour[Col+12];
        B[2] = '\0';

        Red = (int) strtol(R, NULL, 16);
        Green = (int) strtol(G, NULL, 16);
        Blue = (int) strtol(B, NULL, 16);

        rgbOut[3 * Col / (LenEntry * 2) + 0] = Red;
        rgbOut[3 * Col / (LenEntry * 2) + 1] = Green;
        rgbOut[3 * Col / (LenEntry * 2) + 2] = Blue;

    }

    return;
}

void FreeMem(int* P){

    free(P);

    return;
}

void ImageScaler(int* Image,
                 int* Scaled,
                 int ImgW,
                 int ImgH,
                 int Sx,
                 int Sy){

    int* LineBuffer = (int*) malloc(ImgW * Sx * sizeof(int));   //Buffer for duplicating lines
    int* ImgScaledX = (int*) malloc(ImgW * Sx * ImgH * sizeof(int));    //Intermediate buffer for image scaled in X

    for(int Row = 0; Row < ImgH; Row++){
        for(int Px = 0; Px < ImgW; Px++){
            for(int nX = 0; nX < Sx; nX++){

                ImgScaledX[Row*ImgW*Sx + Px*Sx + nX] = Image[Row*ImgW + Px];    //Duplicates pixel data Sx times

            }
        }
    }

    for(int Row = 0; Row < ImgH; Row++){

        for(int i = 0; i < ImgW*Sx; i++){
            LineBuffer[i] = ImgScaledX[Row*ImgW*Sx + i];    //Copy line to line buffer
        }

        for(int LineCopy = 0; LineCopy < Sy; LineCopy++){
            for(int i = 0; i < ImgW*Sx; i++){

                Scaled[ImgW*Sx*(Row*Sy + LineCopy) + i] = LineBuffer[i];   //Copy line buffer to final image

            }
        }
    }

    free(LineBuffer);
    free(ImgScaledX);

    return;

}