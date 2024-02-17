#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 15:41:40 2023

@author: emma
"""

import numpy as np
import pandas as pd
import scanpy as sc
import umap
#import matplotlib.pyplot as plt
from scipy.stats import zscore
from tqdm import tqdm
from adjustText import adjust_text
from numpy import where
from sklearn.cluster import DBSCAN
from matplotlib import pyplot as plt
import os



#%% read in single-nuc data
#sample = 'CTR081_Fron'
#adata = sc.read_h5ad("/Users/emma/Library/CloudStorage/OneDrive-KarolinskaInstitutet/2. Postdoc KI/1. ALS-FTD project/FTD-GRN/snRNAseq/Integrated with large dataset/outputfiles/EGE1_output/samples/" + sample + ".h5ad")

sample = 'Allen_MTG_Smartseq'
adata = sc.read_h5ad("/Users/emma/Library/CloudStorage/OneDrive-KarolinskaInstitutet/2. Postdoc KI/Other/Allen Human MULTIPLE CORTICAL AREAS - SMART-SEQ (2019)/outputfiles/dataset.h5ad")

# extract raw countmatrix
countmtx = adata.raw.X
df = pd.DataFrame(countmtx.toarray(), index=adata.obs.index, columns=adata.var.features)

if not os.path.isdir('./Results/01. Zscores/' + sample):
    os.mkdir('./Results/01. Zscores/' + sample)

#%% gene filtering
col_sums = (df != 0).sum(axis=0)

# export list of the genes with total counts
col_sums.to_csv('./Results/01. Zscores/' + sample + '/genes.csv')

# filter for genes expressed in at least 50 cells
df = df.loc[:, col_sums >= 50] # 50

#df = df.sample(5000, axis= 0)


#%% generating count table
# only include cells with at least 2 counts of a gene
greater_than_1 = df > 1
row_indices = [np.where(greater_than_1[col])[0] for col in df.columns]

# generate output table
res = np.zeros((len(row_indices), df.shape[1]), dtype=float)

# subset table for geneX-positive cells and sum the counts 
with tqdm(total=len(row_indices), leave=True) as pbar:
    for i, indices in enumerate(row_indices):
        if len(indices) > 0:
            sub = df.values[indices, :]
            res[i,:] = (sub.sum(axis=0) / len(indices))
        pbar.update(1)  # Update the progress bar
pbar.close()
        
        
        
#%%
res = pd.DataFrame(res)
res = res.dropna(axis=0) # remove rows with NA

# save std per column to a csv file
#stdevs = res.stdev(axis = 0)
#stdevs.to_csv('./Results/01. Zscores/' + sample + '/res_std.csv')

# zscore by column
res_zscore = zscore(res, axis=0)
res_zscore.columns=df.columns
res_zscore.index=df.columns
res_zscore = res_zscore.dropna(axis=1) # there were some NAs
res_zscore = res_zscore.T # rows are samples, columns are genes


#%% Run UMAP
# Create a UMAP reduction
reducer = umap.UMAP(
        n_neighbors=15,#15
        min_dist=0.3, # 0.3
        n_components=2,
        metric='euclidean',
        n_epochs=100, # 100
        spread = 3.0, #3
        random_state=42
    )

# Fit and transform your data using UMAP
umap_result = reducer.fit_transform(res_zscore)

#%%
# Visualize the UMAP result
plt.scatter(umap_result[:, 0], umap_result[:, 1], s=0.8, c="black", alpha=0.1, linewidths=0)
plt.title('UMAP Visualization')
plt.show()


#%% another plot

coords_df = pd.DataFrame(umap_result, columns=['x', 'y'])
coords_df.index = df.columns

# Subset the data for labels
label_subset = [
    "GFAP", "AQP4", "ALDH1L1",   "PLP1",  "MBP", "OPALIN", "WDR49", "CFAP47", "CP",
    "P2RY12", "TMEM119", "CSF1R", "CKB",
     "GAD2", "SLC17A7", "MAP2", "SNAP25", "CARTPT", "NPY", "SST",
     "GAPDH", "HMGB1", "HPRT1", "MALAT1", "NEAT1"
]

# Create a filtered DataFrame for labels
label_df = coords_df[coords_df.index.isin(label_subset)]

# Create a scatter plot
plt.scatter(coords_df['x'], coords_df['y'], s=0.5, color='grey', alpha=0.1, linewidths=0)

# Create a scatter plot with labels
plt.scatter(label_df['x'], label_df['y'], s=0.5, color='red', label="Labels")

# Add labels with text adjustment
texts = [plt.text(x, y, label) for label, x, y in zip(label_df.index, label_df['x'], label_df['y'])]

# Adjust the positions of labels to avoid overlaps
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'), force_text=(0.1, 0.1))

plt.savefig("./Results/01. Zscores/" + sample + "/UMAP_geneannotation" + ".pdf", format = "pdf", transparent = True)


#%% dbscan clustering
# define dataset
X = umap_result
# define the model
model = DBSCAN(eps=0.6, min_samples=150) # 0.52, 25
# fit model and predict clusters
yhat = model.fit_predict(X)
clusters = np.unique(yhat)
# define colormap
colors = plt.cm.rainbow(np.linspace(0, 1, len(clusters)))
# create scatter plot for samples from each cluster
for cluster, color in zip(clusters, colors):
 # get row indexes for samples with this cluster
 row_ix = where(yhat == cluster)
 # create scatter of these samples
 plt.scatter(X[row_ix, 0], X[row_ix, 1], s=0.2, linewidth=0, label=f'Cluster {cluster}', c=[color])
 # calculate the centroid of the cluster
 cluster_center = np.mean(X[row_ix], axis=0)
 # label the centroid with the cluster number
 plt.text(cluster_center[0], cluster_center[1], str(cluster), fontsize=8, color='black', ha='center', va='center')
 plt.savefig("./Results/01. Zscores/" + sample + "/UMAP_geneclustering" + ".pdf", format = "pdf", transparent = True)
# show the plot
pyplot.show()


#%% extract zscore lists per cluster
coords_df['cluster'] = yhat
coords_df.to_csv('./Results/01. Zscores/' + sample + '/Cluster_annotation.csv')

res_zscore.columns = df.columns
res_zscore.index = df.columns

for cluster in clusters:
    row_ix = where(yhat == cluster)
    res_zscore_sub = res_zscore.iloc[row_ix] 
    result_mean = res_zscore_sub.mean(axis = 0)
    result_sum = res_zscore_sub.sum(axis = 0)
    
    result_df = pd.DataFrame({'mean': result_mean, 'sum': result_sum})
    result_df.to_csv('./Results/01. Zscores/' + sample + '/Cluster' + str(cluster) + '.csv')

#%%
# export z-score table
res_zscore.to_csv('./Results/01. Zscores/' + sample + '/res_zscore.csv')









