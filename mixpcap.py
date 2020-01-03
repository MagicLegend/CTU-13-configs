#!/home/magiclegend/anaconda3/bin/python

import pandas as pd
import math
import os
import re
import argparse
pd.options.mode.chained_assignment = None  # default='warn' https://stackoverflow.com/a/20627316

# /mnt/hgfs/Datasets/ISCX-Bot-2014
# ISCX_Botnet-Testing.argus.netflow.labeled
def isBotnet(row):
    if not pd.isna(row['Label']):
        if 'botnet' in row['Label'] or 'Botnet' in row['Label']:
            # print("Botnet row")
            return 1
        else:
            return 0
    else:
        return 0

def mixTraffic(df, ratio=5):
    """Takes single dataframe, and re-distributes the content to a 1:x botnet:non-botnet traffic ratio.
    
    Arguments:
        df {pd.DataFrame} -- Dataframe to process.
    
    Keyword Arguments:
        ratio {int} -- Ratio in which the botnet:non-botnet traffic should be distributed. (default: {5})
    
    Returns:
        pd.DataFrame -- Processed dataframe.
    """
    # Randomly select just as much non-botnet rows as there are botnet rows to create a 1:1 ratio
    counts = df['isBotnet'].value_counts().to_dict()
    print(counts)
    # df_reduced = df[df.isBotnet != 1].sample(counts[1])
    df_reduced = df[df.isBotnet != 1].sample(counts[1] * ratio, random_state=1337)
    
    df_pure_botnet = df[df.isBotnet == 1]
    # Concat the random traffic with the pure botnet traffic; and sort the dataframe
    df_concatted = pd.concat([df_reduced, df_pure_botnet])
    df_concatted = df_concatted.sort_values(by='StartTime')

    return df_concatted

def main():
    print("Searching for dataset at: " + args.path)

    if (os.path.isfile(args.path)):
        print("Reworking dataset...")
        dataframe = pd.read_csv(args.path, index_col='StartTime')
        print("Applying column")
        # dataframe['isBotnet'] = dataframe.apply(lambda x: isBotnet(x), axis=1)
        dataframe['isBotnet'] = dataframe.apply(isBotnet, axis=1)
        print("Mixing traffic")
        dataframe = mixTraffic(dataframe)
        print("Saving new csv")
        true_path, filename = os.path.split(args.path)
        tmp = filename.split('.')
        new_filename = tmp[0] + ".reworked." + tmp[3] + "." + tmp[4]
        # new_filename = tmp[0] + ".reworkedv2." + tmp[2] + "." + tmp[3]
        print("New filename: " + true_path + "/" + new_filename)
        dataframe.to_csv(true_path + "/" + new_filename, index=True)
        print("Done")

parser = argparse.ArgumentParser("prepare_dataset.py")
parser.add_argument("path", help="The file that should be processed.", type=str)
args = parser.parse_args()

main()