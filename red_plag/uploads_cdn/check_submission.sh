#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 <tarfile>"
fi
tf=$1

ls_output=".:\nTask1-Integers\nTask2-GodSave\nTask3-CheckCode\nTask4-Music\nTask5-HiddenLore\n\n./Task1-Integers:\nroman.sh\nsum.sh\nsum_all.sh\n\n./Task2-GodSave:\ncipher.sh\n\n./Task3-CheckCode:\nverifier.sh\n\n./Task4-Music:\norganiser.sh\n\n./Task5-HiddenLore:\nstory.sh"

dir=${tf%.tar.gz}

tar -xf $tf && pushd $dir >/dev/null 2>/dev/null || { echo "Could not untar the directory"; exit 1; }

ls -1R >../o
diff -bBw ../o <( echo -e $ls_output ) >/dev/null && echo "Files in the right order. Do submit" || echo -e "Please maintain this structure- $ls_output" 
rm ../o
popd >/dev/null 2>/dev/null && rm -rf $dir
