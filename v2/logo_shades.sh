#!/bin/bash
# declare -A cols
# declare -A nams
cols=( "#3FB3B2" "#AAD400" "#FFCC00" "#FF2A2A" "#FFFFFF" )
nams=( "turquoise" "yellowgreen" "gold" "red" "white" ) 

for f in "main" "cloud"
do 
    for i in "${!cols[@]}"
    do 
        sed -e "s/#37abc8/${cols[$i]}/" "$f.svg" > "shades/$f"_"${nams[$i]}.svg"
    done
done

