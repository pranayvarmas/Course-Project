#!/bin/bash
if [ $# -ne 3 ]; then
    echo "Usage: ./verifier.sh <source file> <testcases url> <cut-dirs arg>"
    exit 1
fi
file=$1
url=$2
cutdir=$3
wget --quiet -r -nH -R "index.html*" --cut-dirs=$cutdir --no-parent $url
cp $1 ./
name=$( basename $url )
if [ ! -d "./$name/my_outputs" ]; then
    mkdir ./$name/my_outputs
fi
g++ $1
for file in $( ls ./$name/inputs/ );
do
    if [ ${file: -3} == ".in" ]; then
        len=${#file}
        end=$(( $len - 3 ))
        out=$( echo $file | cut -c1-$end )
        out="$out.out"
        ./a.out < ./$name/inputs/$file > ./$name/my_outputs/$out
    fi
done
if [ ! -f "./feedback.txt" ];then
    touch feedback.txt
fi
echo "Failed testcases are:" > feedback.txt
count=0
for file in $( ls ./$name/outputs/ );
do
    my=$( cat ./$name/my_outputs/$file )
    test=$( cat ./$name/outputs/$file )
    if [ "$my" != "$test" ];then
        (( count++ ))
        len=${#file}
        end=$(( $len - 4 ))
        out=$( echo $file | cut -c1-$end )
        echo $out >> feedback.txt
    fi
done
if [ $count != 0 ]; then
    echo "Some testcases failed"
else
    echo "All testcases passed!"
fi
exit 0
