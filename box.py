# -*- coding: utf-8 -*-
"""Box, subclass of model class, for drawing boxes"""

import logging
from modelobject import modelOBJECT

# ===================================================================
# Define the cylinder Class
# ===================================================================
class BOX(modelOBJECT):
    """BOX is a type of model object"""

    # Initialize the cylinder
    def __init__(self, fout, innermostRad=0.0, outerRads=[0], daero=0.0, length=0.0, haero=0.0, matnum=[-1],
                 inns =[-1], quantity = 1, name = ' '):

        # make sure dimensions aren't negative
        assert daero > 0.0, "daero <= 0 !! : %d" % daero
        assert length > 0.0, "length <= 0 !! : %d" % length
        assert haero > 0.0, "haero <= 0 !! : %d" % haero

        modelOBJECT.__init__(self, fout, innermostRad, outerRads, length, haero,
                             matnum, inns, quantity, name)


        self.set_outerValues(daero, length, haero)

        # set thickness of box
        self.thickness = self.calc_thickness()

        # Thickness of box give the thickness of the box around the hollow center
        assert 2.0*self.thickness < daero, "2*thickness >= daero !! : %d" % self.thickness
        assert 2.0*self.thickness < length, "2*thickness >= length !! : %d" % self.thickness
        assert 2.0*self.thickness < haero, "2*thickness >= haero !! : %d" % self.thickness

        self.set_innerValues(daero)



    # print the object
    # has to return a string
    def __str__(self):
        """Print the box attributes"""
        temp = "type of object : %s" % self.object_type() + "\n"
        temp = temp + "Outer radii : "
        temp = temp + " ".join("%.5f" % x for x in self.outerRads) + "\n"
        temp = temp + "diameters : "
        temp = temp + " ".join("%.5f" % x for x in self.outerDiams) + "\n"

        temp = temp + " ".join("%.5f" % x for x in self.outerLengths) + "\n"

        temp = temp + " ".join("%.5f" % x for x in self.outerHeights) + "\n"

        temp = temp + "Innermost Radius : %.5f" % self.innermostRad + "\n"
        temp = temp + "Inner diameter : %.5f" % self.innerDiam + "\n"
        temp = temp + "Inner length : %.5f" % self.innerLength + "\n"
        temp = temp + " ".join("%.5f" % x for x in self.gridPosition) + "\n"
        temp = temp + " ".join("%.5f" % x for x in self.objectPosition) + "\n"
        temp = temp + "quantity : %s" % self.quantity + "\n"
        temp = temp + "name : %s" % self.name
        return temp

    def object_type(self):
        """"Return a string representing the type of object this is."""
        return 'box'

    # For Boxes, grid position and object position are the same
    def calc_object_position(self):
        self.objectPosition = self.gridPosition


    # Size of inner hollow box is same ratio as outer most box
    # The width of the inner box is given by the innermost radius
    def set_outerValues(self, daero, laero, haero):
        #self.outerDiams = [x * 2.0 for x in self.outerRads]

        self.outerDiams = []
        self.outerDiams.append(daero)

        self.outerLengths = []
        self.outerLengths.append(laero)

        self.outerHeights = []
        self.outerHeights.append(haero)


    # Size of inner hollow box is same ratio as outer most box
    # The width of the inner box is given by the innermost radius
    def set_innerValues(self, daero):

        # THIS MAY NOT BE NEEDED - ASSERTING THAT THICKNESS < 2*daero in __init__ **********
        if self.thickness == daero:
            self.innerDiam = 0.
            self.innerLength = 0.
            self.innerHeight = 0.
        else:
            # Must subtract twice the thickness
            self.innerDiam = self.outerDiams[len(self.outerDiams) - 1] - 2.0*self.thickness
            self.innerLength = self.outerLengths[len(self.outerLengths) - 1] - 2.0*self.thickness
            self.innerHeight = self.outerHeights[len(self.outerHeights) - 1] - 2.0*self.thickness


    def calc_thickness(self):
        return self.outerRads[0] - self.innermostRad

    # ----------------------------------------------
    # Write out the macro file to draw the cylinder
    # ----------------------------------------------
    def write_macro(self):

        logging.debug("box : write_macro : Writing macro........")

        # Write out the quantity
        self.fout.write('quantity = ' + str(self.quantity) + '\n')

        self.nested_write('outerDiams', self.outerDiams)
        self.nested_write('outerLengths', self.outerLengths)
        self.nested_write('outerHeights', self.outerHeights)

        # Write out the grid position vector
        self.fout.write("gridPosition = " + str(self.gridPosition) + "\n")

        # Write out the object position vector
        self.fout.write("objectPosition = " + str(self.objectPosition) + "\n")


        # Only do this if thickness > 0 :
        if (self.thickness > 0.):

            # Write out the inner width
            self.fout.write('innerDiam = ' + str(self.innerDiam) + '\n')

            # Write out the inner length
            self.fout.write('innerLength = ' + str(self.innerLength) + '\n')

            # Write out the inner length
            self.fout.write('innerHeight = ' + str(self.innerHeight) + '\n')

            # Write out the inner length
            self.fout.write('thickness = ' + str(self.thickness) + '\n')



        # Make all the boxes

        logging.debug("box : write_macro : self.outerDiams = %s", self.outerDiams)
        # Initialize relativePosition
        relativePosition = (0,0,0)
        for n in range(0, len(self.outerRads)):
            partName = 'box' + str(n)
            self.fout.write('box' + str(n) + ' = Part.makeBox(outerDiams[' + str(n) + '], outerLengths[' + str(n) + ']  , outerHeights[' + str(n) + ']  )\n')

            # Translate the inner boxes to their realtive positions w/in the box
            if n > 0:
                # translation vector for inside the box (relative to box only)
                self.fout.write('relativePosition = (outerDiams[' + str(n) + '] / 2.0, outerLengths[' + str(n) + '] / 2.0, outerHeights[' + str(n) + '] / 2.0)\n')

                # translate the boxes to position in the box
                self.fout.write(partName + '.translate(Base.Vector(relativePosition))\n')

        if self.thickness != 0. :
            self.fout.write('innerBox = Part.makeBox(innerDiam, innerLength, innerHeight)\n')

            # translation vector for inside the box (relative to box only)
            self.fout.write('innerPosition = (thickness, thickness, thickness)\n')

            # translate the innr box to position in the box
            self.fout.write('innerBox.translate(Base.Vector(innerPosition))\n')

        logging.debug("box: write_macro : quantity = : %s", self.quantity)

        if self.quantity > 1 :
            #totalVerticalWidth = 3.*self.outerHeights[0]
            totalVerticalWidth = modelOBJECT.vertMultiplier * self.outerHeights[0]
            vertPosition = (0., 0., totalVerticalWidth)
            self.fout.write("vertPosition = " + str(vertPosition) + "\n")
            logging.debug("box: write_macro : Quantity > 1, vertPosition = %s", vertPosition)



        # Cut out the inner boxes & translate them to grid position
        for n in range(0, len(self.outerRads)-1):

            partName = 'boxcut' + str(n)
            self.fout.write(partName + ' = box' + str(n) + '.cut(box' + str(n + 1) + ')' '\n')

            # translate the boxes to grid position
            self.fout.write(partName + '.translate(Base.Vector(gridPosition))\n')

            self.display_object(partName, self.colors[n], "outerTransparency", "Shaded")

            if self.quantity > 1:
                for ii in range(1, self.quantity):
                    self.fout.write(partName + ".translate(Base.Vector(vertPosition))\n")
                    self.display_object(partName, self.colors[n], "outerTransparency", "Shaded")


        # Show the last box : special case b/c there may not be any inner cuts
        # FreeCAD will crash if try to cut out a size that equals 0
        n = len(self.outerRads) - 1
        if self.thickness != 0. :

            partName = 'boxcut' + str(n)

            # Need to cut out the box inside
            self.fout.write(partName + ' = box' + str(n) + '.cut(innerBox)\n')

            self.fout.write(partName + '.translate(Base.Vector(gridPosition))\n')

            shadeType = "Flat Lines"
            self.display_object(partName, self.colors[n], "outerTransparency", shadeType)

            if self.quantity > 1:
                for ii in range(1, self.quantity):
                    self.fout.write(partName + ".translate(Base.Vector(vertPosition))\n")
                    self.display_object(partName, self.colors[n], "outerTransparency", shadeType)


            # translate inner box
            self.fout.write("innerBox.translate(Base.Vector(gridPosition))\n")


            shadeType = "Flat Lines"
            partName = "innerBox"
            self.display_object(partName, modelOBJECT.white, "hollowTransparency", shadeType)

            if self.quantity > 1:
                for ii in range(1, self.quantity):
                    self.fout.write(partName + ".translate(Base.Vector(vertPosition))\n")
                    self.display_object(partName, modelOBJECT.white, "hollowTransparency", shadeType)


        else:

            partName = 'box' + str(n)

            # translate the box to grid position
            self.fout.write(partName + '.translate(Base.Vector(gridPosition))\n')

            # ---------------------------------------------------------------------
            # Create an active document object to set the transparency and color
            # ---------------------------------------------------------------------
            # self.fout.write(partName + 'Obj = App.ActiveDocument.addObject("Part::Feature", "' + partName + '")\n')
            # self.fout.write(partName + 'Obj.Shape = ' + partName + '\n')
            #
            # # set transparency of outer box
            # self.fout.write(partName + 'Obj.ViewObject.Transparency = outerTransparency\n')
            #
            # self.fout.write('color = ' + str(self.colors[n]) + '\n')
            # self.fout.write(partName + 'Obj.ViewObject.ShapeColor = color  \n')

            shadeType = "Flat Lines"
            self.display_object(partName, self.colors[n], "outerTransparency", shadeType)

            if self.quantity > 1:
                for ii in range(1, self.quantity):
                    self.fout.write(partName + ".translate(Base.Vector(vertPosition))\n")
                    self.display_object(partName, self.colors[n], "outerTransparency", shadeType)



        logging.debug('box : write_macro : self.thickness = %s', self.thickness)



        # write out the text position
        self.fout.write('textPosition = ' + str(self.textPosition) + '\n')  # call function to write out the text
        # self.fout.write('writeObjectText("' + self.name + '", ' + str(
        #                 len(self.materials)) + ', ' + str(self.materials) + ', ' + str(self.quantity) + ', textPosition)\n')

        self.fout.write('writeObjectText("' + self.name + '", ' + str(
            len(self.materials)) + ', ' + str(self.materials) + ', ' + str(self.inns) + ', ' + str(
            self.quantity) + ', textPosition)\n')


        self.fout.write('\n')



    # ---------------------
    # Get the object radii
    # ---------------------
    def get_radii(self):

        rads = [x / 2.0 for x in self.outerDiams]

        return rads

    # ---------------------
    # Get the object radii
    # ---------------------
    def get_lengths(self):

        rads = [x / 2.0 for x in self.outerLengths]

        return rads



# ===================================================================
# End of Box class
# ===================================================================





