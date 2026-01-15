#!/bin/bash
# declare -A cols
# declare -A nams
col1=( "#3fb3b2" "#aad400" "#ffcc00" "#ff2a2a" "#ffffff" )
col2=( "#ffffff" "#ffffff" "#ffffff" "#ffffff" "#999999" )
namc=( "turquoise" "yellowgreen" "gold" "red" "white" ) 
nami=( "chip" "cloud" "book" "robot" )
namf=( "main" "cloud" "training" "robot" ) 

mkdir ./tmp
mkdir -p ./shades/png

for i in "${!col1[@]}"
    do 
        fl_frame="tmp/frame_"${namc[$i]}".svg"
        sed -e "s/#37abc8/${col1[$i]}/" "frame.svg" > $fl_frame
        inkscape -w 1024 -h 1024 $fl_frame -o "${fl_frame%.svg}.png"
        for j in "${!nami[@]}" 
        do
            fl_part="tmp/"${nami[$j]}"_"${namc[$i]}".svg"
            fl_out="shades/png/"${namf[$j]}"_"${namc[$i]}".png"
            sed -e "s/#ffffff/${col2[$i]}/" ${nami[$j]}".svg" > $fl_part
            inkscape -w 248 -h 248 $fl_part -o "${fl_part%.svg}.png"
            echo "writig $fl_out"
            convert "${fl_frame%.svg}.png" "${fl_part%.svg}.png" -gravity center -geometry +31-5 -compose over -composite $fl_out
    done
done

rm -r ./tmp
