#!/bin/sh  

# Choose one path to compress videos
folder='./datasets/davis/BSCJPEGImages'
# folder='./datasets/youtube-vos/BSCJPEGImages'

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
