import cv2
import math
import itertools
import numpy as np

from utils.Cornors import Cornors

class DecodeImageAruco:
    def __init__(self, ImagePath : str):
        # Converting each Image to greyscale just to ensure contrast
        self.__img = cv2.imread(ImagePath, cv2.IMREAD_GRAYSCALE)
        aruco = cv2.QRCodeDetectorAruco()

        self._DecodedQR, self._Points = aruco.detect(self.__img, cv2.IMREAD_GRAYSCALE)

        if self._DecodedQR == False:
            return Exception

        self._Points = self._Points.reshape(-1,2)
        
        self.__top_left = tuple(map(int,self._Points[0]))
        self.__top_right = tuple(map(int,self._Points[1]))
        self.__bottom_right = tuple(map(int,self._Points[2]))
        self.__bottom_left = tuple(map(int,self._Points[3]))

        return None
    
    def getValues(self) -> list: # type: ignore Image,tuple,tuple,tuple,tuple,tuple
        return [self.__img,
                self.__img.size,
                self.__top_left,
                self.__top_right,
                self.__bottom_left,
                self.__bottom_right]
    
class VerifyQR:

    global tolerance 
    tolerance = 10

    @staticmethod
    def getQRMatrix(QRVersion : int) -> list[list]:
        QRModuleLength = 4 * QRVersion + 17
        QRMatrix = [[0 for x in range(QRModuleLength)] 
                    for y in range(QRModuleLength)]
        LenofQRMatrix = len(QRMatrix)

        # Iterator Function to Mask the Tracking Pattern
        def MaskLoopTP(y: tuple, QRMatrix: list, LenofQRMatrix: int) -> None:
            # Condition to check if list value is 6,6
            # This condition only applies to the TOP LEFT Tracking Pattern
            if y[0] == y[1]:
                for i in range(0, 8):  # Value hardcoded because size of each Tracking Pattern is 7 by 7 and a additional white border around tracking pattern is skipped
                    for j in range(0, 8):  # Range goes till 8 because range goes till the value-1
                        QRMatrix[i][j] = -1

            # Condition to check if list value is MAX,6
            # This condition only applies to the TOP RIGHT Tracking Pattern
            elif y[0] > y[1]:
                MaxValue = y[0]
                for i in range(MaxValue-1, LenofQRMatrix):
                    for j in range(0, 8):
                        QRMatrix[i][j] = -1

            # Condition to check if list value is 6,MAX
            # This condition only applies to the BOTTOM LEFT Tracking Pattern
            elif y[1] > y[0]:
                MaxValue = y[1]
                for i in range(0, 8):
                    for j in range(MaxValue-1, LenofQRMatrix):
                        QRMatrix[i][j] = -1
        
        # Iterator Function to Mask the Alignment Pattern
        def MaskLoopAP(y: tuple, QRMatrix: list) -> None:
            for i in range(y[0] - 2, y[0] + 3):  # We need to subtract it by 2 to correct the pos of given coords and add 3 for the same
                for j in range(y[1] - 2, y[1] + 3):  # We need to subtract it by 2 to correct the pos of given coords and add 3 for the same
                    QRMatrix[i][j] = -1

        VersionAPLocationDic = {
            2: [6, 18],
            3: [6, 22],
            4: [6, 26],
            5: [6, 30],
            6: [6, 34],
            7: [6, 22, 38],
            8: [6, 24, 42],
            9: [6, 26, 46],
            10: [6, 28, 50],
            11: [6, 30, 54],
            12: [6, 32, 58],
            13: [6, 34, 62],
            14: [6, 26, 46, 66],
            15: [6, 26, 48, 70],
            16: [6, 26, 50, 74],
            17: [6, 30, 54, 78],
            18: [6, 30, 56, 82],
            19: [6, 30, 58, 86],
            20: [6, 34, 62, 90],
            21: [6, 28, 50, 72, 94],
            22: [6, 26, 50, 74, 98],
            23: [6, 30, 54, 78, 102],
            24: [6, 28, 54, 80, 106],
            25: [6, 32, 58, 84, 110],
            26: [6, 30, 58, 86, 114],
            27: [6, 34, 62, 90, 118],
            28: [6, 26, 50, 74, 98, 122],
            29: [6, 30, 54, 78, 102, 126],
            30: [6, 26, 52, 78, 104, 130],
            31: [6, 30, 56, 82, 108, 134],
            32: [6, 34, 60, 86, 112, 138],
            33: [6, 30, 58, 86, 114, 142],
            34: [6, 34, 62, 90, 118, 146],
            35: [6, 30, 54, 78, 102, 126, 150],
            36: [6, 24, 50, 76, 102, 128, 154],
            37: [6, 28, 54, 80, 106, 132, 158],
            38: [6, 32, 58, 84, 110, 136, 162],
            39: [6, 26, 54, 82, 110, 138, 166],
            40: [6, 30, 58, 86, 114, 142, 170],
        }
        
        if QRVersion == 1:
            TPList = [(6, 6), (6, 14), (14, 6)]
            for x in TPList:
                MaskLoopTP(x, QRMatrix, LenofQRMatrix)
            return QRMatrix
        
        # List of Locations of Module - Gotten from the Huge Dictionary
        MaskCoords = VersionAPLocationDic[QRVersion]

        # List of cartesian product derived from APList
        CartProductList = list(itertools.product(MaskCoords, repeat=2))
        
        ### START CODE FOR MASKING TRACKING PATTERN ###

        # To find the Max Value in Alignment Pattern list which we use to figure out the Tracking Pattern Position
        MaxMaskPatternVal = max(MaskCoords)
        TPList = [(6, 6), (6, MaxMaskPatternVal), (MaxMaskPatternVal, 6)]


        # A for loop to send each value of list to the Mask iterator
        for x in TPList:
            MaskLoopTP(x, QRMatrix, LenofQRMatrix)

        ### END CODE FOR MASKING TRACKING PATTERN ###
        
        ### START CODE FOR MASKING ALIGNMENT PATTERN ###

        # Eliminated Co-ordinates List after Masking out Large Tracking Pattern
        # It leaves us with list of Alignment Pattern
        APList = [item for item in CartProductList if item not in TPList]

        for x in APList:
            MaskLoopAP(x, QRMatrix)
        ### END CODE FOR MASKING ALIGNMENT PATTERN ###

        return QRMatrix
    
    @staticmethod
    def isVersionCorrect(Possible_Module_Size_Dict : dict, Coord_topleft : tuple, img) -> list | bool:
        """Returns the valid QR Version and Version Module Length depending on the Dictionary entered
        
        Possible_Module_Size_Dict : dict { QR Version : Module Length }
        
        Key => ITP = Internal Tracking Pattern"""
        
        for QRVersion, ModuleLength in Possible_Module_Size_Dict.items():
            top_left_Coord_ITP = (Coord_topleft[0] + (2*ModuleLength), Coord_topleft[1] + (2*ModuleLength))
            bottom_right_Coord_ITP = (Coord_topleft[0] + (5*ModuleLength) - 1, Coord_topleft[1] + (5*ModuleLength) - 1)

            roi = img[int(top_left_Coord_ITP[1]):int(bottom_right_Coord_ITP[1]), int(top_left_Coord_ITP[0]):int(bottom_right_Coord_ITP[0])]

            if np.all(np.isclose(roi, 0, atol=tolerance)):
                return [int(QRVersion) , int(ModuleLength)]
        return False

    @staticmethod
    def getPixelColour(ImageObject, Point : tuple) -> int:
        return int(ImageObject[Point[1],Point[0]])

    @staticmethod
    def isPointOnQRCode(ImageObject, Point : tuple, Cornor : Cornors) -> bool:
        # Check Valid Cornor Input
        if Cornor not in [Cornors.TopLeft,Cornors.TopRight,Cornors.BottomLeft,Cornors.BottomRight]:
            return False
        
        # Check if Point lies on a Black Value
        if VerifyQR.getPixelColour(ImageObject, Point) > tolerance:
            return False
        
        x, y = Point
        if Cornor == Cornors.TopLeft:
            neighbors = [(x-1, y-1), (x-1, y), (x, y-1)]
            neighbor_colors = [VerifyQR.getPixelColour(ImageObject,neighbor) for neighbor in neighbors]
            return all(n > 250 - tolerance for n in neighbor_colors)
        elif Cornor == Cornors.TopRight:
            neighbors = [(x+1, y-1), (x+1, y), (x, y-1)]
            neighbor_colors = [VerifyQR.getPixelColour(ImageObject,neighbor) for neighbor in neighbors]
            return all(n > 250 - tolerance for n in neighbor_colors)
        elif Cornor == Cornors.BottomLeft:
            neighbors = [(x-1, y+1), (x-1, y), (x, y+1)]
            neighbor_colors = [VerifyQR.getPixelColour(ImageObject,neighbor) for neighbor in neighbors]
            return all(n > 250 - tolerance for n in neighbor_colors)
        elif Cornor == Cornors.BottomRight:
            neighbors = [(x+1, y+1), (x+1, y), (x, y+1)]
            neighbor_colors = [VerifyQR.getPixelColour(ImageObject,neighbor) for neighbor in neighbors]
            return all(n > 250 - tolerance for n in neighbor_colors)

    @staticmethod
    def returnSameEdgeLength(Coord_topleft : tuple, Coord_topright : tuple, Coord_bottomleft : tuple, Coord_bottomright :tuple) -> float:
        def calculate_distance(coord1, coord2):
            """Calculate the Euclidean distance between two points."""
            return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

        # Calculate the lengths of the edges
        top_edge_length = calculate_distance(Coord_topleft, Coord_topright)
        bottom_edge_length = calculate_distance(Coord_bottomleft, Coord_bottomright)
        left_edge_length = calculate_distance(Coord_topleft, Coord_bottomleft)
        right_edge_length = calculate_distance(Coord_topright, Coord_bottomright)
        # Verify if any two edges have the same length
        if math.isclose(top_edge_length, bottom_edge_length):
            return(top_edge_length)
        elif math.isclose(top_edge_length, left_edge_length):
            return(top_edge_length)
        elif math.isclose(top_edge_length, right_edge_length):
            return(top_edge_length)
        elif math.isclose(bottom_edge_length, left_edge_length):
            return(bottom_edge_length)
        elif math.isclose(bottom_edge_length, right_edge_length):
            return(bottom_edge_length)
        elif math.isclose(left_edge_length, right_edge_length):
            return(left_edge_length)
        else:
            return -1
        
class getSecretDataQR:
    @staticmethod
    def getPixelColour(ImageObject, Point : tuple) -> int:
        return ImageObject[Point[1],Point[0]]
