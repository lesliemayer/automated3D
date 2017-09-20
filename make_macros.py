"""Python code to write freeCAD macros to draw various shapes like boxes, cylinder, etc"""

from cylinder import CYLINDER
from box import BOX
from sphere import SPHERE

# constant for converting meters to millimeters
conM2mm = 1000.

# Define cylinder and make macro to draw it in FreeCAD

# Outer radii of the cylinder layers
outerRads = [.005, .004, .003]  # meters
# test to see what happens when negative
#outerRads = [.005, .004, -1.]

# convert to millmeters
outerRads = [x * conM2mm for x in outerRads]

innermostRad = 0.001 * conM2mm
# test to see what happens when innermostRad < 0
#innermostRad = -1

laero = .01 * conM2mm  # Length for aero
#laero = -1

haero = 0.0 # (not used for cylinders)

macroName = 'draw_layered_cylinder.FCMacro'

cyl = CYLINDER(innermostRad, outerRads, laero, haero, macroName)

# cyl.print_outerRads()
#
# cyl.print_innerSpaces()
#
# cyl.print_innermostRad()
#
# cyl.print_macroName()

# print the cyl object
print(cyl)

cyl.write_macro()

# ------------------------------------------------------
# Make a cylinder w/ 1 material, 0 inner radius
# ------------------------------------------------------

# Outer radii of the cylinder layers
outerRads = [2.0]  # meters  = 1/2 of the Width of the outer most box

innermostRad = 0.0

laero = 9.0  # Length for aero

macroName = 'draw_simple_cylinder.FCMacro'

cylSimple = CYLINDER(innermostRad, outerRads, laero,  haero, macroName)

# print the cyl object
print
print(cylSimple)

cylSimple.write_macro()

# ------------------------------------------------------
# Make a cylinder w/ 1 material, >0 inner radius
# ------------------------------------------------------

# Outer radii of the cylinder layers
outerRads = [4.0]  # meters

innermostRad = 1.0

laero = 5.0  # Length for aero

macroName = 'draw_simple2_cylinder.FCMacro'

cylSimple2 = CYLINDER(innermostRad, outerRads, laero,  haero, macroName)

# print the cyl object
print
print(cylSimple2)

cylSimple2.write_macro()

# ------------------------------------------------------
# Make a cylinder w/ 2 material, no inner radius
# ------------------------------------------------------
# Outer radii of the cylinder layers
outerRads = [4.0,2.0]  # meters

innermostRad = 0.0

laero = 15.0  # Length for aero

macroName = 'draw_2layer_cylinder.FCMacro'

cylLay2 = CYLINDER(innermostRad, outerRads, laero, haero, macroName)

# print the cyl object
print
print(cylLay2)

cylLay2.write_macro()

# -------------------
# Make a simple box
# -------------------
outerRads = [4.0]  # meters

innermostRad = 0.0

laero = 3.0  # Length for aero

haero = 8.0

macroName = 'draw_simple_box.FCMacro'

dirName = r'C:\Users\lrmayer\Documents\Mayer\WorkGroup\model\PythonCode'

box = BOX(innermostRad, outerRads, laero,  haero, macroName, dirName)

# print the cyl object
print
print(box)

box.write_macro()

# ----------------------------
# Make a simple box with hole
# ----------------------------
outerRads = [2.0]  # meters  1/2 of the outer Width

innermostRad = 1.0

laero = 3.0  # full Length for aero

haero = 8.0

macroName = 'draw_simple_box_hole.FCMacro'

dirName = r'C:\Users\lrmayer\Documents\Mayer\WorkGroup\model\PythonCode'

box = BOX(innermostRad, outerRads, laero,  haero, macroName, dirName)

# print the cyl object
print
print(box)

box.write_macro()

# ------------------------------------------------------
# Make a sphere w/ 2 material, no inner radius
# ------------------------------------------------------
# Outer radii of the cylinder layers
outerRads = [4.0,2.0]  # meters

innermostRad = 0.0

macroName = 'draw_2layer_sphere.FCMacro'

sphere0 = SPHERE(innermostRad, outerRads, laero,  haero, macroName)

# print the cyl object
print
print(sphere0)

sphere0.write_macro()
