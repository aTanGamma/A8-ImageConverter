import numpy as np
import PySimpleGUI as gui
import os.path
import os
from PIL import Image
import io
from ctypes import *
import time
from copy import deepcopy


def ColPick_Window():

    AtariCols = [
    ['#000000', '#252525', '#464646', '#6B6B6B', '#838383', '#A8A8A8', '#CACACA', '#EEEEEE'],
    ['#3E0100', '#631800', '#853A00', '#A85E06', '#C2771F', '#E79C44', '#FFBD65', '#FFE28A'],
    ['#500100', '#750500', '#962716', '#BB4B3B', '#D36454', '#F88978', '#FFAA9A', '#FFCFBF'],
    ['#540103', '#790327', '#9A1B49', '#BF3F6D', '#D85886', '#FC7DAB', '#FF9ECC', '#FFC3F1'],
    ['#4F0135', '#740259', '#95147B', '#BA389F', '#D251B8', '#F776DD', '#FF97FE', '#FFBCFF'],
    ['#3D0068', '#61018D', '#8313AD', '#A638D3', '#C050EC', '#E575FF', '#FF96FF', '#FFBBFF'],
    ['#20008B', '#4500AF', '#661BD1', '#8B3FF6', '#A458FF', '#C87DFF', '#EA9EFF', '#FFC3FF'],
    ['#020089', '#021CAD', '#233DCF', '#4961F3', '#617BFF', '#859FFF', '#A7C1FF', '#CBE5FF'],
    ['#000C65', '#003189', '#0753AB', '#2C77CE', '#4590E7', '#6AB4FF', '#8BD6FF', '#B0FBFF'],
    ['#001F30', '#014454', '#006676', '#1B8A9A', '#34A3B3', '#58C8D8', '#7AE9F9', '#9EFFFF'],
    ['#002B00', '#005022', '#017144', '#169668', '#2EAF81', '#54D3A5', '#76F5C7', '#9AFFEC'],
    ['#003300', '#005800', '#087900', '#2E9E02', '#47B71B', '#6BDB40', '#8DFD61', '#B2FF86'],
    ['#002B00', '#055000', '#267200', '#4A9600', '#63AF00', '#88D31C', '#A9F53E', '#CEFF63'],
    ['#011C00', '#264100', '#486300', '#6C8700', '#85A000', '#A9C412', '#CBE633', '#F0FF58'],
    ['#230900', '#482D00', '#694F00', '#8E7300', '#A68C00', '#CBB11F', '#EDD241', '#FFF765'],
    ['#3E0100', '#631800', '#853A00', '#A85E06', '#C2771F', '#E79C44', '#FFBD65', '#FFE28A']
    ]#Colours coutesy of Thelen from Atariage

    Col = None
    Lum = None

    layout = [
        [[gui.Button(button_text="",pad=(0, 0), size= (3, 2), key = "{},{}".format(i, j), button_color=AtariCols[i][j]) 
         for i in range(16)] 
         for j in range(8)],
         [gui.Button("Cancel")]
    ]

    ColWindow = gui.Window("Colour picker", layout, modal= True)

    while True:

        event, value = ColWindow.read()

        if event == gui.WIN_CLOSED:
            break

        if event == "Cancel":
            break

        if event != None:
            Col, Lum = int(event.split(",")[0]), int(event.split(",")[1])
            break
    
    ColWindow.close()
    
    if Col == None or Lum == None:
        return [AtariCols[0][0], Col, Lum]
    else:
        return [AtariCols[Col][Lum], Col, Lum]

def HueValPick_Window():

    FullColours = [
    ['#000000', '#111111', '#252525', '#353535', '#464646', '#575757', '#6B6B6B', '#7C7C7C', '#838383', '#949494', '#A8A8A8', '#B9B9B9', '#CACACA', '#DADADA', '#EEEEEE', '#FFFFFF'], 
    ['#3C0000', '#4C0700', '#601B00', '#712C00', '#823C00', '#934D00', '#A66100', '#B77211', '#BF7A19', '#D08B2A', '#E49E3E', '#F4AF4F', '#FFC05F', '#FFD170', '#FFE484', '#FFF595'], 
    ['#4B0000', '#5C0000', '#700B00', '#811C00', '#912D03', '#A23E13', '#B65127', '#C76238', '#CF6A40', '#E07B51', '#F38F65', '#FFA075', '#FFB086', '#FFC197', '#FFD5AB', '#FFE6BB'], 
    ['#500015', '#610026', '#74003A', '#85094A', '#96195B', '#A72A6C', '#BB3E80', '#CB4F91', '#D35798', '#E468A9', '#F87BBD', '#FF8CCE', '#FF9DDF', '#FFAEEF', '#FFC1FF', '#FFD2FF'], 
    ['#3D0067', '#4E0078', '#62008C', '#73029D', '#8313AE', '#9424BE', '#A838D2', '#B948E3', '#C150EB', '#D161FC', '#E575FF', '#F686FF', '#FF96FF', '#FFA7FF', '#FFBBFF', '#FFCCFF'], 
    ['#280084', '#390095', '#4C00A9', '#5D07BA', '#6E18CB', '#7F29DB', '#933DEF', '#A34EFF', '#AB55FF', '#BC66FF', '#D07AFF', '#E18BFF', '#F19CFF', '#FFACFF', '#FFC0FF', '#FFD1FF'], 
    ['#0F0094', '#1F00A5', '#3300B9', '#4411C9', '#5522DA', '#6533EB', '#7947FF', '#8A57FF', '#925FFF', '#A370FF', '#B784FF', '#C795FF', '#D8A6FF', '#E9B6FF', '#FDCAFF', '#FFDBFF'], 
    ['#000086', '#000A97', '#001EAB', '#102FBC', '#203FCC', '#3150DD', '#4564F1', '#5675FF', '#5E7DFF', '#6E8EFF', '#82A1FF', '#93B2FF', '#A4C3FF', '#B5D4FF', '#C8E7FF', '#D9F8FF'], 
    ['#000A6A', '#001B7B', '#002E8F', '#003FA0', '#0B50B0', '#1B61C1', '#2F74D5', '#4085E6', '#488DEE', '#599EFF', '#6CB2FF', '#7DC3FF', '#8ED3FF', '#9FE4FF', '#B3F8FF', '#C3FFFF'], 
    ['#001944', '#002A54', '#003E68', '#004F79', '#005F8A', '#0C709A', '#1F84AE', '#3095BF', '#389DC7', '#49AED8', '#5DC1EC', '#6ED2FC', '#7EE3FF', '#8FF4FF', '#A3FFFF', '#B4FFFF'], 
    ['#002D00', '#003E00', '#005110', '#006220', '#007331', '#078442', '#1B9756', '#2CA867', '#34B06E', '#44C17F', '#58D593', '#69E6A4', '#7AF6B5', '#8BFFC5', '#9EFFD9', '#AFFFEA'], 
    ['#002E00', '#003F00', '#005300', '#0E6300', '#1E7400', '#2F8500', '#439900', '#54AA00', '#5CB100', '#6CC210', '#80D624', '#91E734', '#A2F845', '#B3FF56', '#C6FF6A', '#D7FF7B'], 
    ['#002400', '#023500', '#164900', '#275900', '#386A00', '#487B00', '#5C8F00', '#6DA000', '#75A800', '#86B800', '#9ACC14', '#AADD25', '#BBEE36', '#CCFF46', '#E0FF5A', '#F0FF6B'], 
    ['#0C1700', '#1D2700', '#313B00', '#424C00', '#525D00', '#636E00', '#778100', '#889200', '#909A00', '#A1AB00', '#B4BF13', '#C5CF24', '#D6E035', '#E7F146', '#FBFF5A', '#FFFF6A'], 
    ['#260700', '#371800', '#4A2B00', '#5B3C00', '#6C4D00', '#7D5E00', '#917100', '#A18200', '#A98A00', '#BA9B0E', '#CEAF22', '#DFC033', '#EFD043', '#FFE154', '#FFF568', '#FFFF79'], 
    ['#3C0000', '#4C0700', '#601B00', '#712C00', '#823C00', '#934D00', '#A66100', '#B77211', '#BF7A19', '#D08B2A', '#E49E3E', '#F4AF4F', '#FFC05F', '#FFD170', '#FFE484', '#FFF595'], 
    ]#Extracted from Altirra64

    Hues = None
    Vals = None

    layout = [
        [[gui.Button(button_text="",pad=(0, 0), size= (2,1), key = "{},{}".format(i, j), button_color=FullColours[i][j]) 
         for i in range(16)] 
         for j in range(16)],
         [gui.Button("Cancel")]
    ]

    ColWindow = gui.Window("Colour picker", layout, modal= True)

    while True:

        event, value = ColWindow.read()

        if event == gui.WIN_CLOSED:
            break

        if event == "Cancel":
            break

        if event != None:
            Row, Column = int(event.split(",")[0]), int(event.split(",")[1])
            Hues = FullColours[Row]
            Vals = [FullColours[i][Column] for i in range(16)]

            break
    
    ColWindow.close()


    return [Hues, Vals]

def Export(Img, Path, img, asm, dlist):

    if img:
        try:
            Img.save(Path+"Converted.png")
        except:
            gui.popup_error("Error saving file >:3")
        
    if asm:
    
        return 0

    if dlist:

        return 0

    return 0

def ImgProcessor(Path, Mode, Auto, OutW, OutH, Width, Rastered,Hue, Sat, Brightness, *Cols):

    def ParseCols(ColArray):

        
        FlatColours = ''.join([Letter for Colour in ColArray for Letter in Colour])
        ParsedCols = (c_int * (len(ColArray) * 3))()
        ImgProcesses.ParseColours(FlatColours, byref(ParsedCols), len(ColArray), len(ColArray[0]))

        return ParsedCols
    
    def CalcColDist(ImgPalette, UsrPalette):

        UsrColArray = (c_uint * len(UsrPalette))()
        UsrColArray[:] = UsrPalette
        
        ImgColArray = (c_uint * len(ImgPalette))()
        ImgColArray[:] = ImgPalette

        CDist = (c_uint * (len(UsrPalette) // 3 * len(ImgPalette)//3 // 4))()

        ImgProcesses.ColourDistance(ImgColArray, UsrColArray, byref(CDist), len(ImgColArray), len(UsrColArray))

        return CDist

    def ImgResizer(Img, ImgW, ImgH, OutW, OutH):   #Takes image formatted as [[R...G...B], ...[R...G...B...]] and shrinks it to desired resolution

        ImgArray = (c_uint * len(Img))()
        ImgArray[:] = Img

        Resized = (c_int * (OutW * OutH))()
        ImgProcesses.ResizeImage(ImgArray, ImgW, ImgH, byref(Resized), OutW, OutH)

        return Resized

    def ImgScaler(Img, Sx, Sy, ImgW, ImgH):


        ImgArray = (c_int * len(Img))()
        ImgArray[:] = Img

        t_Scaled = (c_int * (len(Img) * Sx * Sy))()
        ImgProcesses.ImageScaler(ImgArray, byref(t_Scaled), ImgW, ImgH, Sx, Sy)

        NewW = ImgW * Sx
        NewH = ImgH * Sy

        #print(t_Scaled[0:20], '\n', Flattened[0:20])

        return t_Scaled, NewW, NewH

    def AdjustCols(H, S, V, *ImgCols):

        #Explanations of algorithms from 
        #https://www.rapidtables.com/convert/color/hsv-to-rgb.html 
        #and 
        #https://www.rapidtables.com/convert/color/rgb-to-hsv.html

        flatCols = [rgb for Col in ImgCols[0] for rgb in Col]
        flatColArray = (c_int * len(flatCols))()
        flatColArray[:] = [*flatCols]

        AdjustedRGB = (c_int * (len(flatCols)))()

        ImgProcesses.AdjustColours(flatColArray, byref(AdjustedRGB), len(flatColArray), int(H), int(S), int(V))

        return AdjustedRGB

    #Does all the image processing
    
    ImgProcesses = CDLL("D:\Code\Atari\Projects\ImageConverter\ImgProcesses.so")

    InputImg = Image.open(Path)

    ImgWidth, ImgHeight = InputImg.size
    ImgData = list(InputImg.getdata())

    Palettised = False

    if InputImg.getpalette() == None: #Get colours / palette

        RawPalette = InputImg.getcolors(ImgWidth*ImgHeight)
        
        if not RawPalette:
            InputImg.close()
            raise Exception('Error collecting image palette...')
        
        ImgPalette = [[RawPalette[i][1][0], RawPalette[i][1][1], RawPalette[i][1][2]] for i in range(len(RawPalette))]

        Palettised = False

    else:

        RawPalette = InputImg.getpalette()
        ImgPalette = [[RawPalette[3*i], RawPalette[(3*i)+1], RawPalette[(3*i)+2]] for i in range(len(RawPalette) // 3)]   
        
        Palettised = True

    if Palettised == True:
        
        IntCols = ParseCols(Cols) #Convert list of strings'#RRGGBB' to flat list containing [RR, GG, BB, RR, GG, BB ...]

        ImgPalette = AdjustCols(Hue, Sat, Brightness, ImgPalette)   #Adjusts the image colour palette brightness

        #flatCols = np.array([N for a in ImgPalette for N in a], dtype=np.uint)
        IntColArray = (c_uint * len(ImgPalette))()
        IntColArray[:] = ImgPalette

        TempAdjImg = np.array(ImgData, dtype=np.uint)
        ImgArrayPtr = (c_uint * len(TempAdjImg))()
        ImgArrayPtr[:] = TempAdjImg

        AdjustedImg = (c_uint8 * (ImgWidth*ImgHeight*3))()
        ImgProcesses.FormatImg(IntColArray, ImgArrayPtr, byref(AdjustedImg), ImgWidth, ImgHeight, 0)
        AdjustedImg = np.array(AdjustedImg).astype(np.uint8)
        AdjustedImg.shape = (ImgHeight, ImgWidth, 3)


        ShrunkImg = [[0,0,0]]
        TempImg = [[0,0,0]]
        NewImg = [[0,0,0]]

        if Mode == 0:   #160x96, not interlaced

            ShrunkImg = ImgResizer(ImgData, ImgWidth, ImgHeight, OutW, OutH)
            
            RefPalette = CalcColDist(ImgPalette, IntCols[0:12]) #Finds the distance btween all colours in image and selected palette, creating a referance palette
            NewImgCols = [RefPalette[ShrunkImg[i]] for i in range(len(ShrunkImg))]  #Convert old image to new colour space
            ResizedTempImg, TempW, TempH = ImgScaler(NewImgCols, 4, 4, OutW, OutH)

            IntColArray = (c_uint * len(IntCols))()
            IntColArray[:] = IntCols
            
            TempIntImg = np.array(ResizedTempImg, dtype=np.uint)
            ImgArrayPtr = (c_uint * len(TempIntImg))()
            ImgArrayPtr[:] = TempIntImg

            t_TempImg = (c_uint8 * (TempW*TempH*3))()
            ImgProcesses.FormatImg(IntColArray, ImgArrayPtr, byref(t_TempImg), TempW, TempH, 0)
            TempImg = np.array(t_TempImg)
            TempImg.shape = (TempH, TempW, 3)

            OutIntImg = np.array(NewImgCols, dtype=np.uint)
            ImgArrayPtr = (c_uint * len(OutIntImg))()
            ImgArrayPtr[:] = OutIntImg

            t_NewImg = (c_uint8 * (OutW*OutH*3))()
            ImgProcesses.FormatImg(IntColArray, ImgArrayPtr, byref(t_NewImg), OutW, OutH, 0)
            NewImg = np.array(t_NewImg)
            NewImg.shape = (OutH, OutW, 3)

                         
        elif Mode == 2: #80x192, 16 Lum, not interlaced

            ShrunkImg = ImgResizer(ImgData, ImgWidth, ImgHeight, OutW, OutH)
            RefPalette = CalcColDist(ImgPalette, IntCols[12:60])    #Finds the distance btween all colours in image and selected palette, creating a referance palette       
            NewImgCols = [RefPalette[ShrunkImg[i]] for i in range(len(ShrunkImg))]  #Convert old image to new colour space
            ResizedTempImg, TempW, TempH = ImgScaler(NewImgCols, 8, 2, OutW, OutH)

            IntColArray = (c_uint * len(IntCols))()
            IntColArray[:] = IntCols

            TempIntImg = np.array(ResizedTempImg, dtype=np.uint)
            ImgArrayPtr = (c_uint * len(TempIntImg))()
            ImgArrayPtr[:] = TempIntImg

            t_TempImg = (c_uint8 * (TempW*TempH*3))()
            ImgProcesses.FormatImg(IntColArray, ImgArrayPtr, byref(t_TempImg), TempW, TempH, 2)
            TempImg = np.array(t_TempImg)
            TempImg.shape = (TempH, TempW, 3)

            OutIntImg = np.array(NewImgCols, dtype=np.uint)
            ImgArrayPtr = (c_uint * len(OutIntImg))()
            ImgArrayPtr[:] = OutIntImg

            t_NewImg = (c_uint8 * (OutW*OutH*3))()
            ImgProcesses.FormatImg(IntColArray, ImgArrayPtr, byref(t_NewImg), OutW, OutH, 2)
            NewImg = np.array(t_NewImg)
            NewImg.shape = (OutH, OutW, 3)

                     
        elif Mode == 4: #80x192, 16 Col, not interlaced

            ShrunkImg = ImgResizer(ImgData, ImgWidth, ImgHeight, OutW, OutH)
            RefPalette = CalcColDist(ImgPalette, IntCols[60:108])    #Finds the distance btween all colours in image and selected palette, creating a referance palette
            NewImgCols = [RefPalette[ShrunkImg[i]] for i in range(len(ShrunkImg))]  #Convert old image to new colour space
            ResizedTempImg, TempW, TempH = ImgScaler(NewImgCols, 8, 2, OutW, OutH)

            IntColArray = (c_uint * len(IntCols))()
            IntColArray[:] = IntCols

            TempIntImg = np.array(ResizedTempImg, dtype=np.uint)
            ImgArrayPtr = (c_uint * len(TempIntImg))()
            ImgArrayPtr[:] = TempIntImg

            t_TempImg = (c_uint8 * (TempW*TempH*3))()
            ImgProcesses.FormatImg(IntColArray, ImgArrayPtr, byref(t_TempImg), TempW, TempH, 4)
            TempImg = np.array(t_TempImg)
            TempImg.shape = (TempH, TempW, 3)

            OutIntImg = np.array(NewImgCols, dtype=np.uint)
            ImgArrayPtr = (c_uint * len(OutIntImg))()
            ImgArrayPtr[:] = OutIntImg

            t_NewImg = (c_uint8 * (OutW*OutH*3))()
            ImgProcesses.FormatImg(IntColArray, ImgArrayPtr, byref(t_NewImg), OutW, OutH, 4)
            NewImg = np.array(t_NewImg)
            NewImg.shape = (OutH, OutW, 3)
            
            
        OutViewerPNG = Image.fromarray(TempImg, 'RGB')
        with io.BytesIO() as OutViewer:
            OutViewerPNG.save(OutViewer, format="PNG")
            window["OutView"].update(data=OutViewer.getvalue())
            OutViewerPNG.close()
            OutViewer.close()


        AdjustedImgPNG = Image.fromarray(np.array(AdjustedImg).astype(np.uint8), mode = 'RGB' )
        with io.BytesIO() as InViewer:
            AdjustedImgPNG.save(InViewer, format="PNG")
            window["-IN_IMG-"].update(data = InViewer.getvalue())
            AdjustedImgPNG.close()
            
            InViewer.truncate(0)
            InViewer.close()

        NewImgPNG = Image.fromarray(NewImg, 'RGB')

    return NewImgPNG


gui.theme("Topanga")

FilePicker = [  #Box @ top of screen to browse for input image
    [
        gui.Text("Input image"),
        gui.In(size=(25, 1), enable_events=True, key="-PICK_IMG-"),
        gui.FileBrowse(),
        gui.Button(button_text="About")
    ]
]

ImagePreview = [    #Show input image with filename
    [gui.Image( key = "-IN_IMG-", size=(256,256))],
    [gui.Frame(layout=[
                
                [gui.Text("Hue", expand_x=True), 
                gui.Slider(range = (-180,180), 
                        resolution=1, 
                        default_value=0, 
                        orientation='horizontal',
                        key = 'InHue',
                        enable_events=True),
                gui.Button(button_text="Reset", key="Reset_Hue")],

                [gui.Text("Saturation", expand_x=True), 
                gui.Slider(range = (-100,100), 
                        resolution=1, 
                        default_value=0, 
                        orientation='horizontal',
                        key = 'InSat',
                        enable_events=True),
                gui.Button(button_text="Reset", key="Reset_Sat")],
                
                [gui.Text("Brightness", expand_x=True), 
                gui.Slider(range = (-100,100), 
                        resolution=1, 
                        default_value=0, 
                        orientation='horizontal',
                        key = 'InBright',
                        enable_events=True),
                gui.Button(button_text="Reset", key="Reset_Bright")],
                
                ],
                title='Image adjustments'
    )]
]

GFXModePicker = [

    [gui.Radio("160 x 96 px, 4-Colours", "gfxMode", enable_events= True, key = "160x96", default = True)],
    [gui.Radio("80 x 192 px, 1 Colour & 16 Luminance", "gfxMode", enable_events= True, key = "80x192_L")],
    [gui.Radio("80 x 192 px, 16 Colour & 1 Luminance", "gfxMode", enable_events= True, key = "80x192_C")],
    [gui.HorizontalSeparator()],
    [gui.Radio("Normal", "gfxMode2", enable_events=True, default=True, key='FullRes')],
    [gui.Radio("Half Resolution (Every other line)", "gfxMode2", enable_events=True, key='HalfRes')],
    [gui.HorizontalSeparator()],
    [gui.Radio("Wide", "gfxWidth", enable_events=True, key= 'Wide')],
    [gui.Radio("Normal", "gfxWidth", enable_events=True, default=True, key= 'Normal')],
    [gui.Radio("Narrow", "gfxWidth", enable_events=True, key= 'Narrow')],

]

ColourModePicker = [
        [gui.Radio("Automatic *Not Implemented*", "ColMode",enable_events= True,  key = "-AutoCol-", default = True)],
        [gui.Radio("Manual", "ColMode", enable_events= True, key = "-ManualCol-")],
]

ManualColours_4 = [

    [gui.Text("Colour Picker:")],
    [gui.Button(button_text="\t", key = "4_C0", button_color="#808080", pad=(0,0))],
    [gui.Button(button_text="\t", key = "4_C1", button_color="#808080", pad=(0,0))],
    [gui.Button(button_text="\t", key = "4_C2", button_color="#808080", pad=(0,0))],
    [gui.Button(button_text="\t", key = "4_C3", button_color="#808080", pad=(0,0))],
]

ManualColours_16Col = [

    [gui.Text("Chroma mode:"), gui.Button(button_text="Choose Value", key="C_Val")],
    [gui.Button(button_text="\t", key = "C_C0", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "C_C8", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "C_C1", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "C_C9", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "C_C2", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "C_CA", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "C_C3", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "C_CB", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "C_C4", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "C_CC", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "C_C5", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "C_CD", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "C_C6", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "C_CE", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "C_C7", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "C_CF", button_color="#808080", enable_events=False, pad=(0,0))],

]

ManualColours_16Lum = [

    [gui.Text("Luma Mode:"), gui.Button(button_text="Choose Hue", key="L_Hue")],
    [gui.Button(button_text="\t", key = "L_C0", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "L_C8", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "L_C1", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "L_C9", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "L_C2", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "L_CA", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "L_C3", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "L_CB", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "L_C4", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "L_CC", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "L_C5", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "L_CD", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "L_C6", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "L_CE", button_color="#808080", enable_events=False, pad=(0,0))],
    [gui.Button(button_text="\t", key = "L_C7", button_color="#808080", enable_events=False, pad=(0,0)), gui.Button(button_text="\t", key = "L_CF", button_color="#808080", enable_events=False, pad=(0,0))],

]

Output_Viewer = [
    [gui.Image(key="OutView", size =(256,256))],
]

OutputDimensions = [
    [gui.Text("Width"), 
     gui.Spin([i for i in range(321)], initial_value = 160, key = 'OutViewWidth', enable_events=True, size=(3,1), bind_return_key=True), 
     gui.Text("Height"), 
     gui.Spin([i for i in range(193)], initial_value = 96, key = 'OutViewHeight', enable_events=True, size=(3,1), bind_return_key=True)],
     
     [gui.Text(text="Output width too large!\nMust be <= 160.", 
               text_color='#FF0000', 
               background_color='#101010', 
               visible = False, 
               key = "Err_W_160"),
     
     gui.Text(text="Output height too large!\nMust be <= 96.", 
               text_color='#FF0000', 
               background_color='#101010', 
               visible = False, 
               key = "Err_H_96"),

     gui.Text(text="Output dimensions too large!\nWidth <= 160 and H <= 96", 
               text_color='#FF0000', 
               background_color='#101010', 
               visible = False, 
               key = "Err_WH_160_96"),
     
     gui.Text(text="Output width too large!\nMust be <= 80", 
               text_color='#FF0000', 
               background_color='#101010', 
               visible = False, 
               key = "Err_W_80"),
     
     gui.Text(text="Output height too large!\nMust be <= 192", 
               text_color='#FF0000', 
               background_color='#101010', 
               visible = False, 
               key = "Err_H_192"),
     
     gui.Text(text="Output dimensions too large!\nWidth <= 80 and H <= 192", 
               text_color='#FF0000', 
               background_color='#101010', 
               visible = False, 
               key = "Err_WH_80_192")],

]

ExportButton = gui.Frame(layout =[
                [gui.Checkbox("Image?", key="Img?"),
                gui.Checkbox(".asm?", key="asm?"),
                gui.Checkbox("Display List?", key="DList?")],
                
                [gui.Text("Save path:"), gui.Input('', enable_events=False, expand_x=True, key="SaveLocation")],
                [gui.Button("Export")],
                ], 
                title="Save Options",
                vertical_alignment='top',
                relief='groove',)

Layout = [
    [FilePicker],
    [gui.HorizontalSeparator()],
    [gui.Column(
        [
        [gui.Frame(layout=ImagePreview,
                   title = "Input Preview", 
                   vertical_alignment= 'top', 
                   relief='groove'), 
         gui.Column(
            [[gui.Frame(title = "GFX Mode", layout = GFXModePicker, relief = 'groove')],
            [gui.Frame(title = "Colour Mode", layout = ColourModePicker, relief = 'groove', expand_x=True)]],
            vertical_alignment='top',
            ),
         gui.Column([
            [gui.Frame(
                title = "Output Preview",
                layout = Output_Viewer,
                relief = 'groove',
                expand_x=True
            )]],
            vertical_alignment='top',
            )
        ],

        [gui.Column([
                [gui.Frame(
                    title = "Output Dimensions",
                    layout = OutputDimensions,
                    relief = 'groove',
                    vertical_alignment = 'top',
                    expand_x=True
                    ),
                    ExportButton
                ],
                [
                gui.Frame(
                    title = 'Manual Colour Picker',
                    layout = [
                        [gui.Column(ManualColours_4, vertical_alignment= 'top', key = "ManCols-4", visible=False),
                        gui.Column(ManualColours_16Lum, vertical_alignment= 'top', key = "ManCols_16Lum", visible=False),
                        gui.Column(ManualColours_16Col, vertical_alignment= 'top', key = "ManCols_16Col", visible=False)],
                    ],
                    relief = 'groove',
                    key = "ManualColourBox",
                    visible=False,
                    expand_x = False
                )
                ],
                ],
                vertical_alignment = 'top',
                )
            ],
        ])],
    ]

window = gui.Window("Atari 8-Bit Image Converter", Layout, resizable= True, icon='D:\Code\Atari\Projects\ImageConverter\Icon.ico', titlebar_icon='D:\Code\Atari\Projects\ImageConverter\Icon.ico')

FilePath = None
Mode = 0
Width = 0
Res = 0
BrightAdjust = 0
Hues = Temp_Hues = ['#808080']*16
Vals = Temp_Vals = ['#808080']*16

frametimes = [0]

while True:

    event, values = window.read()

    if (event == gui.WIN_CLOSED):   #Check for window closed
        break

    HueAdjust = values["InHue"]
    SatAdjust = values["InSat"]
    BrightAdjust = values["InBright"]

    OutWidth = values["OutViewWidth"]
    OutHeight = values["OutViewHeight"]
    ExportPath = values["SaveLocation"]
    ExportImg = None

    if (event == "-PICK_IMG-"):     #Check for file picked
        FilePath = values["-PICK_IMG-"]
    
    if event == "Reset_Hue":
        window["InHue"].update(value=0)
        HueAdjust = 0
    if event == "Reset_Sat":
        window["InSat"].update(value=0)
        SatAdjust = 0
    if event == "Reset_Bright":
        window["InBright"].update(value=0)
        BrightAdjust = 0

    if values["-AutoCol-"] == False:
        if values["160x96"]==True:
            Mode = 0
            window["ManCols_16Lum"].update(visible = False)
            window["ManCols_16Col"].update(visible = False)
            window["ManCols-4"].update(visible = True)
            window["ManualColourBox"].update(visible = True)
        
        elif values["80x192_L"] == True:
            Mode = 2
            window["ManCols-4"].update(visible = False)
            window["ManCols_16Col"].update(visible = False)
            window["ManCols_16Lum"].update(visible = True)
            window["ManualColourBox"].update(visible = True)

        elif values["80x192_C"] == True:
            Mode = 4
            window["ManCols_16Lum"].update(visible = False)
            window["ManCols-4"].update(visible = False)
            window["ManCols_16Col"].update(visible = True)
            window["ManualColourBox"].update(visible = True)
    else:
        
        window["ManCols_16Lum"].update(visible = False)
        window["ManCols_16Col"].update(visible = False)
        window["ManCols-4"].update(visible = False)
        window["ManualColourBox"].update(visible = False)
        
        if values["160x96"]==True:
            Mode = 0
        elif values["80x192_L"] == True:
            Mode = 2
        elif values["80x192_C"] == True:
            Mode = 4

    if Mode == 0 or Mode == 1:  #Size Errors

        window['Err_W_80'].update(visible = False)
        window['Err_H_192'].update(visible = False)
        window['Err_WH_80_192'].update(visible = False)
        
        if int(values['OutViewWidth'])<=160 and int(values['OutViewHeight'])<=96:
            window['Err_W_160'].update(visible = False)
            window['Err_H_96'].update(visible = False)
            window['Err_WH_160_96'].update(visible = False)

        elif int(values['OutViewWidth'])>160 and int(values['OutViewHeight'])<=96:
            window['Err_W_160'].update(visible = True)
            window['Err_H_96'].update(visible = False)
            window['Err_WH_160_96'].update(visible = False)
        
        elif int(values['OutViewWidth'])<=160 and int(values['OutViewHeight'])>96:
            window['Err_W_160'].update(visible = False)
            window['Err_H_96'].update(visible = True)
            window['Err_WH_160_96'].update(visible = False)
            
        else:
            window['Err_W_160'].update(visible = False)
            window['Err_H_96'].update(visible = False)
            window['Err_WH_160_96'].update(visible = True)

    if Mode == 2 or Mode == 3 or Mode == 4 or Mode == 5:  #Size Errors

        window['Err_W_160'].update(visible = False)
        window['Err_H_96'].update(visible = False)
        window['Err_WH_160_96'].update(visible = False)

        if int(values['OutViewWidth'])<=80 and int(values['OutViewHeight'])<=192:
            window['Err_W_80'].update(visible = False)
            window['Err_H_192'].update(visible = False)
            window['Err_WH_80_192'].update(visible = False)

        elif int(values['OutViewWidth'])>80 and int(values['OutViewHeight'])<=192:
            window['Err_W_80'].update(visible = True)
            window['Err_H_192'].update(visible = False)
            window['Err_WH_80_192'].update(visible = False)

        elif int(values['OutViewWidth'])<=80 and int(values['OutViewHeight'])>192:
            window['Err_W_80'].update(visible = False)
            window['Err_H_192'].update(visible = True)
            window['Err_WH_80_192'].update(visible = False)
            
        else:
            window['Err_W_80'].update(visible = False)
            window['Err_H_192'].update(visible = False)
            window['Err_WH_80_192'].update(visible = True)

    if values['Wide'] == True:
        Width = 2
    elif values['Normal'] == True:
        Width = 1
    elif values['Narrow'] == True:
        Width = 0

    if values['FullRes'] == True:
        Res = 0
    else:
        Res = 1

    if (values["160x96"] == True):


        if (event == "4_C0"): #Check for manual colour picker button pressed
            Hex, Col, Lum = ColPick_Window()
            
            if (Col != None and Lum != None):
                window["4_C0"].update(button_color= Hex)

        if (event == "4_C1"):
            Hex, Col, Lum = ColPick_Window()
            if (Col != None and Lum != None):
                window["4_C1"].update(button_color= Hex)

        if (event == "4_C2"):
            Hex, Col, Lum = ColPick_Window()
            if (Col != None and Lum != None):
                window["4_C2"].update(button_color= Hex)

        if (event == "4_C3"):
            Hex, Col, Lum = ColPick_Window()
            if (Col != None and Lum != None):
                window["4_C3"].update(button_color= Hex)

    elif (values["80x192_L"] == True):

        if (event == "L_Hue"):
            
            Temp_Hues = Hues
            TempVals = Vals
            
            Hues, Vals = HueValPick_Window()

            if (Hues != None and Vals != None):
                
                window["L_C0"].update(button_color = Hues[0])
                window["L_C1"].update(button_color = Hues[1])
                window["L_C2"].update(button_color = Hues[2])
                window["L_C3"].update(button_color = Hues[3])
                window["L_C4"].update(button_color = Hues[4])
                window["L_C5"].update(button_color = Hues[5])
                window["L_C6"].update(button_color = Hues[6])
                window["L_C7"].update(button_color = Hues[7])
                window["L_C8"].update(button_color = Hues[8])
                window["L_C9"].update(button_color = Hues[9])
                window["L_CA"].update(button_color = Hues[10])
                window["L_CB"].update(button_color = Hues[11])
                window["L_CC"].update(button_color = Hues[12])
                window["L_CD"].update(button_color = Hues[13])
                window["L_CE"].update(button_color = Hues[14])
                window["L_CF"].update(button_color = Hues[15])

            else:
                Hues = Temp_Hues
                Vals = TempVals

    elif (values["80x192_C"] == True):

        if (event == "C_Val"):

            Temp_Hues = Hues
            TempVals = Vals
            Hues, Vals = HueValPick_Window()

            if (Hues != None and Vals != None):
            
                window["C_C0"].update(button_color = Vals[0])
                window["C_C1"].update(button_color = Vals[1])
                window["C_C2"].update(button_color = Vals[2])
                window["C_C3"].update(button_color = Vals[3])
                window["C_C4"].update(button_color = Vals[4])
                window["C_C5"].update(button_color = Vals[5])
                window["C_C6"].update(button_color = Vals[6])
                window["C_C7"].update(button_color = Vals[7])
                window["C_C8"].update(button_color = Vals[8])
                window["C_C9"].update(button_color = Vals[9])
                window["C_CA"].update(button_color = Vals[10])
                window["C_CB"].update(button_color = Vals[11])
                window["C_CC"].update(button_color = Vals[12])
                window["C_CD"].update(button_color = Vals[13])
                window["C_CE"].update(button_color = Vals[14])
                window["C_CF"].update(button_color = Vals[15])

            else:
                Hues = Temp_Hues
                Vals = TempVals

    if event == "About":

        gui.popup("Atari 8-Bit Image Converter V0.5\n\n"+
                  "Code: aTan\n\n"+
                  "Special thanks to:\n"+
                  "rapidtables.com: HSV/RGB algorithms\n"+
                  "Wikipedia: HSV/RGB algorithms\n"+
                  "The folks @ Altirra: Atari colour palettes")

    if FilePath != None and event != None and event != "About":

        ExportImg = ImgProcessor(
                        FilePath, 
                        Mode, 
                        values["-ManualCol-"],
                        int(OutWidth),
                        int(OutHeight),
                        Width,
                        Res,
                        HueAdjust,
                        SatAdjust,
                        BrightAdjust,
                        window["4_C0"].ButtonColor[1], 
                        window["4_C1"].ButtonColor[1], 
                        window["4_C2"].ButtonColor[1], 
                        window["4_C3"].ButtonColor[1],
                        *Hues,
                        *Vals
                        )


    if event == "Export" and ExportPath != None and ExportImg != None:
        
        Export(ExportImg, 
                ExportPath,
                values["Img?"],
                values["asm?"],
                values["DList?"])

    window.refresh()


window.close()
