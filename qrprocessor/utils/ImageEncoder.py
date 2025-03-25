from PIL import Image
import numpy as np
import math

def add_quiet_zone(image, 
                   module_size) -> Image:
    # Calculate quiet zone size
    quiet_zone = 4 * module_size  # Quiet zone is 4 times the module size
    
    # Calculate new image size
    original_width, original_height = image.size
    new_width = original_width + 2 * quiet_zone
    new_height = original_height + 2 * quiet_zone
    
    # Create a new image with a white background
    new_image = Image.new("RGB", (new_width, new_height), "white")
    
    # Paste the original image in the center of the new image
    new_image.paste(image, (quiet_zone, quiet_zone))
    
    return new_image

def makeimage(QRMatrix : list, 
              LenofQRMatrix : int,
              UniqueFolder : str, 
              Blocksize  : int = 100, 
              imgIteration : int = 0) -> None:
    
    # Adjustment Ratio = 20% of Blocksize
    adjustmentRatio = math.ceil(0.2*Blocksize) #TODO change later
    colour_black = (0,0,0)
    colour_offwhite = (240,240,240)
    #colour_white = (255, 255, 255) #TODO
    
    # Create a blank white image as a NumPy array
    img_size = LenofQRMatrix * Blocksize
    img_array = np.full((img_size, img_size, 3), 255, dtype=np.uint8)  # White background

    # Precompute the color for black pixels
    black_colour = np.array(colour_black, dtype=np.uint8)
    endembed_colour = np.array(colour_offwhite, dtype=np.uint8)

    for y in range(LenofQRMatrix):
        for x in range(LenofQRMatrix):
            # Calculate the starting and ending coordinates for the block
            start_y = y * Blocksize
            end_y = start_y + Blocksize
            start_x = x * Blocksize
            end_x = start_x + Blocksize

            if QRMatrix[y][x][1] == 1:  # If pixel is viable for data embed
                if QRMatrix[y][x][0] == 1:  # Black pixel
                    # Adjust the block size for data embedding
                    end_x += adjustmentRatio
                    img_array[start_y:end_y, start_x:end_x] = black_colour
                else:
                    # Render a normal block
                    img_array[start_y:end_y, start_x:end_x] = black_colour
            elif QRMatrix[y][x][1] == 2: #If pixel is marked as end of embed
                img_array[start_y:end_y, start_x:end_x] = endembed_colour
            elif QRMatrix[y][x][0] == 1:
                # Render a normal block
                img_array[start_y:end_y, start_x:end_x] = black_colour

    # Convert the NumPy array to a PIL image
    img = Image.fromarray(img_array, 'RGB')
    
    img = add_quiet_zone(img,Blocksize)
    
    # Output format -> output0.png
    img.save(f'Output/{UniqueFolder}/{imgIteration}.png')

def main(QRMatrix : list,
         LenofMatrix : int,
         VBACoordLst : list,
         UniqueFolder : str,
         imgIteration : int=0,
         Blocksize : int = 100, 
         BitData : str="010100110111010001101001011101000110001101101000") -> None:
    
    # QRMatrix -> List -> 2D Array
    # LenofMatrix -> int -> Length of QR Matrix
    # VBACoord ->  List ->  List of Co ordinates -> Structure - [(y,x),....]
    # imgIteration -> int -> Labels the output image with a given number
    # Blocksize -> int -> Defines the pixel size of each module of a qr code
    # BitData -> str -> Bit Data that has to be embed in the base qr code

    # Code to ensure that it ends when the data to embed is less than the number of spaces where it
    # can embed
    for CoordPair in VBACoordLst:
        if len(BitData) != 0:
            bit = BitData[0]
            BitData = BitData[1:]
            if bit == "1":
                QRMatrix[CoordPair[0]][CoordPair[1]][1] = 1
        else:
            QRMatrix[CoordPair[0]][CoordPair[1]+1][1] = 2
            import pandas as pd
            df = pd.DataFrame(QRMatrix)
            print(f"Base QR Code Visualized\n{df}")
            break


    # # Using the Co-ordinates derived from method DeriveBlockAdjustmentCoord we mark each cell for block widening
    # for bit,CoordPair in zip(BitData,VBACoordLst):
    #     if bit == "1":
    #         QRMatrix[CoordPair[0]][CoordPair[1]][1] = 1

    makeimage(QRMatrix,LenofMatrix,UniqueFolder,Blocksize,imgIteration)
