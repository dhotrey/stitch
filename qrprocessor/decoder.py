import time
import os
import glob
import subprocess
import redis

from utils.Cornors import Cornors
from utils.DecodeQR import DecodeImageAruco
from utils.DecodeQR import VerifyQR
from utils.DecodeQR import getSecretDataQR as SD


def main(ImagePath: str, tolerance=1):

    DI = DecodeImageAruco(ImagePath)

    img, imgSize, Coord_topleft, Coord_topright, Coord_bottomleft, Coord_bottomright = (
        DI.getValues()
    )

    # Verify QR Code Coordinates # checks not necesary anymore.
    # if VerifyQR.isPointOnQRCode(img, Coord_topleft, Cornors.TopLeft) is False:
    #     pass
    # if VerifyQR.isPointOnQRCode(img, Coord_topright, Cornors.TopRight) is False:
    #     pass
    # if VerifyQR.isPointOnQRCode(img, Coord_bottomleft, Cornors.BottomLeft) is False:
    #     pass
    # if VerifyQR.isPointOnQRCode(img, Coord_bottomright, Cornors.BottomRight) is False:
    #     pass

    # We have to add 1 here cause of the length of coordinates is lower by 1 due to coordinates starting from 0
    Length_QR = 1 + int(
        VerifyQR.returnSameEdgeLength(
            Coord_topleft, Coord_topright, Coord_bottomleft, Coord_bottomright
        )
    )

    # Possible_Module_Size_LST = [y for y in [Length_QR/(4 * x + 17) for x in range(1,41)] if isinstance(y, float) and y == int(y)]
    Possible_Module_Size_Dict = {
        x: module_length
        for x in range(1, 41)
        # WALRUS OPERATOR says - "Urr-urr-urr! Urr-urr-urr!"
        if (module_length := Length_QR / (4 * x + 17)) == int(module_length)
    }

    temp = VerifyQR.isVersionCorrect(Possible_Module_Size_Dict, Coord_topleft, img)
    if temp is False:
        return False
    QRVersion = temp[0]
    BlockSize = temp[1]
    QRMatrix = VerifyQR.getQRMatrix(QRVersion)
    # print(pd.DataFrame(QRMatrix))
    # print("Top Left Coord -",Coord_topleft)
    # print("Top Right Coord -",Coord_topright)
    # print("Bottom Left Coord -",Coord_bottomleft)
    # print("Bottom Right Coord -",Coord_bottomright)
    # print("QR Version - ",QRVersion)
    SecretData = ""
    temp = []
    Center_of_Block = (int(BlockSize / 2), int(BlockSize / 2))
    for x in range(
        len(QRMatrix) - 1
    ):  # We subtract by 1 here cause we dont want to check the last block column
        for y in range(len(QRMatrix)):
            if QRMatrix[x][y] != -1:
                BlockCoord = (
                    Coord_topleft[0] + (BlockSize * x),
                    Coord_topleft[1] + (BlockSize * y),
                )
                # Checking if Current Block is Black
                if (
                    SD.getPixelColour(
                        img,
                        (
                            BlockCoord[0] + Center_of_Block[0],
                            BlockCoord[1] + Center_of_Block[1],
                        ),
                    )
                    <= 0 + tolerance
                ):
                    # Checking if Adjacent Block to the right is White
                    if (
                        SD.getPixelColour(
                            img,
                            (
                                BlockCoord[0] + BlockSize + Center_of_Block[0],
                                BlockCoord[1] + Center_of_Block[1],
                            ),
                        )
                        >= 255 - tolerance
                    ):
                        # If Both the above conditions are satisfied
                        # We can extract the Secret Data by finding the Pixel Value
                        # of the adjacent block's top left coord
                        temp.append(BlockCoord)
                        Adjacent_topLeft_Colour = SD.getPixelColour(
                            img, (BlockCoord[0] + BlockSize, BlockCoord[1])
                        )
                        if Adjacent_topLeft_Colour <= 0 + tolerance:
                            SecretData += "1"
                        if Adjacent_topLeft_Colour >= 255 - tolerance:
                            SecretData += "0"
                    # Check if Adjacent Block is Grey
                    if (
                        SD.getPixelColour(
                            img,
                            (
                                BlockCoord[0] + BlockSize + Center_of_Block[0],
                                BlockCoord[1] + Center_of_Block[1],
                            ),
                        )
                        == 240
                    ):
                        return SecretData

    return SecretData
    # print("\nSecret Data Found at Co-ordinates",temp)
    # print("\nDecode Binary Data\n",SecretData)


# TESTING PURPOSES
if __name__ == "__main__":
    # Define input folder
    input_folder = "InputFolder"
    inputfile = input("Enter path to gif : ")

    os.makedirs(input_folder, exist_ok=True)

    decodedResult = subprocess.run(
        [
            "ffmpeg",
            "-i",
            inputfile,
            "-vsync",
            "0",
            "-q:v",
            "1",
            f"{input_folder}/%d.png",
        ]
    )
    print("Decoded gif successfully")
    print("Return code", decodedResult.returncode)
    # Get all image files in the folder
    qr_images = glob.glob(os.path.join(input_folder, "*.png"))

    # Sort files numerically
    qr_images.sort(key=lambda x: int(os.path.basename(x).split(".")[0]))

    SecretDataList = []
    timerstart = time.time()
    for img_path in qr_images:
        time.sleep(0.05)
        print(f"Processing QR Code: {img_path}", end="\r")
        SecretDataList.append(main(img_path))
    timerend = time.time()
    print(f"\nTime Taken: {timerend-timerstart} sec")

    rdb = redis.Redis()

    for secret in SecretDataList:
        if secret:
            rdb.rpush("chunkdata", secret)

    print("written decoded data stream to redis successfully")
    print("constructing file from chunks")

    constructRes = subprocess.run("./constructor")
    print("Constructed original file successfully , content saved to decoded file")
    print(f"return code {constructRes.returncode}")
