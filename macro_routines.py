""""Write header for FreeCAD macro document"""

import logging

def make_macro_header(leftXX, bottomYY, fout):

    # Append the visualization library to the pythonpath so can use its functions
    fout.write("import sys\n")  # for appending path
    fout.write("import os\n")  # for using environment variables
    #fout.write("sys.path.append(r'C:\Users\lrmayer\Documents\Mayer\WorkGroup\model\VizLibrary')\n")
    fout.write("print 'VIZLIBRARY = ' + os.environ['VIZLIBRARY']\n")
    fout.write("sys.path.append(os.environ['VIZLIBRARY'])\n")

    # Print out the font file
    fout.write("print 'VIZFONTFILE = ' + os.environ['VIZFONTFILE']\n")

    fout.write("import Part, Draft\n")
    fout.write("from FreeCAD import Base\n")
    fout.write("import FreeCADGui\n")

    # for writeObjectText function:
    fout.write("from vizlibrary import writeObjectText\n")

    # where to start 1st object in X direction
    fout.write("leftXX = " + str(leftXX) + "\n")

    # Y line where bottom of objects lines up
    fout.write("bottomYY = " + str(bottomYY) + "\n")

    # These have to be float values
    fout.write("yellowgreen = (154./255.,205./255.,0.)\n")
    fout.write("black = (0., 0., 0.)\n")
    fout.write("white = (1.,1.,1.)\n")
    fout.write("deepskyblue	= (0.,191./255.,255./255.)\n")
    fout.write("darkgoldenrod =	(184./255.,134./255.,11./255.)\n")
    fout.write("yellow	= (1.,1.,0.)\n")
    fout.write("red = (1.,0.,0.)\n")
    fout.write("darkgray = (169./255.,169./255.,169./255.)\n")

    # Create the document
    fout.write("myDoc = FreeCAD.newDocument('Parent')\n")

    # Set the transparency for hollow insides
    # Don't make too large, makes inner white sphere look like the color of the outer sphere
    fout.write("hollowTransparency = 40\n")

    # Set outer shell transparency
    fout.write("outerTransparency = 70\n")

    # DON'T NEED TO WRITE TO MACRO
    # Set the minimum width between objects
    #fout.write("minWidth = 25\n")
    #fout.write("minWidth = 30\n")

    # Define the planes
    fout.write("xy = Base.Vector(0, 0, 1)\n")
    fout.write("xz = Base.Vector(0, 1, 0)\n")
    fout.write("yz = Base.Vector(1, 0, 0)\n")

    fout.write("\n")

    return



"""Write closing freecad statements"""
def make_macro_tail(fout):

    logging.debug("make_macro_tail : writing..........")

    fout.write('\n')

    # Need to activate the workbench so grid shows up
    # default workbench is "Start"
    fout.write('FreeCADGui.activateWorkbench("DraftWorkbench")\n')

    # Draft.setParam("gridSpacing",q.Value)
    fout.write('if hasattr(FreeCADGui, "Snapper"):\n')
    fout.write('   FreeCADGui.Snapper.setGrid()\n')

    fout.write('Gui.SendMsgToActiveView("ViewFit")\n')
    # comment out to initial view in the XY plane
    # Gui.activeDocument().activeView().viewAxonometric()

    fout.close()

    return



"""Calculate the position of the object"""
def calc_grid_position(bottomYY, prevPosition, prevRadius, currentRadius, currentLength) :

    logging.debug("calc_position : currentRadius = %s", currentRadius)
    logging.debug("calc_position : currentLength = %s", currentLength)

    minWidth = 50.  # minimum width b/t objects

    # Calculate the space between the 2 objects
    spaceWidth = currentRadius + prevRadius   # average the 2 radii to get the width b/t objects (2*cR + 2* pR)/2

    # Make sure there is a minimum of space between the 2 objects
    if spaceWidth < minWidth :
        spaceWidth = minWidth



    logging.debug("calc_position : spaceWidth = %s", spaceWidth)

    # Width from previous grid position to new grid position
    totalWidth = spaceWidth + 2.0*prevRadius

    gridPosition = (totalWidth + prevPosition[0], bottomYY, 0.)

    return gridPosition



