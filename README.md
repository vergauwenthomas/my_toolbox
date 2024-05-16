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



