"""Code to compare run read_model_input,  to read an model input file and write
a FreeCAD python script to draw the objects in the model input file"""

import os
import sys

# directory where the code to run is
codeDir = os.environ['VIZAUTOCODE'] + '/'

sys.path.append(codeDir)


# model inputfile
modelIN = r'C:\Users\lrmayer\Documents\Mayer\WorkGroup\model\modelinputFiles/sample_6.in' # 1 sphere, w layers, hollow inside

#modelIN = codeDir+r'input.in'

print ("input file : {}".format(modelIN))

# where macro files are generated
macroOutDir = r'C:\Users\lrmayer\Documents\Mayer\WorkGroup\model\VizGeneratedMacros'
#macroOutDir = codeDir

# The input arguments to read_model_input
sys.argv = ['read_model_input.py', modelIN, macroOutDir]

try :
    # Run the test code to generate the macros
    execfile(codeDir+'read_model_input.py')
except :
     print("couldn't run "+codeDir+'read_model_input.py ' + modelIN)
     print("Unexpected error:", sys.exc_info()[0])
     raise

