# Structural-Engineering
Structural Engineering Modules (Python 2.7 primarily)
Everything was developed using a standard intall the 2.7.10 version of Pyhton XY which can be downloaded from here: https://python-xy.github.io/downloads.html

## Concrete T beam - depends on concrete_beam_classes in the same directory
Tkinter GUI based Python program.
Provides various code defined capacities based on strain compatibility. Currently based on ACI 318-08. Calculates elevation
of various steel reinf. layers based on clearance and spacing requirements per ACI 318-08.

## Concrete T Beam Any Steel - depends on concrete_beam_classes in the same directory
Tkinter GUI based Python program
Provides various code defined capacities based on strain compatibility. Allows for user assigned elevations of steel reinforcement
layers. Does not check or provide for min spacing of tension layer bars nor maximum amount of bars that fit in a layer.

## Three Moment Method
Contains a class for the Three Moment Method for continuous beam analysis. Refer to the comments in the py file for additional information.

## Beam Patterning - depends on having the point and udl GIF files in same directory as the py file
A Tkinter GUI based Python program implimenting IBC 2012 load combinations and load patterning. Analysis is done using the Three moment method. Results are displayed on screen and CSV and DXF files are created and placed in RESULTS folder on the users desktop. NOTE: When using the prescribed support displacement option the beam slope diagram and values are incorrect. Deflection values have been corrected using small angle approximations. The effect of the support displacement can be toggled on and off in the results window for shear, moment, slope and deflection charts. Limit to 8 spans or less, based on testing will run into a memory limit at 9 spans with patterning considered this is due to exponetial increase in number of patterns to solve and the results arrays generated.

## ASIC Shapes Database - depends on having the excel file in the same directory as the py file
A Tkinter GUI based Python program to sort and filter steel shapes built off the freely available excel file provided by AISC, https://www.aisc.org/publications/steel-construction-manual-resources/

## ASIC Shapes Historic Database - depends on having the excel file in the same directory as the py file
A Tkinter GUI based Python program to sort and filter historic steel shapes built off the freely available excel file provided by AISC, https://www.aisc.org/publications/steel-construction-manual-resources/

## Section Props - GUI
A Tkinter GUI based Python program implementing Green's Theorem on a set of user input vertex points. **Note: Scrutenize results where the defined shape centroid is 0,0 implemented a fix in the code but generally Sx or Sy is per I/x or y which would result in a divide by zero error if either coordinate of the centroid was at 0. The "fix" implemented takes the distance from the furthest vertex point in either the x or y direction for the claculation of Sx or Sy.
