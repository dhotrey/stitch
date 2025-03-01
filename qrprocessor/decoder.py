import pandas as pd
import argparse


from utils.Cornors import Cornors
from utils.DecodeQR import DecodeImageAruco
from utils.DecodeQR import VerifyQR
from utils.DecodeQR import getSecretDataQR as SD


def main(ImagePath:str, tolerance=10):

    DI = DecodeImageAruco(ImagePath)
    
    img, imgSize, Coord_topleft, Coord_topright, Coord_bottomleft, Coord_bottomright = DI.getValues()

    # Verify QR Code Coordinates
    if VerifyQR.isPointOnQRCode(img, Coord_topleft, Cornors.TopLeft) == False:
        raise # TODO: Add custom Exceptions
    if VerifyQR.isPointOnQRCode(img, Coord_topright, Cornors.TopRight) == False:
        raise
    if VerifyQR.isPointOnQRCode(img, Coord_bottomleft, Cornors.BottomLeft) == False:
        raise
    if VerifyQR.isPointOnQRCode(img, Coord_bottomright, Cornors.BottomRight) == False:
        raise
    

    # We have to add 1 here cause of the length of coordinates is lower by 1 due to coordinates starting from 0
    Length_QR = 1 + int(VerifyQR.returnSameEdgeLength(Coord_topleft, Coord_topright, Coord_bottomleft, Coord_bottomright))

    # Possible_Module_Size_LST = [y for y in [Length_QR/(4 * x + 17) for x in range(1,41)] if isinstance(y, float) and y == int(y)]
    Possible_Module_Size_Dict = {
        x: module_length
        for x in range(1, 41)
        # WALRUS OPERATOR says - "Urr-urr-urr! Urr-urr-urr!"
        if (module_length := Length_QR / (4 * x + 17)) == int(module_length)
    }

    temp = VerifyQR.isVersionCorrect(Possible_Module_Size_Dict, Coord_topleft, img)
    if temp == False:
        return False
    QRVersion = temp[0]
    BlockSize = temp[1]
    QRMatrix = VerifyQR.getQRMatrix(QRVersion)
    print(pd.DataFrame(QRMatrix))
    print("Top Left Coord -",Coord_topleft)
    print("Top Right Coord -",Coord_topright)
    print("Bottom Left Coord -",Coord_bottomleft)
    print("Bottom Right Coord -",Coord_bottomright)
    print("QR Version - ",QRVersion)
    SecretData = ""
    temp = []
    Center_of_Block = (int(BlockSize/2),int(BlockSize/2))
    for x in range(len(QRMatrix)-1): # We subtract by 1 here cause we dont want to check the last block column
        for y in range(len(QRMatrix)):
            if QRMatrix[x][y] != -1:
                BlockCoord = (Coord_topleft[0] + (BlockSize * x),Coord_topleft[1] + (BlockSize * y))
                # Checking if Current Block is Black
                if SD.getPixelColour(img,(BlockCoord[0]+Center_of_Block[0],
                                          BlockCoord[1]+Center_of_Block[1])) <= 0+tolerance:
                    # Checking if Adjacent Block to the right is White
                    if SD.getPixelColour(img,(BlockCoord[0]+BlockSize+Center_of_Block[0],
                                            BlockCoord[1]+Center_of_Block[1])) >= 255-tolerance:
                        # If Both the above conditions are satisfied
                        # We can extract the Secret Data by finding the Pixel Value
                        # of the adjacent block's top left coord
                        temp.append(BlockCoord)
                        Adjacent_topLeft_Colour = SD.getPixelColour(img,(BlockCoord[0]+BlockSize,BlockCoord[1]))
                        if Adjacent_topLeft_Colour <= 0+tolerance:
                            SecretData += "1"
                        if Adjacent_topLeft_Colour >= 255-tolerance:
                            SecretData += "0"
    print("\nSecret Data Found at Co-ordinates",temp)
    print("\nDecode Binary Data\n",SecretData)
                              
                        
# TESTING PURPOSES
if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Main QR Decoder Script")

    # Add the --BaseQRData option. This argument will pass the input data and generate QR Base QR Code
    # If no --BaseQRData is mentioned then default value will be used
    parser.add_argument(
        "--InputImgFile",
        type=str,
        default="output.png",
        help="Input File Location for decoding",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Run the main function
    main(args.InputImgFile)