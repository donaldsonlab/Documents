```
I believe I resolved the issue with importing deeplabcut in the conda environment. It was related to the software's default behavior, which is to open up in GUI mode. This in turn causes issues with libraries that don't exist or are incompatible. Per page 7 of https://www.biorxiv.org/content/biorxiv/early/2018/11/24/476531.full.pdf, when you are running on a non-GUI environment like a university cluster, you can disable the GUI environment by setting the environment variable "DLClight=True" before running ipython. Here's an example of sourcing the DLCCPU environment, setting the environment variable, starting ipython, and loading deeplabcut:
 
[chdu9122@shas0137 ~]$ source /curc/sw/anaconda3/2019.03/bin/activate
(base) [chdu9122@shas0137 ~]$ conda activate DLCCPU
(DLCCPU) [chdu9122@shas0137 ~]$ export DLClight=True
(DLCCPU) [chdu9122@shas0137 ~]$ ipython
Python 3.6.7 | packaged by conda-forge | (default, Jul 2 2019, 02:18:42)
Type 'copyright', 'credits' or 'license' for more information
IPython 6.0.0 -- An enhanced Interactive Python. Type '?' for help.
 
In [1]: import deeplabcut
DLC loaded in light mode; you cannot use the relabeling GUI!
DLC loaded in light mode; you cannot use the labeling GUI!
```
