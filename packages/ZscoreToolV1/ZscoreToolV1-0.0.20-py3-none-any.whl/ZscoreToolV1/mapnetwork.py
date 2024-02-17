##!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 12:35:34 2023

@author: jan
"""

#%% import necessary tools
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
import tifffile as tiff
from tqdm import tqdm
from scipy import ndimage
#import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import os
from PIL import Image


#%%
def calculate_block_sums(df_block, r):
    points = df_block[['x', 'y']].values
    tree = cKDTree(points)
    block_sums = []

    # Create a tqdm progress bar
    progress_bar = tqdm(total=len(df_block), desc='Calculating Block Sums', position=0, leave=True)

    for i, (x, y) in enumerate(points):
        indices = tree.query_ball_point([x, y], r)
        block_sum = np.sum(df_block['mean'].iloc[indices])
        block_sums.append(block_sum)

        # Update the progress bar
        progress_bar.update(1)

    # Close the progress bar
    progress_bar.close()

    return block_sums

#%%
def make_images(singlenuc_sample, spatial_sample, overlap, block_size, r, mode, inputvalue, fill, method, outputimageformat):
    
    # make output folders
    if not os.path.isdir('./Results/02. Images/' + spatial_sample):
        os.mkdir('./Results/02. Images/' + spatial_sample)
    if not os.path.isdir('./Results/02. Images/' + spatial_sample + '/clusters/'):
        os.mkdir('./Results/02. Images/' + spatial_sample + '/clusters/')
    if not os.path.isdir('./Results/02. Images/' + spatial_sample + '/genes/'):
        os.mkdir('./Results/02. Images/' + spatial_sample + '/genes/')
        
    
    # Load the stereoseq CSV file (gem file) into a Pandas DataFrame
    print("Load spatial data")
    if method=='stereoseq':
        # CTR and FTD
        csv_file = '/Users/emma/OneDrive - Karolinska Institutet/2. Postdoc KI/1. ALS-FTD project/FTD-GRN/Stereoseq_109/outputfiles/EGE1_output/' + spatial_sample + '_tissue_cleaned.csv'
        df = pd.read_csv(csv_file)
        # male 1
        #csv_file = '/Users/emma/OneDrive - Karolinska Institutet/2. Postdoc KI/4. Human stereoseq/DATA/GEM files/bgi/' + spatial_sample + '.txt'
        #df = pd.read_csv(csv_file, sep='\t')
        #df = df.rename(columns={'MIDCounts': 'MIDCount'})
        #df['bin1_ID'] = df.index
        # AD
        #csv_file = '/Users/emma/OneDrive - Karolinska Institutet/2. Postdoc KI/4. Human stereoseq/Manual tissue selection/outputfiles/EGE2_output/' + spatial_sample + '_bin_coordinates_tissue.csv'
        #df = pd.read_csv(csv_file, sep=',')
        
        if spatial_sample=='2000-018_GFM_SS200000838BL_A6':
            tmp = pd.read_csv("./Tests/Expression under mask/WeirdGenesCTR018.csv", sep=';')
            df = df[~df['geneID'].isin(tmp[tmp.iloc[:, 1] == 'remove'].iloc[:,0])]
        
        # extend gemfile
        print("Expanding gemfile")
        count_numbers = df['MIDCount'].unique()
        df_keep = df[df['MIDCount'] == 1]
        for i in count_numbers[count_numbers > 1]:
            print(i)
            df_ext = df[df['MIDCount'] == i]
            df_ext = pd.concat([df_ext] * i, ignore_index=True)
            df_keep = pd.concat([df_keep, df_ext], ignore_index=True)
        df = df_keep  
        del df_keep
        del df_ext
        df['MIDCount'] = 1
        
        
    if method=='merfish':
        df = pd.read_csv('/Users/emma/OneDrive - Karolinska Institutet/2. Postdoc KI/Other/Fang et al. 2022 MERFISH/DATA/' + spatial_sample + '.barcodes.csv')
        df['bin1_ID'] = df.index
        df = df.drop(columns=df.columns[[0,1, 5, 6]])
        df.columns = ['geneID', 'x', 'y', 'bin1_ID']
        df['MIDCount'] = 1
        df['x'] = df['x'] - df['x'].min()
        df['y'] = df['y'] - df['y'].min()
    if method=='allen-merfish':
        df = pd.read_csv('/Users/emma/OneDrive - Karolinska Institutet/2. Postdoc KI/Other/Allen SEA-AD Merfish/middle-temporal-gyrus/' + spatial_sample.split('_')[0] + '/' + spatial_sample.split('_')[1] + '/cellpose-detected_transcripts.csv')
        df['bin1_ID'] = df.index
        df = df.drop(columns=df.columns[[0,1,2,3,4,7,9,10]])
        df['MIDCount'] = 1
        df = df.rename(columns={'gene': 'geneID'})
    if method=='xenium':
        csv_file = '/Users/emma/OneDrive - Karolinska Institutet/2. Postdoc KI/Other/10x/' + spatial_sample + '_outs/transcripts.csv'
        df = pd.read_csv(csv_file)
        df = df.drop(columns=df.columns[[1, 2, 6, 7, 8,9]])
        df.columns = ['bin1_ID','geneID', 'x', 'y']
        df['MIDCount'] = 1   
    
    if mode=='cluster':
        # Load the single nuc z-score file (output from script 01) into a Pandas DataFrame
        print("Load z-scores for cluster " + inputvalue)
        csv_file = '/Users/emma/Library/CloudStorage/OneDrive-KarolinskaInstitutet/2. Postdoc KI/13. Zscore paper/Analysis/Results/01. Zscores/' + singlenuc_sample + '/Cluster' + inputvalue + '.csv'
        zf = pd.read_csv(csv_file)
        zf.columns = ['geneID', 'mean', 'sum'] 
        # merge the zscores (zf) with the DNB data (df) 
        df=df.merge(zf, how='inner', on='geneID') 
        
    if mode=='gene':
        # Load the single nuc z-score file (output from script 01) into a Pandas DataFrame
        print("Load z-scores for gene " + inputvalue)
        csv_file = '/Users/emma/Library/CloudStorage/OneDrive-KarolinskaInstitutet/2. Postdoc KI/13. Zscore paper/Analysis/Results/01. Zscores/' + singlenuc_sample + '/res_zscore.csv'
        zf = pd.read_csv(csv_file)
        zf = zf.loc[zf["features"] == inputvalue].T.tail(-1)  ## or take the column??
        zf['geneID'] = zf.index
        zf.columns = ['mean', 'geneID'] 
        # merge the zscores (zf) with the DNB data (df)
        df=df.merge(zf, how='inner', on='geneID') 

    df = df[['x', 'y', 'bin1_ID', 'MIDCount', 'geneID', 'mean']] ###new

    # set the blocks
    full_width= int(round(df['x'].max(), 0))
    full_height= int(round(df['y'].max(), 0))
    result_df = pd.DataFrame(columns=['x', 'y', 'bin1_ID', 'geneID', 'MIDCount', 'block_sum'])
    block_results = []

    for x_start in range(0, full_width, block_size):
        x_end = min(x_start + block_size, full_width)
        for y_start in range(0, full_height, block_size):
            y_end = min(y_start + block_size, full_height)

            # Extract the block DataFrame
            block_df = df[
                (df['x'] >= x_start - overlap) & (df['x'] < x_end + overlap) &
                (df['y'] >= y_start - overlap) & (df['y'] < y_end + overlap)
                ]
        
            print("Processing block at x_start:", x_start, "y_start:", y_start)
        
            # Calculate block sums
            block_sums = calculate_block_sums(block_df,r)

            # Create a DataFrame with 'x', 'y', and 'block_sum'
            block_result_df = pd.DataFrame({'x': block_df['x'], 'y': block_df['y'], 'bin1_ID': block_df['bin1_ID'], 'geneID': block_df['geneID'], 'MIDCount': block_df['MIDCount'], 'block_sum': block_sums})

            # Append block results to the block_results list
            block_results.append(block_result_df)

    # Concatenate all block results into the final result DataFrame
    result_df = pd.concat(block_results, ignore_index=True)
    
    # aggregate by bin1_ID
    result_df2 = pd.DataFrame(result_df.groupby(by=["bin1_ID"])["block_sum"].sum()) ## or product?
    result_df2['bin1_ID'] = result_df2.index
    result_df2 = result_df2.reset_index(drop=True)
    result_df = result_df2.merge(result_df[["bin1_ID", "x", "y", "geneID", "MIDCount"]], on = "bin1_ID", how = "inner")
    result_df = result_df.drop_duplicates()

    if outputimageformat=='tiff':  
    # create a new image 
        print("Create tiff image")
        new_image = np.zeros((full_height+1, full_width+1, 3), dtype=np.uint8)
        max_sum = result_df['block_sum'].max()
        min_sum = result_df['block_sum'].min()*-1

        normalized_values = result_df['block_sum'].values
        x_values = result_df['x'].astype(int).values
        y_values = result_df['y'].astype(int).values

        # Positive and negative values separation
        positive_mask = normalized_values >= 0
        negative_mask = ~positive_mask
        positive_values = normalized_values[positive_mask]
        negative_values = -normalized_values[negative_mask]

        # Calculate values for green and blue channels
        new_image[y_values[positive_mask], x_values[positive_mask], 1] = (positive_values * (255 / max_sum)).astype(int)
        new_image[y_values[negative_mask], x_values[negative_mask], 2] = (negative_values * (255 / min_sum)).astype(int)

        # Save or display the image
        if mode=='cluster':
            tiff.imsave('./Results/02. Images/' + spatial_sample + '/clusters/cluster' + inputvalue + '_from_' + singlenuc_sample + '_mean_r' + str(r) + '.tif', new_image)
        if mode=='gene':
            tiff.imsave('./Results/02. Images/' + spatial_sample + '/genes/' + inputvalue + '_from_' + singlenuc_sample + '_mean_r' + str(r) + '.tif', new_image)

        if fill==True:
            # Create a mask for zero pixels
            print("Create filled image")
            zero_mask = (new_image == 0)
            avg_blue = ndimage.convolve(new_image[:, :, 0], np.ones((3, 3)) / 9, mode='constant', cval=0)
            avg_green = ndimage.convolve(new_image[:, :, 1], np.ones((3, 3)) / 9, mode='constant', cval=0)
            new_image[:, :, 0][zero_mask[:, :, 0]] = avg_blue[zero_mask[:, :, 0]]
            new_image[:, :, 1][zero_mask[:, :, 1]] = avg_green[zero_mask[:, :, 1]]

            # Save or display the image
            if mode=='cluster':
                tiff.imsave('./Results/02. Images/' + spatial_sample + '/clusters/cluster' + inputvalue + '_from_' + singlenuc_sample + '_mean_fill_r' + str(r) + '.tif', new_image)
            if mode=='gene':
                tiff.imsave('./Results/02. Images/' + spatial_sample + '/genes/' + inputvalue + '_from_' + singlenuc_sample + '_mean_fill_r' + str(r) + '.tif', new_image)


    if outputimageformat=='png':  
            new_image = Image.new("RGBA", (full_width+1, full_height+1), (255, 255, 255, 255))
            normalized_values = result_df['block_sum'].values
            x_values = result_df['x'].astype(int).values
            y_values = result_df['y'].astype(int).values

            # Positive and negative values separation
            positive_mask = normalized_values >= 0
            positive_values = normalized_values[positive_mask]
            positive_values_scaled = positive_values / positive_values.max()
            transparency_values = [max(100, int(255 * intensity)) for intensity in positive_values_scaled]
            pixels = new_image.load() 
            rgb_color = (255, 0, 0)
            for x, y, transparency in zip(x_values[positive_mask], y_values[positive_mask], transparency_values):
                # Set RGB values with constant color and varying transparency
                pixels[x, y] = rgb_color + (transparency,)

            if mode=='cluster':
                new_image.save('./Results/02. Images/' + spatial_sample + '/clusters/cluster' + inputvalue + '_from_' + singlenuc_sample + '_mean_r' + str(r) + '.png')
            if mode=='gene':
                new_image.save('./Results/02. Images/' + spatial_sample + '/genes/' + inputvalue + '_from_' + singlenuc_sample + '_mean_r' + str(r) + '.png')
            
    # plot histogram
    fix, axs = plt.subplots(1, 1, figsize =(10,7), tight_layout = True)
    axs.hist(result_df['block_sum'], bins = 100)
    plt.axvline(x = 0, color = 'r')
    if mode=='cluster':
        plt.savefig('./Results/02. Images/' + spatial_sample + '/clusters/cluster' + inputvalue + '_from_' + singlenuc_sample + '_mean_r' + str(r) + '_thres0_sumblocksums.pdf', format = 'pdf')
    if mode=='gene':
        plt.savefig('./Results/02. Images/' + spatial_sample + '/genes/' + inputvalue + '_from_' + singlenuc_sample + '_mean_r' + str(r) + '_thres0_sumblocksums.pdf', format = 'pdf')

        
    # save total counts under the mask
    ## scale based on block sum intensity of that point?? 
    result_df_sub = result_df.loc[result_df['block_sum'] > 0]
    result_df_sub['MIDCount_blocksum'] = result_df_sub['block_sum']
    res = pd.DataFrame(result_df_sub.groupby(by=["geneID"])["MIDCount"].sum())
    res2 = pd.DataFrame(result_df_sub.groupby(by=["geneID"])["MIDCount_blocksum"].sum()) ### new
    res=pd.DataFrame({'geneID': res.index,'MIDCount': res['MIDCount'], 'MIDCount_blocksum': res2['MIDCount_blocksum']}) ### new
    res['MIDCount_totpixel_fraction'] = res['MIDCount'] / int(len(result_df_sub))
    
    if mode=='cluster':
        res.to_csv('./Results/02. Images/' + spatial_sample + '/clusters/cluster' + inputvalue + '_from_' + singlenuc_sample + '_mean_r' + str(r) + '_countsundermask.csv', index=False)
    if mode=='gene':
        res.to_csv('./Results/02. Images/' + spatial_sample + '/genes/' + inputvalue + '_from_' + singlenuc_sample + '_mean_r' + str(r) + '_countsundermask.csv', index=False)


    # result_df_sub
    if mode=='cluster':
        result_df_sub.to_csv('./Results/02. Images/' + spatial_sample + '/clusters/cluster' + inputvalue + '_from_' + singlenuc_sample + '_mean_r' + str(r) + '_result_df_sub.csv', index=False)
    if mode=='gene':
        result_df_sub.to_csv('./Results/02. Images/' + spatial_sample + '/genes/' + inputvalue + '_from_' + singlenuc_sample + '_mean_r' + str(r) + '_result_df_sub.csv', index=False)

    


#%%
#clusters=[2,3,1,6,7,8,9] #,11,12,13,14,15,16,17,18,19,20] 
#for cluster in clusters:
#    print("Running cluster " + str(cluster))
#    make_images(singlenuc_sample='CTR081_Fron',
#                spatial_sample = '2000-018_GFM_SS200000838BL_A6',
#                overlap = 3,
#                block_size = 5000,
#                r=10, 
#                mode='cluster', # 'gene' or 'cluster'
#                inputvalue=str(cluster), # specify gene or cluster
#                method='stereoseq', # 'stereoseq' 'merfish' 'xenium'
#                fill=False,
#                outputimageformat='png') # png or tiff

#%%
#genes=["NPY", "GFAP", "WDR49", "PLP1", "P2RY12", "SNAP25"]
#for gene in genes:
#    print("Running gene " + str(gene))
#    make_images(singlenuc_sample='Allen_MTG_Smartseq',
#                spatial_sample = 'H20.33.002_1217501029',
#                overlap = 3,
#                block_size = 5000,
#                r=10, 
#                mode='gene', # 'gene' or 'cluster'
#                inputvalue=str(gene), # specify gene or cluster
#                fill=True,
#                outputimageformat='png',
#                method='allen-merfish' # 'stereoseq' 'merfish' 'xenium'
#                )
    
