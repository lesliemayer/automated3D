# -*- coding: utf-8 -*-
"""sphere object, subclass of an modelOBJECT"""

from modelobject import modelOBJECT
import logging

# ===================================================================
# Define the sphere Class
# ===================================================================
class SPHERE(modelOBJECT):
    # Initialize the sphere object
    def __init__(self, fout, innermostRad=0.0, outerRads=[0], daero=0.0, length=0.0,  haero=0.0, matnum=[-1],
                 inns=[-1], quantity = 1, name = " "):

        # daero is not used for spheres, but need the placeholder

        logging.debug("sphere : innermostRad = %s", innermostRad)
        logging.debug("sphere : outerRads = %s", outerRads)
        logging.debug("sphere : length = %s", length)
        logging.debug("sphere : haero = %s", haero)
        logging.debug("sphere : matnum = %s", matnum)
        logging.debug("sphere : inns = %s", matnum)
        logging.debug("sphere : quantity  = %s", quantity)
        logging.debug("sphere : name = %s", name)

        modelOBJECT.__init__(self, fout, innermostRad, outerRads, length, haero,
                             matnum, inns, quantity, name)

        logging.debug("sphere : gridPosition = %s", self.gridPosition)
        logging.debug("sphere : objectPosition = %s", self.objectPosition)
        #logging.debug("sphere : textPosition = %s", self.textPosition)

    def object_type(self):
        """"Return a string representing the type of object this is."""
        return 'sphere'

    # Calculate the position of the object
    def calc_object_position(self):
        self.objectPosition = (self.gridPosition[0] + self.outerRads[0],
                               self.gridPosition[1] + self.outerRads[0],
                               self.gridPosition[2])

    # ----------------------------------------------
    # Write out the macro file to draw the sphere
    # ----------------------------------------------
    def write_macro(self):

        # Write out the quantity
        self.fout.write('quantity = ' + str(self.quantity) + '\n')

        # Write out the outer radii
        self.nested_write('outerRADS', self.outerRads)

        # Write out the innermostRad value
        self.fout.write('innermostRad = ' + str(self.innermostRad) + '\n')

        # Write out the position vectors
        self.fout.write("gridPosition = " + str(self.gridPosition) + "\n")
        self.fout.write("objectPosition = " + str(self.objectPosition) + "\n")

        # Make all the spheres
        for n in range(0, len(self.outerRads)):
            self.fout.write('sph' + str(n) + ' = Part.makeSphere(outerRADS[' + str(n) + '])\n')

        # Only make the inner hollow sphere if innermost radius > 0 :
        if self.innermostRad > 0 :
            # Make the inner sphere
            self.fout.write('innerSphere = Part.makeSphere(innermostRad)\n')

        logging.debug("cone: write_macro : quantity = : %s", self.quantity)

        if self.quantity > 1 :
            #totalVerticalWidth = 3*self.outerRads[0]
            totalVerticalWidth = modelOBJECT.vertMultiplier * self.outerRads[0]
            vertPosition = (0., 0., totalVerticalWidth)
            self.fout.write("vertPosition = " + str(vertPosition) + "\n")
            logging.debug("sphere: write_macro : Quantity > 1, vertPosition = %s", vertPosition)

        # Cut out the inner spheres
        for n in range(0, len(self.outerRads)-1):
            partName = 'sphcut' + str(n)
            self.fout.write(partName + ' = sph' + str(n) + '.cut(sph' + str(n + 1) + ')' '\n')

            self.fout.write(partName + ".translate(Base.Vector(objectPosition))\n")

            # ---------------------------------------------------------------------
            # Create an active document object to set the transparency and color
            # ---------------------------------------------------------------------
            # self.fout.write(partName + 'Obj = App.ActiveDocument.addObject("Part::Feature", "' + partName + '")\n')
            # self.fout.write(partName + 'Obj.Shape = ' + partName + '\n')
            #
            # # set transparency of outer sphere
            # self.fout.write(partName + 'Obj.ViewObject.Transparency = outerTransparency\n')
            #
            # self.fout.write('color = ' + str(self.colors[n]) + '\n')
            # self.fout.write(partName + 'Obj.ViewObject.ShapeColor = color  \n')
            # #if n == 0:
            # self.fout.write(partName + 'Obj.ViewObject.DisplayMode = "Shaded"  \n')

            self.display_object(partName, self.colors[n], "outerTransparency", "Shaded")

            if self.quantity > 1:
                for ii in range(1, self.quantity):
                    self.fout.write(partName + ".translate(Base.Vector(vertPosition))\n")
                    self.display_object(partName, self.colors[n], "outerTransparency", "Shaded")


        # Show the last sphere : special case b/c may not be any inner cuts
        # FreeCAD will crash if try to cut out a size that equals 0
        n = len(self.outerRads) - 1
        if self.innermostRad > 0 :
            partName = 'sphcut' + str(n)

            self.fout.write(partName + ' = sph' + str(n) + '.cut(innerSphere)\n')

            # Translate the cut sphere
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
            # #if n == 0:
            # self.fout.write(partName + 'Obj.ViewObject.DisplayMode = "Shaded"  \n')

            self.display_object(partName, self.colors[n], "outerTransparency", "Shaded")

            if self.quantity > 1:
                for ii in range(1, self.quantity):
                    self.fout.write(partName + ".translate(Base.Vector(vertPosition))\n")
                    self.display_object(partName, self.colors[n], "outerTransparency", "Shaded")

            # -------------------------------------------------------------------
            # Make the inner hollow sphere, color it white w/ less transparency
            # -------------------------------------------------------------------
            # translate inner sphere
            self.fout.write("innerSphere.translate(Base.Vector(objectPosition))\n")

            # ---------------------------------------------------------------------
            # Create an active document object to set the transparency and color
            # ---------------------------------------------------------------------
            # self.fout.write('innerObj = App.ActiveDocument.addObject("Part::Feature", "innerSphere") \n')
            # self.fout.write('innerObj.Shape = innerSphere \n')
            #
            # self.fout.write('innerObj.ViewObject.Transparency = hollowTransparency \n') # set this to a low number
            # self.fout.write('innerObj.ViewObject.ShapeColor = white \n')
            # self.fout.write('innerObj.ViewObject.DisplayMode = "Shaded" \n')

            partName = "innerSphere"

            self.display_object(partName, modelOBJECT.white, "hollowTransparency", "Shaded")

            if self.quantity > 1:
                for ii in range(1, self.quantity):
                    self.fout.write(partName + ".translate(Base.Vector(vertPosition))\n")
                    self.display_object(partName, modelOBJECT.white, "hollowTransparency", "Shaded")


        else:

            partName = 'sph' + str(n)

            # Translate the inner solid sphere
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
            # self.fout.write(partName + 'Obj.ViewObject.DisplayMode = "Shaded"  \n')

            self.display_object(partName, self.colors[n], "outerTransparency", "Shaded")

            if self.quantity > 1:
                for ii in range(1, self.quantity):
                    self.fout.write(partName + ".translate(Base.Vector(vertPosition))\n")
                    self.display_object(partName, self.colors[n], "outerTransparency", "Shaded")

        # End of if else construct


        # write out the text position
        self.fout.write('textPosition = ' + str(self.textPosition) + '\n')

        # call function to write out the text
        # self.fout.write('writeObjectText("' + self.name + '", ' + str(
        #     len(self.materials)) + ', ' + str(self.materials) + ', ' + str(self.quantity) + ', textPosition)\n')

        self.fout.write('writeObjectText("' + self.name + '", ' + str(
            len(self.materials)) + ', ' + str(self.materials) + ', ' + str(self.inns) + ', ' + str(
            self.quantity) + ', textPosition)\n')



# ===================================================================
# End of Sphere class
# ===================================================================





