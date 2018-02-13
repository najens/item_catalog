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
Create and activate virtual environment
```
$ mkdir /virtualenvs
$ cd /virtualenvs
$ python3 -m venv item_catalog
$ source item_catalog/bin/activate
```
Install  moduledependencies
```
$ cd /vagrant
$ pip3 install -r requirements.txt

Create a virtual environment
```

## Run App
```
$ python3 run.py
```
