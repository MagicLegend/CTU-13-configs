#!/bin/bash

folder=$1
file=$2

echo "Going for" $folder$file
echo "Assuming config files present in folder" $folder
# echo "Assuming slash appended to" $folder
# echo "Assuming no .pcap extension on " $file


if [ ! "${folder: -1}" == "/" ]; then
	echo "No slash present"
	echo "${folder: 10}"
	echo "${folder: -1}"
	folder+="/"
	echo $folder
fi

if [ "${file: -5}" == ".pcap" ]; then
	echo ".pcap present"
	# tmp=$file
	file=${file::-5}
	echo $file
fi

# Argus
echo "Running Argus..."
echo "$folder$file.argus"
argus -F "${folder}argus_bi.conf" -r $folder$file.pcap -w $folder$file.argus

echo "Running ralabel..."
ralabel -f "${folder}ralabel.conf" -r $folder$file.argus -w $folder$file.argus.labeled

echo "Cleaning $file.argus"
rm -f $folder$file.argus

echo "Running ra..."
ra -F "${folder}ra.conf" -Z b -nr $folder$file.argus.labeled > $folder$file.argus.netflow.labeled

echo "Cleaning $file.argus.labeled"
rm -f $folder$file.argus.labeled

echo "Done!"
