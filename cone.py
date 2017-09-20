# -*- coding: utf-8 -*-

from modelobject import modelOBJECT
import logging

# ===================================================================
# Define the cone Class
# ===================================================================
class CONE(modelOBJECT):
    # Initialize the cylinder
    # haero is not used - only used a place holder for setting up modelobjects of unknown class
    def __init__(self, fout, innermostRad=0.0, outerRads=[0], daero=0.0, length=0.0, haero=0.0,
                 #matnum=[-1], quantity=1, name=' '):
                 matnum = [-1], inns = [-1], quantity = 1, name = ' '):

        assert length > 0.0, "length <= 0 !! : %d" % length

        logging.debug("cone : innermostRad = %s", innermostRad)
        logging.debug("cone : outerRads = %s", outerRads)
        logging.debug("cone : length = %s", length)
        logging.debug("cone : haero = %s", haero)
        logging.debug("cone : matnum = %s", matnum)
        logging.debug("cone : inns = %s", inns)
        logging.debug("cone : quantity  = %s", quantity)
        logging.debug("cone : name = %s", name)

        modelOBJECT.__init__(self, fout, innermostRad, outerRads, length, haero,
                             matnum, inns, quantity, name)

        logging.debug("cone : gridPosition = %s", self.gridPosition)
        logging.debug("cone : objectPosition = %s", self.objectPosition)


    def object_type(self):
        """"Return a string representing the type of object this is."""
        return 'cone'

    # Calculate the position of the object
    def calc_object_position(self):
        """
        Get the object position
        :return:
        """
        self.objectPosition = (self.gridPosition[0] + self.outerRads[0],
                               self.gridPosition[1],
                               self.gridPosition[2])

    # ----------------------------------------------
    # Write out the macro file to draw the cone
    # ----------------------------------------------
    def write_macro(self):
        """
        Write out the macro file for FreeCAD to read
        :return:
        """

        # Write out the quantity
        self.fout.write('quantity = ' + str(self.quantity) + '\n')

        # Write out the outer radii
        self.nested_write('outerRADS', self.outerRads)

        # Write out the LAERO value
        self.fout.write('LAERO = ' + str(self.laero) + '\n')

        # Write out the innermostRad value
        self.fout.write('innermostRad = ' + str(self.innermostRad) + '\n')

        # Write out the position vectors
        self.fout.write("gridPosition = " + str(self.gridPosition) + "\n")
        self.fout.write("objectPosition = " + str(self.objectPosition) + "\n")

        # Make all the cones
        # 0.0 has to be in there,  is the radius of 2nd cone
        # cone = Part.makeCone(outerRADS5[0], 0.0, LAERO, Base.Vector(0,0,0), xz)
        for n in range(0, len(self.outerRads)):
            self.fout.write('cyl' + str(n) + ' = Part.makeCone(outerRADS[' + str(n) + '], 0.0, LAERO, Base.Vector(0,0,0), xz)\n')


        # Only do this if innermost radius > 0 :
        if self.innermostRad > 0 :
        #     # Make the inner cone
            self.fout.write('innerCyl = Part.makeCone(innermostRad, LAERO, Base.Vector(0,0,0), xz)\n')

        logging.debug("cone: write_macro : quantity = : %s", self.quantity)

        # if there is more than 1 cone, set up the vertical positioning for the cones
        if self.quantity > 1 :
            totalVerticalWidth = modelOBJECT.vertMultiplier * self.outerRads[0]
            vertPosition = (0., 0., totalVerticalWidth)
            self.fout.write("vertPosition = " + str(vertPosition) + "\n")
            logging.debug("cone: write_macro : Quantity > 1, vertPosition = %s", vertPosition)

        # Cut out the inner cones
        for n in range(0, len(self.outerRads)-1):
            partName = 'cylcut' + str(n)
            self.fout.write(partName + ' = cyl' + str(n) + '.cut(cyl' + str(n + 1) + ')' '\n')

            self.fout.write(partName + ".translate(Base.Vector(objectPosition))\n")

            self.display_object(partName, self.colors[n], "outerTransparency", "Shaded")

            if self.quantity > 1 :
                for ii in range(1,self.quantity) :
                    self.fout.write(partName + ".translate(Base.Vector(vertPosition))\n")
                    self.display_object(partName, self.colors[n], "outerTransparency", "Shaded")


        # Show the last cone : special case b/c may not be any inner cuts
        # FreeCAD will crash if try to cut out a size that equals 0
        n = len(self.outerRads) - 1
        if self.innermostRad > 0 :

            partName = 'cylcut' + str(n)
            self.fout.write(partName + ' = cyl' + str(n) + '.cut(innerCyl)\n')

            self.fout.write(partName + ".translate(Base.Vector(objectPosition))\n")

            self.display_object(partName, modelOBJECT.white, "hollowTransparency", "Shaded")

            if self.quantity > 1:
                for ii in range(1, self.quantity):
                    self.fout.write(partName + ".translate(Base.Vector(vertPosition))\n")
                    self.display_object(partName, modelOBJECT.white, "hollowTransparency", "Shaded")


        else:

            partName = 'cyl'  + str(n)

            self.fout.write(partName + ".translate(Base.Vector(objectPosition))\n")

            self.display_object(partName, self.colors[n], "outerTransparency", "Shaded")

            if self.quantity > 1:
                for ii in range(1, self.quantity):
                    self.fout.write(partName + ".translate(Base.Vector(vertPosition))\n")
                    self.display_object(partName, self.colors[n], "outerTransparency", "Shaded")

        # --------------------------------------------------------------------------------------------------------

        # Write out the text position
        self.fout.write('textPosition = ' + str(self.textPosition) + '\n')

        # call function to write out the text
        self.fout.write('writeObjectText("' + self.name + '", ' + str(
            len(self.materials)) + ', ' + str(self.materials) + ', ' + str(self.inns) + ', ' + str(self.quantity) + ', textPosition)\n')

# ===================================================================
# End of Cone class
# ===================================================================





