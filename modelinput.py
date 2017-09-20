"""Python class for model input """

import sys
import logging
#from modelobject import modelOBJECT
from cylinder import CYLINDER
from box import BOX
from sphere import SPHERE
from cone import CONE


class modelINPUT:

    """
    Class to handle methods for reading an model input file
    """

    # Define static variables -------------------------------

    # Dictionary of model input classes
    # 8 : non-tumbling flat plate
    # 9 is a flat plate
    # 14 is a disk
    # 10 is a spinning sphere
    itypes = {4:CYLINDER, 6:BOX, 7:BOX, 1:SPHERE, 9:BOX, 14:CYLINDER, 17:CONE, 10:SPHERE,
              11:SPHERE, 8:BOX}

    convertMtomm = 1000.
    scaleFactor = 100.

    qtyWord = "(QTY."


    def __init__(self, inFile):
        """
        Initialize the modelINPUT object
        :param inFile:
        """

        self.inFile = inFile  # point the file handle to the input file


    def skip(self,nn):
        """
        Skip past nn lines in the file
        :param nn:
        :return:
        """

        logging.debug("Skipping these lines")
        for ii in range(1, nn + 1, 1):
            logging.debug(self.inFile.readline())
        logging.debug(" ")


    def read_int(self):
        """
        Read in an integer
        """
        try:
            list = [s.strip() for s in self.inFile.readline().split()]
            logging.debug("modelinput : read_int : list = %s",list)
            # convert 1st value in list to integer
            return int(list[0])
        except:
            logging.info('modelinput : read_int : Exception thrown')
            print 'modelINPUT : read_int : Exception thrown'
            return

    # function to read a list of integers.  How many is read is specified by nn
    def read_list(self,nn):
        """
        Read a list of nn integers
        :param nn:
        :return:
        """
        try:
            temp = [s.strip() for s in self.inFile.readline().split()]

            # this will crash if try to convert a non-digit to an integer
            list = [int(s) for s in temp[0:nn]]

            # convert 1st value in list to integer
            logging.debug('modelinput : read_list : list = %s', list)
            return list
        except ValueError:
            logging.debug('modelINPUT : read_list :  ValueError Exception thrown')
            sys.exit('modelINPUT : read_list :  ValueError Exception thrown')
            return


    def read_float(self):
        """
        Read a float
        :return:
        """
        try:
            list = [s.strip() for s in self.inFile.readline().split()]
            # convert 1st value in list to integer
            return float(list[0])
        except ValueError :
            logging.debug('modelINPUT : read_float : ValueError Exception thrown, check input values')
            sys.exit('modelINPUT : read_float : ValueError Exception thrown, check input values')
            return

    # function to read the material numbers.
    def read_material(self):
        """
        Read in the model material values
        :return:
        """

        num = 4 # how many numbers to read
        intnums = num/2

        try:
            temp = [s.strip() for s in self.inFile.readline().split()]

            # this will crash if try to convert a non-digit to an integer
            list = [int(s) for s in temp[0:intnums]]

            list.append(float(temp[num-2]))
            list.append(float(temp[num-1]))

            # convert 1st value in list to integer
            logging.debug('modelinput : read_material : list = %s', list)
            return list
        except ValueError :
            logging.debug('modelINPUT : read_material : ValueError  Exception thrown, check input values!')
            sys.exit('modelINPUT : read_material : ValueError Exception thrown, check input values!')
            return



    def get_object_values(self):
        """
        Get the model input values for this object
        :return:
        """

        # get nnod
        nnod = self.read_int()
        logging.debug('get_object_values : nnod = %s', nnod)

        # get kkmax
        kkmax = self.read_int()
        logging.debug('get_object_values : kkmax = %s', kkmax)

        # get nmat
        nmat = self.read_int()
        logging.debug('get_object_values : # of material layers, nmat = %s', nmat)

        # Read INN(i), IMAT(i), RAD(i)  for each material
        INN = []
        IMAT = []
        RAD = []

        # Read in INN, IMAT, RAD grouped together
        for ii in range(nmat):
            # Get # of nodes in the layer
            INN.append(self.read_int())

        logging.debug("get_object_values : INN : %s", INN)

        # Get the materials
        for ii in range(nmat):
            # Read nodes / layer
            #IMAT.append(self.read_list(4))
            IMAT.append(self.read_material())


        logging.debug("get_object_values : IMAT: % s", IMAT)

        # Get the radii in meters and convert to mm
        for ii in range(nmat):
            # Get the outer radius for this material
            RAD.append(self.read_float()*modelINPUT.scaleFactor)

        logging.debug("modelinput : get_object_values : RAD: % s", RAD)

        # for ii in range(nmat):
        #     # Get # of nodes in the layer
        #     INN.append(self.read_int())
        #
        #     # Read nodes / layer
        #     IMAT.append(self.read_list(4))
        #
        #     # Get the outer radius for this material
        #     RAD.append(self.read_float())

        logging.debug('modelinput : get_object_values : INN = %s', INN)
        logging.debug('modelinput : get_object_values : IMAT = %s', IMAT)


        # Get inner most radius
        RI = self.read_float()*modelINPUT.scaleFactor
        logging.debug('modelinput : get_object_values : RI = %s', RI)

        # Get diameter/width for aero
        DAERO = self.read_float()*modelINPUT.scaleFactor
        logging.debug('modelinput : get_object_values : DAERO = %s', DAERO)


        # Skip a line
        self.skip(1)

        # Get length for aero
        LAERO = self.read_float()*modelINPUT.scaleFactor
        logging.debug('modelinput : get_object_values : LAERO = %s', LAERO)

        # Skip a line
        self.skip(1)

        # Get height for aero
        HAERO = self.read_float()*modelINPUT.scaleFactor
        logging.debug('modelinput : get_object_values : HAERO = %s',HAERO)

        # return a tuple of the needed values
        return (RI, RAD, DAERO, LAERO, HAERO, IMAT, INN)  # Getting quantity in read_model_input


    def setup_object(self, fout, name, itype=0, quantity=1):
        """
        Pass in the model inputs into the model object type
        :param fout:  the output filehandle
        :param name:  name of the model object
        :param itype:  the itype of model object
        :param quantity:  number of these objects
        :return:  The initialized model object
        """

        # Initialize modelObj
        modelObj = None

        # Read in all the dimension & material values from the input file
        inputs = self.get_object_values()
        logging.debug("modelinput : setup_object : inputs = %s", inputs)
        logging.debug("modelinput : setup_object : name = %s", name)
        logging.debug("modelinput : setup_object : itype = %s", itype)
        logging.debug("modelinput : setup_object : itype = %s", quantity)

        # Get class from dictionary, then call it to create an model object instance.
        # Will call the appropriate class based in what type inputs[0] is
        modelObj = modelINPUT.itypes[itype](fout, inputs[0], inputs[1], inputs[2], inputs[3],
                                            #inputs[4], inputs[5], quantity, name)
                                            inputs[4], inputs[5], inputs[6], quantity, name)

        return modelObj


    def searchWord(self, inFile, word):
        """
        Find next occurrence of NAME (to find each fragment section)
        :param inFile: the filehandle of the model input file
        :param word:  the word to search for
        """

        notFound = True
        x = inFile.tell()  # where the current file pointer is
        logging.debug("modelinput: searchWord : searching for %s", word)
        logging.debug("modelinput: searchWord : x = %s", x)
        line = inFile.readline()
        while (notFound) and line :
            # read line, search for the word

            # Parse the line (remove spaces), returns list
            #aLine = inFile.readline().split()
            aLine = line.split()

            logging.debug("modelinput: searchWord: aLine = %s", aLine)

            # Iterate words and test to see if they match our word
            for sWord in aLine:
                # if it matches, append it to our list
                if sWord == word:
                    notFound = False
                    logging.debug("SearchWord : Found the word : %s",  word)
                    # reset pointer back to line where word was found
                    # logging.debug("Resetting file pointer to %s",x)
                    # inFile.seek(x)
                    return aLine

            # Read the next line
            # x = inFile.tell()  # where the current file pointer is
            # logging.debug("searchWord : x = %s", x)
            line = inFile.readline()


        # If got to end of file and still not found.........
        if (notFound) :
            logging.info("Didn't find %s", word)
            # Reset the file pointer
            inFile.seek(x)
            # Return nothing
            return None




    def getNumFrags(self,inList):
        """
        Get the total number of fragments in this input file
        :param: inList : the list input
        :return: int value of 1st value in inList
        """
        return int(inList[0])

    def getItype(self,inList):
        """
        Get the itype from the input list (strings)
        :param inList:
        :return:  int value of 1st value in inList
        """
        return int(inList[0])

    def getName(self, inList):
        """
        Get the name of object
        :param inList:  the list input (strings)
        :return: the name of the object
        """
        # My Name (QTY. 1)

        indQty = inList.index(modelINPUT.qtyWord )

        spacer = " "
        name = spacer.join(inList[0:indQty])
        logging.debug("modelinput : getName : name = %s", name)

        return name

    def getParentName(self):
        return (self.inFile.readline().strip())



    def getQuantity(self, inList):
        """
        Get the quantity of objects
        :param inList:  the input list of strings
        :return:  the quantity of the object
        """
        # My Name (QTY. 4)
        # My Name (QTY. 124)
        indQty = inList.index(modelINPUT.qtyWord)

        logging.debug("modelinput : getQuantity : inList = %s", inList)
        logging.debug("modelinput : getQuantity : indQty = %s", indQty)

        # Check how many numbers in quantity value
        numNumbers = sum(c.isdigit() for c in inList[indQty+1])

        logging.debug("numNumbers = %s", numNumbers)

        logging.debug("quantity = %s", int(inList[indQty+1][0:numNumbers]))

        return int(inList[indQty+1][0:numNumbers])



