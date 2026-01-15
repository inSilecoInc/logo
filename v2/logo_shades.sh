#!/bin/bash
# declare -A cols
# declare -A nams
col1=( "#3FB3B2" "#AAD400" "#FFCC00" "#FF2A2A" "#FFFFFF" )
col2=( "#FFFFFF" "#FFFFFF" "#FFFFFF" "#FFFFFF" "#000000" )
namc=( "turquoise" "yellowgreen" "gold" "red" "white" ) 
nami=( "chip" "cloud" "book" "robot" )
namf=( "main" "cloud" "training" "robot" ) 

mkdir ./tmp

for i in "${!col1[@]}"
    do 
        sed -e "s/#37abc8/${col1[$i]}/" "frame.svg" > "tmp/frame_"${namc[$i]}".svg"
        for j in "${!nami[@]}" 
        do
            file_name="shades/"${namf[$j]}"_"${namc[$i]}".svg"
            echo "writing $file_name"
            sed -e "s/#37abc8/${col2[$I]}/" ${nami[$j]}".svg" > "tmp/"${nami[$j]}"_"${namc[$i]}".svg"
            echo '<svg xmlns="http://www.w3.org/2000/svg">' > $file_name
            echo '<g>' >> $file_name
            tail -n +2 "tmp/frame_"${namc[$i]}".svg" >> $file_name
            echo '</g>' >> $file_name
            echo '<g>' >> $file_name
            tail -n +2 "tmp/"${nami[$j]}"_"${namc[$i]}".svg" >> $file_name
            echo '</g>' >> $file_name
    done
done

#rm -r ./tmp