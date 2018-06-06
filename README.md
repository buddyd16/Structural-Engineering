# Structural-Engineering
Structural Engineering Modules (Python 2.7 primarily)
Everything was developed using a standard install of the 2.7.10 version of Python XY which can be downloaded from here: https://python-xy.github.io/downloads.html

## Strap Beam - strap_beam_gui.py
Tkinter GUI based Python Program
requires the analysis folder and contained py files and the concrete folder and contained python files
Currently an alpa level program there are several validation checks not being performed such as numebr of bars required in the strap actually fitting in the strap, etc.

## Concrete T beam - depends on concrete_beam_classes in the same directory
Tkinter GUI based Python program.
Provides various code defined capacities based on strain compatibility. Currently based on ACI 318-08. Calculates elevation
of various steel reinf. layers based on clearance and spacing requirements per ACI 318-08.

## Concrete T Beam Any Steel - depends on concrete_beam_classes in the same directory
Tkinter GUI based Python program
Provides various code defined capacities based on strain compatibility. Allows for user assigned elevations of steel reinforcement
layers. Does not check or provide for min spacing of tension layer bars nor maximum amount of bars that fit in a layer.

## Simple Beam
Tkinter GUI based python program
can solve for shear, moment, slope, and deflection of a simply supported beam with cantilevers at either end. Can apply any combination of point, point moment, uniform line, or trapezoidal loadings. Will automatically generate results curves and has the ability to find values at a specific location. Recently added the ability to solve for redundant interior reactions, simply add the result as a point load to verify deflection returns to 0 at the designated location. Can export an 11x17 pdf plot showing applied loads, reactions, shear, moment, slope, and deflection.

Can be used to verify frame or fixed beam FEM results by applying point end moments returned by your 3rd party software, works on basis of superposition.

## Three Moment Method
### Reworking to use the pin-pin class file and directly compute slope and deflection rather than rely on approx. integration. Also adding in point moments as a load type.
Contains a class for the Three Moment Method for continuous beam analysis. Refer to the comments in the py file for additional information.

**finding some of my edits to the pin pin and simple beam file might create issues in the three moment method file, end user should be mindful of this and so some quick sanity checks on the results, cantilevers should be per the aisc manual and interior spans should be loading + end moment superposition. UDL and TRAP loads should trigger a manual verification, will be corrected in future versions.**

## Beam Patterning - depends on having the point and udl GIF files in same directory as the py file
### Reworking to use the external three moment method python file rather than the duplicate local function.
A Tkinter GUI based Python program implimenting IBC 2012 load combinations and load patterning. Analysis is done using the Three moment method. Results are displayed on screen and CSV and DXF files are created and placed in RESULTS folder on the users desktop. NOTE: When using the prescribed support displacement option the beam slope diagram and values are incorrect. Deflection values have been corrected using small angle approximations. The effect of the support displacement can be toggled on and off in the results window for shear, moment, slope and deflection charts. Limit to 8 spans or less, based on testing will run into a memory limit at 9 spans with patterning considered this is due to exponetial increase in number of patterns to solve and the results arrays generated.


## 14th Edition AISC Shapes Database - depends on having the excel file in the same directory as the py file
**This is in no way affiliated or endorsed in whole or in part by AISC this is a personal project being provided for anyone's general use at no cost.
A Tkinter GUI based Python program to sort and filter steel shapes built off the freely available excel file provided by AISC, https://www.aisc.org/publications/steel-construction-manual-resources/

#11.30.2017: AISC now offers the 15th edition as excel files

#11.30.2017: zip file in directory contains a compiled version for windows, no installation required simply run the .exe

## 14th Edition AISC Shapes Historic Database - depends on having the excel file in the same directory as the py file
**This is in no way affiliated or endorsed in whole or in part by AISC this is a personal project being provided for anyone's general use at no cost.
A Tkinter GUI based Python program to sort and filter historic steel shapes built off the freely available excel file provided by AISC, https://www.aisc.org/publications/steel-construction-manual-resources/

#11.30.2017: AISC now offers the 15th edition as excel files

#11.30.2017: zip file in directory contains a compiled version for windows, no installation required simply run the .exe

## Section Props - GUI
A Tkinter GUI based Python program implementing Green's Theorem on a set of user input vertex points. **Note: Scrutenize results where the defined shape centroid is 0,0 implemented a fix in the code but generally Sx or Sy is per I/x or y which would result in a divide by zero error if either coordinate of the centroid was at 0. The "fix" implemented takes the distance from the furthest vertex point in either the x or y direction for the claculation of Sx or Sy.

## Wood Classes
Currently only contains a method for wood stud walls. routine outside of the class will generate a P vs Lateral Pressure curve for a wall, generates a curver for each load duration factor. Also plots plate crushing with and without Cb and l/180, l/240, and l/360 cut off lines.

## Wood Stud Wall GUI - depends on having wood_classes.py in the same folder
a Tkinter graphical interface for the Wood Classes file - calculates stud wall capacities and shows pvm and pvpressure diagrams. Can take user loads and check against IBC 2012 load combinations, can also attempt to optimize wall stud spacing based on user input loads.
