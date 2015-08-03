#!/bin/zsh

cp ./_main/index.rst .
cp ./_main/database-mp.rst .
cp ./_main/conf.py .

for i in {000..999};do 
    if [ `find d$i -name "*.lzma"|wc|awk '{print $1}'` -gt 0 ];then    
	echo "   d$i/index" >> database-mp.rst
    fi
done

sphinx-build -b html . _build
