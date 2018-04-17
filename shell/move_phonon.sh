#!/bin/zsh
data_dir="../../phonon-run"
www_dir="."
for i in `cat $data_dir/mp-list-phonon-succeeded.dat|sed s/mp-//`;do
  d=`printf "%06d\n" $i|cut -c 1-3`
  echo $i $d

  # mv mp-$i.tar.lzma ../www/d$d

  if [ -f $data_dir/mp-$i/dos.png ]; then
    cp -a $data_dir/mp-$i/dos.png $www_dir/d$d/mp-$i-dos.png
  fi

  if [ -f $data_dir/mp-$i/band.png ]; then
    cp -a $data_dir/mp-$i/band.png $www_dir/d$d/mp-$i-band.png
  fi

  if [ -f $data_dir/mp-$i/tprops.png ]; then
    cp -a $data_dir/mp-$i/tprops.png $www_dir/d$d/mp-$i-tprops.png
  fi
done
