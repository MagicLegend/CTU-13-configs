# CTU-13-configs
This repo contains two custom script that attempt to re-create the CTU-13 binetflow files.

# `pcap2binetflow.sh`

This shell script takes two arguments; the folder and the filename of the pcap. It then executes the three commands nessicary to generate binetflow files. Example configs are provided in `11.dataset-52/`.

# `mixpcap.py`

This python script (requires a python3 conda environment) takes a binetflow file (which is a csv file) and adds the `isBotnet` column to it. This binary value is then used by the classifier later to determine if a flow is possibly from a botnet or not. This script also pre-mixes the traffic, taking 5 background flows for every botnet flow; effectively creating a `1:5` ratio. This is done for better training, because otherwise the classifier will be trained on background traffic because of the bad ratios.
