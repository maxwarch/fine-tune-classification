#!/bin/bash

# Update package list
sudo apt update

# Install pip if not already installed
sudo apt install -y python3-pip

# Install virtualenv
pip3 install virtualenv

# Create a virtual environment named 'env'
virtualenv env

# Activate the virtual environment
source env/bin/activate

# Install packages from requirements.txt
pip install -r requirements.txt