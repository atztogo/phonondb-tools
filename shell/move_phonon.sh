#!/bin/zsh

for i in `cat id_nums.dat`;do
    d=`printf "%06d\n" $i|cut -c 1-3`
    echo $i $d

    mv mp-$i.tar.lzma ../www/d$d

    cp -a mp-$i/dos.png ../www/d$d/mp-$i-dos.png

    if [ -f mp-$i/POSCAR-unitcell-mass.yaml ]; then
    	cp -a mp-$i/POSCAR-unitcell-mass.yaml ../www/d$d/mp-$i-POSCAR.yaml
    else
    	cp -a mp-$i/POSCAR-unitcell.yaml ../www/d$d/mp-$i-POSCAR.yaml
    fi

    ratio=`grep ratio mp-$i/imag_ratio.dat|awk '{print $2}'`
    if [ `echo "$ratio < 0.01"|bc` -eq 1 ]; then
	cp -a mp-$i/tprops.png ../www/d$d/mp-$i-tprops.png
    fi
done
