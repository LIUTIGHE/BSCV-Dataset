#!/bin/sh  

# Choose one path to compress videos
# folder='./datasets/youtube-vos/BSC_JPEGImages'
# folder='./datasets/youtube-vos/GT_JPEGImages'

for file in $folder/*
  do
      if test -f $file
      then
          echo $file is file
      else
          echo compressing \"$file\" ...
          zip -q -r -j $file.zip $file/
          rm -rf $file/
      fi
  done

echo 'Done!'
