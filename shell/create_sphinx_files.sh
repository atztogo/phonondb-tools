#!/bin/zsh

# Run in ph20180417

for i in {000..999};do
  echo d$i
  # if [ `find d$i -name "*.lzma"|wc|awk '{print $1}'` -gt 0 ];then
  mkdir d$i
  cd d$i
  python ../make_rst.py $i
  cd ..
  # fi
done

#sphinx-build -b html . _build
