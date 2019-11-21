# nanotools

Useful code for our NanoTools project at NTNU

### BasicXYplotter
This script reads .xy files and plots them using matplotlib. The function Plot is the main thingy here; Plot uses the other functions Reader and Averager to read files, plot the average CPS-values(if the .xy files contain multiple scans).

MultiPlot is also useful to plot multiple files in one plot, with different preferences regarding UPS and/or XPS scans/plots

Some details are to be found as comments in each function. These details will be updated and improved in the time to come.

The function, getImages saves images of multiple scans from multiple folders on your computer. As it is right now, this is not really modular, but you can understand most of what's going and adapt it to your structure.


### xpsplot2
This is mostly adapted from https://github.com/gVallverdu/xpsplot
Some typos have been fixed, as well as some minor adjustments due to preferations.
