from PIL import Image
import math

def makeimage(QRMatrix : list, LenofQRMatrix : int, Blocksize  : int = 100, imgIteration : int = 0):
    # Adjustment Ratio = 20% of Blocksize
    adjustmentRatio = math.ceil(0.2*Blocksize) #TODO change later
    colour_black = (0,0,0)
    #colour_white = (255, 255, 255) #TODO

    img = Image.new('RGB', (LenofQRMatrix*Blocksize, LenofQRMatrix*Blocksize), color='white')
    pixels = img.load()

    # To render module of square dimension
    def setblock(block_y : int,block_x : int,Blocksize : int,colour : tuple): # Sets a block of pixels specified by the Blocksize variable
        for y in range(block_y*Blocksize,block_y*Blocksize+Blocksize):
            for x in range(block_x*Blocksize,block_x*Blocksize+Blocksize):
                pixels[x, y] = colour

    # To render slightly bigger module
    def setblockrect(block_y : int,block_x : int,blocksizeY : int, blocksizeX : int,colour : tuple):
        for y in range(block_y*Blocksize,(block_y*Blocksize)+blocksizeY):
            for x in range(block_x*Blocksize,(block_x*Blocksize)+blocksizeX):
                pixels[x, y] = colour

    # Time Complexity n^4
    for y in range(0,LenofQRMatrix):
        for x in range(0,LenofQRMatrix):
            if QRMatrix[y][x][1] == 1: # If pixel is viable for data embed
                if QRMatrix[y][x][0] == 1:  # Black pixel
                    setblockrect(y,x,Blocksize,Blocksize+adjustmentRatio,colour_black)
            elif QRMatrix[y][x][0] == 1:
                setblock(y,x,Blocksize,colour_black)

    # Output format -> output0.png
    img.save(f'output{imgIteration}.png')

def main(QRMatrix : list, LenofMatrix : int, VBACoordLst : list, imgIteration : int=0, Blocksize : int = 100, BitData : str="010100110111010001101001011101000110001101101000") -> None:
    # QRMatrix -> List -> 2D Array
    # LenofMatrix -> int -> Length of QR Matrix
    # VBACoord ->  List ->  List of Co ordinates -> Structure - [(y,x),....]
    # imgIteration -> int -> Labels the output image with a given number
    # Blocksize -> int -> Defines the pixel size of each module of a qr code
    # BitData -> str -> Bit Data that has to be embed in the base qr code

    # Using the Co-ordinates derived from method DeriveBlockAdjustmentCoord we mark each cell for block widening
    for bit,CoordPair in zip(BitData,VBACoordLst):
        if bit == "1":
            QRMatrix[CoordPair[0]][CoordPair[1]][1] = 1

    makeimage(QRMatrix,LenofMatrix,Blocksize,imgIteration)
    