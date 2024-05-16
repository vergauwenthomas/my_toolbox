# my_toolbox
A handyman's toolbox for model output on ATOS. This is a collection of simple analysis tools, that are easely accesible by cli. 
The backend are epygram scripts with an argparser, for which aliases are written in the .bashrc


## How to use?
Activate the (epygram) environment by

```
activate_toolbox
```

## Tools
Here a small description of the present tools

### What ??
This tools prints out the details of the content of an output-file. It take only the file (filename, or filepath) as argument.

```
what ELSCFDEODALBC005
```
Or pipe the output to a log file

```
what ELSCFDEODALBC005 > what_output.log
```

### plot_me
This tool makes simple plots of FA outputfiles. Create a plot by runnin `plot_me <filename> <fieldname>'. 
For more details run the `plot_me -h`.

```
[cu1c@aa6-100 ~]$ plot_me -h
usage: plot_me [-h] [-f FIELDNAME] [-l LEVEL] [--backend BACKEND] file

plot_me: a simple plotting tool for FA files using Epygram
--------------------------------------------------------

The following functionality is available:
    * -f, --fieldname (make as spatial plot of this 2D field.)
    * -l, --level(print out information of a FA file.)
    * --backend (Qt5,  agg, ... )
    

positional arguments:
  file                  FA filename, path of FA file or similar regex expression on filenames.

optional arguments:
  -h, --help            show this help message and exit
  -f FIELDNAME, --fieldname FIELDNAME
                        Make as spatial plot of this 2D field (identifier can contain regex but must point to unique fieldname).
  -l LEVEL, --level LEVEL
                        The level of the field, if None, the lowest level is plotted
  --backend BACKEND     The plotting backend for cartoplot/mpl (use Qt5 for interactive --> needs Qt5 module)

                                                @Thomas Vergauwen (thomas.vergauwen@meteo.be), credits to the Epygram-team. 
[cu1c@aa6-100 ~]$ 

```



