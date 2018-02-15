# item_catalog

item_catalog is a simple python flask app that allows users to perform basic crud operations on categories and items in a catalog database.

## Software Requirements

- [Git or Git Bash](https://git-scm.com/downloads)
- [Vagrant 2.0.1](https://releases.hashicorp.com/vagrant/2.0.1/)
- [Virtualbox 5.1.30](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)

## Installation Instructions

Open Git or Git Bash in your workspace directory

Clone the GitHub repository
```
$ git clone https://github.com/najens/item_catalog.git
```
Navigate to project folder
```
$ cd item_catalog
```
Create and Configure Virtual Machine
```
$ vagrant up
```
Sign in to Virtual Machine
```
$ vagrant ssh

# If you have trouble signing in export the
# following environment variable and try again

$ export VAGRANT_PREFER_SYSTEM_BIN=1
```
Create and activate virtual environment
```
$ sudo su
$ mkdir /.virtualenvs
$ cd /virtualenvs
$ python3 -m venv item_catalog
$ source item_catalog/bin/activate
```
Upgrade pip3
```
$ pip3 install --upgrade pip
```
Install Module Dependencies
```
$ cd /vagrant
$ pip3 install -r requirements.txt
```
Export insecure transport environment variable to use with http on localhost
```
export OAUTHLIB_INSECURE_TRANSPORT=1
```
## Run App
```
$ python3 run.py
```
Open app in browser at http://localhost:5000
