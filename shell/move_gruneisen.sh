#!/bin/zsh

for i in `cat id_nums.dat`;do
    d=`printf "%06d\n" $i|cut -c 1-3`
    echo $i $d

    mv mp-$i-gruneisen.tar.lzma ../../www/d$d

    cp -a mp-$i-gruneisen/gruneisen.png ../../www/d$d/mp-$i-gruneisen.png

done
