# -*- coding: utf-8 -*-

from modelobject import modelOBJECT
import logging

# ===================================================================
# Define the cylinder Class
# ===================================================================
class CYLINDER(modelOBJECT):
    # Initialize the cylinder
    def __init__(self, fout, innermostRad=0.0, outerRads=[0], daero=0.0, length=0.0, haero=0.0,
                 #matnum = [-1], quantity = 1, name = " " ):
                 matnum = [-1], inns = [-1], quantity = 1, name = ' '):

        # check dimensions
        assert length > 0.0, "length <= 0 !! : %d" % length

        # daero is not used in cylinders

        modelOBJECT.__init__(self, fout, innermostRad, outerRads, length,
                             haero, matnum, inns, quantity, name)



        # minimum drawable inner radius
        self.innermostDraw = .001

        # Make sure inner most radius (if not 0) is bigger than smallest drawable inner radius
        if self.innermostRad < self.innermostDraw and self.innermostRad >= 0. :
            self.innermostRad = self.innermostDraw


    def object_type(self):
        """"Return a string representing the type of object this is."""
        return 'cylinder'

    # Calculate the position of the object
    def calc_object_position(self):
        self.objectPosition = (self.gridPosition[0] + self.outerRads[0],
                               self.gridPosition[1],
                               self.gridPosition[2])


    # ----------------------------------------------
    # Write out the macro file to draw the cylinder
    # ----------------------------------------------
    def write_macro(self):

        # Write out the quantity
        self.fout.write('quantity = ' + str(self.quantity) + '\n')

        # Write out the outer radii
        self.fout.write('outerRADS = [')
        for n in range(0, len(self.outerRads)-1):
            self.fout.write(str(self.outerRads[n]) + ",")
        self.fout.write(str(self.outerRads[len(self.outerRads)-1]))
        self.fout.write(']\n')

        # Write out the LAERO value
        self.fout.write('LAERO = ' + str(self.laero) + '\n')

        # Write out the innermostRad value
        self.fout.write('innermostRad = ' + str(self.innermostRad) + '\n')

        # Write out the position vector
        self.fout.write("gridPosition = "  + str(self.gridPosition) + "\n")

        # Write out the position vector
        self.fout.write("objectPosition = " + str(self.objectPosition) + "\n")

        # Make all the cylinders
        for n in range(0, len(self.outerRads)):
            self.fout.write('cyl' + str(n) + ' = Part.makeCylinder(outerRADS[' + str(n) + '], LAERO,' +
                            ' Base.Vector(0,0,0), xz)\n')

        # Only do this if innermost radius > 0 :
        if self.innermostRad > 0 :
            # Make the inner cylinder
            self.fout.write('innerCyl = Part.makeCylinder(innermostRad, LAERO,' +
                            ' Base.Vector(0,0,0), xz)\n')

        logging.debug("cylinder: write_macro : quantity = : %s", self.quantity)

        if self.quantity > 1 :
            totalVerticalWidth = modelOBJECT.vertMultiplier * self.outerRads[0]
            vertPosition = (0., 0., totalVerticalWidth)
            self.fout.write("vertPosition = " + str(vertPosition) + "\n")
            logging.debug("cylinder: write_macro : Quantity > 1, vertPosition = %s", vertPosition)

        # cut out the inner cylinders
        for n in range(0, len(self.outerRads)-1):
            # set up partname
            partName = 'cylcut' + str(n)
            self.fout.write(partName + ' = cyl' + str(n) + '.cut(cyl' + str(n + 1) + ')' '\n')

            # Translate the cylinder
            self.fout.write(partName + ".translate(Base.Vector(objectPosition))\n" )

            shadeType = "Flat Lines"
            if n == 0:
                shadeType = "Shaded"

            self.display_object(partName, self.colors[n], "outerTransparency", shadeType)

            if self.quantity > 1:
                for ii in range(1, self.quantity):
                    self.fout.write(partName + ".translate(Base.Vector(vertPosition))\n")
                    self.display_object(partName, self.colors[n], "outerTransparency", shadeType)


        # Show the last cylinder : special case b/c may not be any inner cuts
        # FreeCAD will crash if try to cut out a size that equals 0
        n = len(self.outerRads) - 1
        if self.innermostRad > 0 :

            partName = 'cylcut' + str(n)
            self.fout.write(partName + ' = cyl' + str(n) + '.cut(innerCyl)\n')

            # Translate the cylinder
            self.fout.write(partName + ".translate(Base.Vector(objectPosition))\n" )

            # ---------------------------------------------------------------------
            # Create an active document object to set the transparency and color
            # ---------------------------------------------------------------------
            # self.fout.write(partName + 'Obj = App.ActiveDocument.addObject("Part::Feature", "' + partName + '")\n')
            # self.fout.write(partName + 'Obj.Shape = ' + partName + '\n')
            #
            # # set transparency
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

        else:

            partName = 'cyl' + str(n)

            # Translate the cylinder
            self.fout.write(partName + ".translate(Base.Vector(objectPosition))\n")

            # ---------------------------------------------------------------------
            # Create an active document object to set the transparency and color
            # ---------------------------------------------------------------------
            # self.fout.write(partName + 'Obj = App.ActiveDocument.addObject("Part::Feature", "' + partName + '")\n')
            # self.fout.write(partName + 'Obj.Shape = ' + partName + '\n')
            #
            # # set transparency of outer sphere to 80%
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


        # write out the text position
        self.fout.write('textPosition = ' + str(self.textPosition) + '\n')

        # call function to write out the text
        # self.fout.write('writeObjectText("' + self.name + '", ' + str(
        #                 len(self.materials)) + ', ' + str(self.materials) + ', ' + str(self.quantity) + ', textPosition)\n')

        self.fout.write('writeObjectText("' + self.name + '", ' + str(
            len(self.materials)) + ', ' + str(self.materials) + ', ' + str(self.inns) + ', ' + str(
            self.quantity) + ', textPosition)\n')




# ===================================================================
# End of Cylinder class
# ===================================================================





