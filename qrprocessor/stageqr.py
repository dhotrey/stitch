# This code generates BaseQRCode, and all the parameters required, for generating the SecretQRCode
# BaseQRData -> String -> Input from the user for the base qr code
# QRMatrix -> Main 2D Numpy Array
# LenofQRMatrix -> int -> Length of QR Matrix along the X-Axis & Y-Axis
# QRVersion -> int -> Derived after generating the base QR Code
# This code also masks out the Alignment Pattern and Tracking Pattern. Make sure the masking is performed
# before passing onwards

'''
Coordinate based system
      x
  _________>  
  |
  |
 y|
  |
  V
'''

import logging
import argparse
import qrcode
import itertools

# Code to visualize the QR Code in Nested List format
def printtesting(QRMatrix : list) -> None:
  if logger.isEnabledFor(logging.INFO):
    # Only evaluate printtesting if logging is enabled
    df = pd.DataFrame(QRMatrix)
    logger.info(f"Base QR Code Visualized\n{df}")


# Logging Setup
def setup_logging(level):
  # Setup logging to print to the console
  logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')
  logger.setLevel(level)  

# Alter Module's State of Given Co-ordinate to a given value 
def AlterModuleState( xCoordinate : int, yCoordinate : int, value : int, QRMatrix : list) -> None:
  # print("Printing x,y,val",xCoordinate,yCoordinate,value)
  QRMatrix[yCoordinate][xCoordinate][1] = value


# Iterator Function to Mask the Tracking Pattern
def MaskLoopTP( y : tuple, QRMatrix : list, LenofQRMatrix : int) -> None:

  # Condition to check if list value is 6,6
  # This condition only applies to the TOP LEFT Tracking Pattern
  if y[0] == y[1]:
    for i in range(0,7): # 7 Value hardcoded because size of each Tracking Pattern is 7 by 7
      for j in range(0,7): # Range goes till 7 because range goes till the value-1
        AlterModuleState(i,j,-1,QRMatrix)

  # Condition to check if list value is MAX,6
  # This condition only applies to the TOP RIGHT Tracking Pattern
  elif y[0] > y[1]:
    MaxValue = y[0]
    for i in range(MaxValue,LenofQRMatrix):
      for j in range(0,7):
        AlterModuleState(i,j,-1,QRMatrix)

  # Condition to check if list value is 6,MAX
  # This condition only applies to the BOTTOM LEFT Tracking Pattern
  elif y[1] > y[0]:
    MaxValue = y[1]
    for i in range(0,7):
      for j in range(MaxValue,LenofQRMatrix):
        AlterModuleState(i,j,-1,QRMatrix)


# Iterator Function to Mask the Alignment Pattern
def MaskLoopAP( y : tuple, QRMatrix : list) -> None:

  for i in range(y[0]-2,y[0]+3): # We need to subtract it by 2 to correct the pos of given coords and add 3 for the same
    for j in range(y[1]-2,y[1]+3): # We need to subtract it by 2 to correct the pos of given coords and add 3 for the same
      AlterModuleState(i,j,-1,QRMatrix)

# Tracking Pattern and Alignment Patterns that are generated on bigger versions of qr code from Version 2 and Up
def MaskingMainFunction( QRMatrix : list, QRVersion : int, LenofQRMatrix : int) -> None:
  
  if QRVersion < 1 or QRVersion > 40:
    if args.log:
      logger.warning(f"QR Version {QRVersion} not within range")
    return 
  if QRVersion == 1:
    if args.log:
      logger.info(f"QR Version {QRVersion}, masking Tracking Pattern only")
    TPList = [(6,6),(6,14),(14,6)]
    for x in TPList:
      MaskLoopTP(x, QRMatrix, LenofQRMatrix)
    if args.log:
      printtesting(QRMatrix)
    return

  #Dictionary of QR Version with corresponding TP and AP 
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

  # List of Locations of Module - Gotten from the Huge Dictionary
  MaskCoords = VersionAPLocationDic[QRVersion]

  # List of cartesian product derived from APList
  CartProductList = list(itertools.product(MaskCoords,repeat=2))

  ### START CODE FOR MASKING TRACKING PATTERN ###

  
  # To find the Max Value in Alignment Pattern list which we use to figure out the Tracking Pattern Position
  MaxMaskPatternVal = max(MaskCoords)
  TPList = [(6,6),(6,MaxMaskPatternVal),(MaxMaskPatternVal,6)]

  if args.log:
    logger.info(f"Co-ordinate of Tracking/Alignment Pattern {TPList}")
    logger.info(f"QR Version {QRVersion}, Masking Tracking Pattern")
  # A for loop to send each value of list to the Mask iterator  
  for x in TPList:
    MaskLoopTP(x, QRMatrix, LenofQRMatrix)

  ### END CODE FOR MASKING TRACKING PATTERN ###


  ### START CODE FOR MASKING ALIGNMENT PATTERN ###

  if args.log:
    logger.info(f"QR Version {QRVersion}, Masking Alignment Pattern")
  # Eliminated Co-ordinates List after Masking out Large Tracking Pattern
  # It leaves us with list of Alignment Pattern
  APList = [item for item in CartProductList if item not in TPList]

  for x in APList:
    MaskLoopAP(x, QRMatrix)
  ### END CODE FOR MASKING ALIGNMENT PATTERN ###

  if args.log:
    printtesting(QRMatrix)

# Func to define QR MATRIX 2D array
def DefineQRMatrix( BaseQRData : str = "BaseQRCode") -> int | list:
  if args.log:
    timerstart = time.time()
  
  qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    border=0
  )

  qr.add_data(BaseQRData)
  QRVersion = qr.version

  if args.log:
    logger.info(f"Generating Base QR from \"{BaseQRData}\" Data")
    logger.info(f"Base QR Version -> {QRVersion}")

  qr.make(fit=True)

  # This var converts the cover qr code to a list matrix using in built function and then reassigns
  # value of TRUE and FALSE to  1 and 0 respectively 
  QRMatrix = [[[1,0] if x == True else [0,0] for x in sublist] for sublist in qr.get_matrix()]
  
  if args.log:
    timerend = time.time()
    logger.warning(f"Generated Base QR Code in {timerend-timerstart} second")
    printtesting(QRMatrix)

  return QRVersion,QRMatrix

# Func to define basic variables
def DefineVariables( QRMatrix : list) -> int | int:
  # GLOBAL QR MATRIX - OPERATIONS OF EDIT AND READ TO BE DONE FROM THIS 2D Array 
  # Calulating Length of X and Y Axis Once
  LenofQRMatrix = len(QRMatrix)
  
  if args.log:
    logger.info(f"Length of X & Y axis {LenofQRMatrix}")  
  
  return LenofQRMatrix

# Func to derive location of viable spots to embed bits
def DeriveBlockAdjustmentCoord( QRMatrix : list , LenofQRMatrix : int) -> list:
  if args.log:
    logger.info("Deriving Possible Co-ordinates ")

  ViableBlockAlternationCoordLst = []
  for xCoordinate in range(LenofQRMatrix-1):
    for yCoordinate in range(LenofQRMatrix):
      if (QRMatrix[yCoordinate][xCoordinate][1] != -1) and (QRMatrix[yCoordinate][xCoordinate][0] > QRMatrix[yCoordinate][xCoordinate+1][0]):
        ViableBlockAlternationCoordLst.append((yCoordinate,xCoordinate))
  
  if args.log:
    logger.info("Successfully Generated Viable Co-ordinates for Bit Embedding")
    print("Co-ordinate Formatting - (y,x)\n",ViableBlockAlternationCoordLst)
  return ViableBlockAlternationCoordLst

# Returns Colour of Module Pair
def RowMPColour( xCoordinate : int, yCoordinate : int, QRMatrix : list) -> list:
  return([QRMatrix[yCoordinate][xCoordinate][0],QRMatrix[yCoordinate][xCoordinate+1][0]])


# Alter Module's State of Given Co-ordinate to a given value 
def AlterModuleColour( xCoordinate : int, yCoordinate : int, value : int, QRMatrix : list) -> None:
  if args.log:
    logger.info(f"Changing Colour of {xCoordinate},{yCoordinate} to {value}")
  QRMatrix[yCoordinate][xCoordinate][0] = value


# MAIN FUNCTION
def main( BaseQRData : str = "BaseQRCode"):
  if args.log:
    logger.info("Started Main Function")
  # Make Base QR Code and assign to a variable
  QRVersion,QRMatrix = DefineQRMatrix(BaseQRData) # Got data from Arg. If no data available then it defaults to BaseQRCode
  
  # Define Misc Vars
  LenofQRMatrix = DefineVariables(QRMatrix)

  # Function to mask TP and AP
  MaskingMainFunction(QRMatrix,QRVersion,LenofQRMatrix)

  ViableBlockAltCoordLst = DeriveBlockAdjustmentCoord(QRMatrix, LenofQRMatrix)

  
  
if __name__ == '__main__':
  # Create an argument parser
  parser = argparse.ArgumentParser(description="Main QR Code Script")
  
  # Add the --log flag to enable logging
  parser.add_argument('--log', action='store_true', help="Enable logging to console")
  
  # Add a --log-level option to specify the logging level
  parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', help="Set the logging level (default: INFO)")

  # Add the --BaseQRData option. This argument will pass the input data and generate QR Base QR Code
  # If no --BaseQRData is mentioned then default value will be used
  parser.add_argument('--BaseQRData', type=str, default='BaseQRCode', help="Input data for generating the base QR Code")
  
  # Parse the command-line arguments
  args = parser.parse_args()

  # If --log is passed, enable logging
  if args.log:
    # Configure the logger (by default, it won't log anything)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.CRITICAL) 
    log_level = getattr(logging, args.log_level)
    setup_logging(log_level)  
    logger.info("Logging Enabled")
    import pandas as pd
    import time

  # Run the main function
  main(args.BaseQRData)