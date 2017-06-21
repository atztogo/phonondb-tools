#!/bin/zsh

#cp ~/code/phonondb/sphinx/{index.rst,about.rst,conf.py,webserver.jpg} .

sphinx-build -b html . _build
