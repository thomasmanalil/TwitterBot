import os.path
import sys
from Bot.config import Config
import os

conf = Config()
PARENT_FOLDER = os.path.abspath(os.path.dirname(__file__))
DATA_FILE = os.path.join(PARENT_FOLDER, os.pardir, "data/data.txt")

def getSinceId():
    sinceId = 1

    #if file exist, read from file
    if(os.path.exists(DATA_FILE)):
        try:
            dataFile = open(DATA_FILE,"r")
            if (os.path.getsize(DATA_FILE) != 0): #read from file, if file is not empty
                sinceId = int(dataFile.read())
        except Exception as e:
            Config.LOGGER.info(e)
        finally:
            dataFile.close()

    return sinceId

def setSinceId(Id):
    try:
        dataFile = open(DATA_FILE,"w+")
        dataFile.write(str(Id))
    except Exception as e:
        Config.LOGGER.info(e)
    finally:
        dataFile.close()

def resetSinceId():
    try:
        if(os.path.exists(DATA_FILE)):
            os.remove(DATA_FILE)
    except Exception as e:
        Config.LOGGER.info(e)
        raise e
