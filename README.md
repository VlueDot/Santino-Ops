# Santino-Ops

## Project initialization 

```
nvm install 20
nvm use 20
pyenv install
pyenv local $(< .python-version)
npm install -g firebase-tools
firebase login
firebase init 
cd functions
python -m venv venv 
source venv/bin/activate
pip install nodeenv
nodeenv env
. env/bin/activate
nodeenv -p
pip freeze > requirements.txt 
freeze nrequirements.txt
```

## Project reinstall 

```
nvm install 20
nvm use 20
pyenv install
pyenv local $(< .python-version)
npm install -g firebase-tools
firebase login
cd functions
python -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
pip install --upgrade pip
nodeenv env
. env/bin/activate
nodeenv -p
nodeenv -r nrequirements.txt --update env 
```

## Initialize terminal
```
source venv/bin/activate
. env/bin/activate
nodeenv -p
```

## Emulate environment

