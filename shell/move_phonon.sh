#!/bin/zsh

for i in `cat id_nums.dat`;do
    d=`printf "%06d\n" $i|cut -c 1-3`
    echo $i $d

    mv mp-$i.tar.lzma ../www/d$d

    cp -a mp-$i/gruneisen.png ../www/d$d/mp-$i-gruneisen.png
    cp -a mp-$i/gruneisen-01/dos.png ../www/d$d/mp-$i-dos.png
    if [ -f mp-$i/qha.png ]; then
	cp -a mp-$i/qha.png ../www/d$d/mp-$i-qha.png
    fi

    if [ -f mp-$i/POSCAR-unitcell-mass.yaml ]; then
    	cp -a mp-$i/gruneisen-01/POSCAR-unitcell-mass.yaml ../www/d$d/mp-$i-POSCAR.yaml
    else
    	cp -a mp-$i/gruneisen-01/POSCAR-unitcell.yaml ../www/d$d/mp-$i-POSCAR.yaml
    fi

    ratio=`grep ratio mp-$i/gruneisen-01/imag_ratio.dat|awk '{print $2}'`
    if [ `echo "$ratio < 0.01"|bc` -eq 1 ]; then
	cp -a mp-$i/gruneisen-01/tprops.png ../www/d$d/mp-$i-tprops.png
    fi
done
