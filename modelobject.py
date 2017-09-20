# -*- coding: utf-8 -*-
"""Abstract input object for model model"""

import logging
from abc import ABCMeta, abstractmethod

# ===================================================================
# Define the cylinder Class
# ===================================================================
class modelOBJECT:
    """An model input object
     Attributes:
         type : type of object (box, etc)
         outerRads : the list of outer radii
         innermostRad : the inner most radius
         laero : length of the object
         haero : height of the object
         quantity : how many of this object
     """

    # Colors of materials which correspond to their meltiing temperatures
    # These have to be float values
    userInputColor = (1., 62./255., 150./255.)  # pink
    yellowgreen = (154. / 255., 205. / 255., 0.)
    black = (0., 0., 0.)
    white = (1., 1., 1.)
    deepskyblue = (0., 191. / 255., 255. / 255.)
    darkgoldenrod = (184. / 255., 134. / 255., 11. / 255.)

    yellow = (1., 1., 0.)
    #yellow = (1., 215./255., 0.)

    red = (1., 0., 0.)
    darkgray = (169. / 255., 169. / 255., 169. / 255.)
    brightyellow = (33., 88., 200.)

    # Multiplier for calculating vertical width between quantities of objects
    vertMultiplier = -3.

    materials = {-4: ('user input', userInputColor),
				 -3: ('user input', userInputColor),
				 -2: ('user input', userInputColor),
				 -1: ('user input', userInputColor),
                 1: ('Alumina', red),
                 2: ('Al 1145-H19', darkgray),
                 3: ('Al 2024-T3', darkgray),
                 4: ('Al 2024-T8xx', darkgray),
                 5: ('Al (IADC)', darkgray),
                 6: ('Al 2219-T8xx', darkgray),
                 7: ('Al 5052', darkgray),
                 8: ('Al 6061-T6', darkgray),
                 9: ('Al 7075-T6', darkgray),
                 10: ('Barium', deepskyblue),
                 11: ('Berylium element', yellowgreen),
                 12: ('Beta cloth', yellowgreen),
                 13: ('Brass, Red', darkgoldenrod),
                 14: ('Brass, Cartridge', darkgoldenrod),
                 15: ('Brass, Muntz', darkgoldenrod),
                 #16: ('Carbon-Carbon Reinforced', red),
                 16: ('RCC', red),
                 17: ('Cobalt', yellow),
                 18: ('Cork', deepskyblue),
                 19: ('Cu alloy', darkgoldenrod),
                 20: ('Cu/Be (0.5% Be)', darkgoldenrod),
                 21: ('Cu/Be (1.9% Be)', darkgoldenrod),
                 22: ('Fiberfrax', red),
                 23: ('Fiberglass', darkgoldenrod),
                 #24: ('Gallium Arsenide', yellow),
				 24: ('GaAs', yellow),
                 25: ('Germanium', darkgoldenrod),
                 26: ('Gold', darkgoldenrod),
                 27: ('Graphite Epoxy 1', black),
                 28: ('Graphite Epoxy 2', black),
                 29: ('Hastelloy c', yellow),
                 30: ('Hastelloy 25', yellow),
                 31: ('Hastelloy 188', yellow),
                 32: ('Hastelloy n', yellow),
                 33: ('Inconel x', yellow),
                 34: ('Inconel 600', yellow),
                 35: ('Inconel 601', yellow),
                 36: ('Inconel 625', yellow),
                 37: ('Inconel 718', yellow),
                 38: ('Iron (Armco)', yellow),
                 39: ('Lead Element', yellowgreen),
                 40: ('Macor Ceramic', darkgoldenrod),
                 41: ('Magnesium AZ31', darkgray),
                 42: ('Mgnesium HK31A', darkgray),
                 43: ('Molybdenum', red),
                 44: ('MLI', yellowgreen),
                 45: ('MP35N', yellow),
                 46: ('Nickel', yellow),
                 47: ('Niobium', red),
                 48: ('NOMEX', yellowgreen),
                 49: ('Platinum', red),
                 50: ('Polyamide', yellowgreen),
                 51: ('Rene 41', yellow),
                 52: ('Silver Element', darkgoldenrod),
                 53: ('Sodium-Iodide', deepskyblue),
                 54: ('Stainless Steel (IADC)', yellow),
                 55: ('Steel 21-6-9', yellow),
                 56: ('Steel 17-4 ph', yellow),
                 57: ('Steel A-286', yellow),
                 58: ('Steel AISI 304', yellow),
                 59: ('Steel AISI 316', yellow),
                 60: ('Steel AISI 321', yellow),
                 61: ('Steel AISI 347', yellow),
                 62: ('Steel AISI 410', yellow),
                 63: ('Strontium', deepskyblue),
                 64: ('Teflon', yellowgreen),
                 65: ('Titanium (6 Al-4 V)', red),
                 66: ('Titanium (IADC)', red),
                 67: ('Tungsten', red),
                 68: ('Uranium', yellow),
                 #69: ('Uranium Zirconium Hydride (UZrH)', red),
                 69: ('UZrH', red),
                 70: ('Zinc', yellowgreen),
                 71: ('Zerodur', yellow),
                 72: ('Invar', yellow),
                 73: ('FRCI-12 shuttle tiles', red),
                 74: ('RCG Coating', red),
                 75: ('Water', yellowgreen),
                 76: ('Acrylic', yellowgreen),
                 77: ('Polycarbonate', yellowgreen),
                 78: ('Al 2195 (AlLi)', darkgray),
                 79: ('Al 2090', darkgray),
                 80: ('A356 (Aluminum)', darkgray)}




    # Initialize the object
    def __init__(self, fout, innermostRad=0.0, outerRads=[0], length=0.0, haero=0.0,
                 #matnums = [-1], quantity = 1, name = " " ):
                 matnums = [-1], inns = [-1], quantity = 1, name = " " ):

        """
        Initialize a new modelOBJECT object
        :param fout:  filehandle of output file
        :param innermostRad:  list of inner radii, out -> in
        :param outerRads:  list of outer radii, out -> in
        :param length: length of the object
        :param haero:  height of the object
        :param matnums:  material numbers of the object
        :param quantity:  quantity of this model object
        :param name: name of the model object
        """

        # Check that quantity is 1 or greater
        assert quantity >= 1, "quantity <= 1 : %d " % quantity

        # Layers go from inner to outer

        # Set up the outer radii
        self.outerRads = outerRads

        # Set up inner most radius
        self.innermostRad = innermostRad

        # the length of the object
        self.laero = length

        # height of the object
        self.haero = haero

        # Get color of the materials
        self.matnums = matnums

        # Get the number of nodes for each layer
        self.inns = inns

        # Set the grid position vector
        self.gridPosition = None

        # Set the grid position vector
        self.objectPosition = None

        # initialize text position
        #self.calc_text_position()  # done later

        # Get the quantity (how many of these objects there are)
        self.quantity = quantity

        # set the colors
        self.set_colors()

        # set the materials
        self.set_materials()



        logging.debug("length = %s", length)

        # make sure values are valid
        assert innermostRad >= 0.0, "innermostRad < 0 !! : %d" % innermostRad
        assert self.is_valid(), "outerRads not valid !! "

        # moved this into box class, cylinder class, cone class
        #assert length > 0.0, "length <= 0 !! : %d" % length

        # self.macroName = name
        # self.outDir = outDir
        self.fout = fout

        # Set the name of the object
        self.name = name



    # check for valid outer Radii
    def is_valid(self):
        """Check to see if the outer radii are > 0"""
        for rr in self.outerRads:
             if rr < 0:
                 return False
        return True


    # print the object
    # has to return a string
    def __str__(self):
        temp = "type of object : %s" % self.object_type + "\n"
        temp = temp + "Innermost Radius : %.3f" % self.innermostRad + "\n"
        temp = temp + "Outer radii : "
        temp = temp + " ".join("%.3f" % x for x in self.outerRads) + "\n"
        temp = temp + "Length : %.3f" % self.laero + "\n"
        temp = temp + "gridPosition " + str(self.gridPosition) + "\n"
        temp = temp + "objectPosition " + str(self.objectPosition) + "\n"
        temp = temp + "text position " + str(self.textPosition) + "\n"
        return temp


    @abstractmethod
    def object_type(self):
        """Abstract method to return the type of object"""
        pass

    """Set the colors"""
    def set_colors(self):
        # Get color of the materials
        logging.debug("matnums = %s", self.matnums)
        # Get the corresponding colors for each material
        self.colors = [modelOBJECT.materials[nn[0]][1] for nn in self.matnums]
        #    ['hello{0}'.format(i) for i in a]
        logging.debug("colors = %s",self.colors)


    """Set the material names"""
    def set_materials(self):
        self.materials = [modelOBJECT.materials[nn[0]][0] for nn in self.matnums]
        logging.debug("materials = %s", self.materials)

    # ---------------------------------------
    # Print outer radii
    # ---------------------------------------
    def print_outerRads(self):
        """Print the outer radii of the model object"""
        print "Outer radii = "
        for rad in self.outerRads:
             print str(rad) + " "


    # ---------------------------------------
    # Print inner most radius
    # ---------------------------------------
    def print_innermostRad(self):
        """Print the innermost radius of the object"""
        print "Innermost radii = " + str(self.innermostRad)


    # ---------------------
    # Get the object radii
    # ---------------------
    """Returns radii unless overridden"""
    def get_radii(self):
        return self.outerRads

    # ---------------------
    # Get the object radii
    # ---------------------
    """Returns radii"""
    def get_lengths(self):
        return self.outerRads

    # -------------------------------
    # Get the position of the object
    # -------------------------------
    def get_gridPosition(self):
        return self.gridPosition

    # -------------------------------
    # Get the position of the object
    # -------------------------------
    def get_objectPosition(self):
        return self.objectPosition

    # -------------------------------
    # Get the position of the object
    # -------------------------------
    def set_grid_position(self, position):
        self.gridPosition = position

        # set the object position (uses the subclass calc_object_position)
        self.calc_object_position()

        # set the text position also.  Uses the grid position
        self.calc_text_position()

        return


    # Calculate the text position  - same for all shapes
    def calc_text_position(self):
        space = 10.
        #self.textPosition = (self.gridPosition[0], self.gridPosition[1] - 5., 0.0)
        self.textPosition = (self.gridPosition[0], self.gridPosition[1] - space, 0.0)
        return


    """Nested write out to the macro file"""
    def nested_write(self, name, variable):
        # 'outerDiams', self.outerDiams
        # Write out the layers
        # self.fout.write('outerDiams = [')
        self.fout.write(name + ' = [')

        # for n in range(0, len(self.outerDiams)-1):
        for n in range(0, len(variable) - 1):
            # self.fout.write(str(self.outerDiams[n]) + ",")
            self.fout.write(str(variable[n]) + ",")

        # self.fout.write(str(self.outerDiams[len(self.outerDiams)-1]))
        self.fout.write(str(variable[len(variable) - 1]))

        self.fout.write(']\n')


    #def display_object(self, partName, num, displayMode):
    def display_object(self, partName, color, transparency="outerTransparency", displayMode="Shaded"):

        # ---------------------------------------------------------------------
        # Create an active document object to set the transparency and color
        # ---------------------------------------------------------------------
        self.fout.write(partName + 'Obj = App.ActiveDocument.addObject("Part::Feature", "' + partName + '")\n')
        self.fout.write(partName + 'Obj.Shape = ' + partName + '\n')

        # set transparency
        #self.fout.write(partName + 'Obj.ViewObject.Transparency = outerTransparency\n')
        self.fout.write(partName + 'Obj.ViewObject.Transparency = ' + transparency.strip() + '\n')

        self.fout.write('color = ' + str(color) + '\n')
        self.fout.write(partName + 'Obj.ViewObject.ShapeColor = color  \n')

        #self.fout.write(partName + 'Obj.ViewObject.DisplayMode = "Shaded"  \n')
        self.fout.write(partName + 'Obj.ViewObject.DisplayMode = "' + displayMode.strip() +  '" \n')


# ===================================================================
# End of modelOBJECT class
# ===================================================================




