echo [$(date)]: "START"


echo [$(date)]: "Creating env with python 3.12 version"

conda create --prefix ./env python=3.12 -y

echo [$(date)]: "Activating the environment"

source activate ./env

echo [$(date)]: "Installing the dev requirements"

pip install -r requirements_dev.txt


echo [$(date)]: "END"

# Commands on terminal
# bash init_setup.sh
