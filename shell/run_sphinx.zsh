#!/bin/zsh

cp ~/code/phonondb/sphinx/{index.rst,about.rst,database-mp.rst,conf.py,webserver.jpg} .

for i in {000..999};do 
    if [ `find d$i -name "*.lzma"|wc|awk '{print $1}'` -gt 0 ];then    
	echo "   d$i/index" >> database-mp.rst
    fi
done

sphinx-build -b html . _build
