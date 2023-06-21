# A .sh file for unzip the tar.gz files and rename the folders extracted

# Concate /media/tianyi/BSC-VideoCompletion/Archives/train_14409.tar.gz.partaa and /media/tianyi/BSC-VideoCompletion/Archives/train_14409.tar.gz.partab
cat train_14409.tar.gz.part* > train_144096.tar.gz

# Unzip the .tar.gz files
for f in *.tar.gz; do tar -xvzf "$f"; done

# After unzipping, rename the subfolder 'Annotations' as 'masks' in each extracted folders
for d in */; do mv "$d/Annotations" "$d/masks"; done
mv "./train_144096/JPEGImages" "./train_144906/GT_JPEGImages"

