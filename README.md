# my_toolbox
A handyman's toolbox for model output. This is a collection of simple analysis tools, that are easely accesible by cli. 

The toolbox is feature-based, so the functionallity and dependecies will vary over time.

# How to install 

Clone this repo, use poetry to install the package and dependencies. If you install the toolbox on a server/hpc, you can write an setup script (see the `setup_env/atos.sh' script as exaple.)


## Add aliasses
I found it handy to add the toolbox to your bashrc. You can do it by adding this to your `.bashrc`

```
toolboxdir=${HOME}/software/my_toolbox
alias activate_toolbox="source ${toolboxdir}/setup_env/atos.sh"
alias toolbox="python3 ${toolboxdir}/toolbox "${@: -1}""

```

Update the path to the `toolboxdir` for your setup! 

# Usage
You can run the toolbox using `poetry run pyhon toolbox` from the root folder of this repo. 
If you have added the toolbox to your `.bashrc` as described above, use the toolbox you start by running `activate_toolbox` and to use it, just call `toolbox`.


```
(toolbox-py3.10) [cu1c@aa6-102 ~]$ toolbox -h
usage: toolbox [-h] {diff,explain,Update_defenitions,what,plot} ...

A toolbox for working with NWP/Climate model output.
--------------------------------------------------------

 Note: The used defenitions are define in this online sheet: https://docs.google.com/spreadsheets/d/1qvwju807GBhnCQ5TOdgdqjIMPUWumCi9dEs1XwYfjvU/edit?usp=sharing
    

positional arguments:
  {diff,explain,Update_defenitions,what,plot}
                        sub-commands help
    diff                Print out the difference between two namelist.
    explain             Print out the namelist and explain the settings.
    Update_defenitions  Update the local copy of the namelist defenitions from the online google sheet.
    what                Print out an overview of an FA file (using PyFa as backend).
    plot                Make a 2D plot of a field of an FA file.

options:
  -h, --help            show this help message and exit

toolbox version: 0.1.0a


```

For more details on a specific tool, specify the tool and add `-h` as argument:

```

(toolbox-py3.10) [cu1c@aa6-102 ~]$ toolbox plot -h
usage: toolbox plot [-h] [--reproj] [--trg_crs TRG_CRS] file fieldname

positional arguments:
  file               filename, path or similar regex expression of the FA file to explain.
  fieldname          The name of the field to plot.

options:
  -h, --help         show this help message and exit
  --reproj           If this argument is added, the output field is reprojected to trg_crs.
  --trg_crs TRG_CRS  The target CRS (in epsg) to reproject to. If "epsg:4326" then landfeatures are added to the plot.

```


