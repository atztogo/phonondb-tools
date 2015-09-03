#!/bin/zsh

for i in {000..999};do 
    if [ `find d$i -name "*.lzma"|wc|awk '{print $1}'` -gt 0 ];then    
	cd d$i
	python ~/code/phonondb/phonondb/sphinx/make_rst.py $i
	cd ..
    fi
done

sphinx-build -b html . _build
