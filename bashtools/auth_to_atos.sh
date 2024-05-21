#!bin/bash

#installing python version of teleport
#installation of teleport
module purge

module load Python/3.7.4-GCCcore-8.3.0


FILE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )




#1. Donwload and install teleport

#cd ${HOME}/fileserver/home
#wget https://cdn.teleport.dev/teleport-v11.1.4-linux-amd64-bin.tar.gz
#mv teleport-v11.1.4-linux-amd64-bin.tar.gz software/teleport.tar.gz
#cd software
#tar -xvzf teleport.tar.gz

#2 Set teleport in PATH
cd ${FILE_DIR}


export PATH=${PATH}:${HOME}/fileserver/home/software/teleport



#3. Installation of python teleport (to avoid browser and X11)

#export PATH=${PATH}:/users/thvergau/teleport
#which python
#   /opt/cray/pe/python/3.9.12.1/bin/python


#pip3 install teleport-browserless-login --user -U -i https://get.ecmwf.int/repository/pypi-all/simple
#pip3 install teleport-browserless-login[certificates-check] --user -U -i https://get.ecmwf.int/repository/pypi-all/simple



#4. Launching teleport
teleport-login -f --configuration ${FILE_DIR}/secrets.yml


cd ${FILE_DIR}
