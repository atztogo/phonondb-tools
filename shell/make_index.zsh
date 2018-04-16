#!/bin/zsh

for i in {000..999};do
  if [ `find d$i -name "*.png"|wc|awk '{print $1}'` -gt 0 ];then
    echo "   d$i/index" >> index.rst
  fi
done
