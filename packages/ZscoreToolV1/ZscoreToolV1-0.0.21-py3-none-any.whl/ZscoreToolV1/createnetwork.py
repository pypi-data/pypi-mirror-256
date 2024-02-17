# import tools
import numpy as np
import pandas as pd
import scanpy as sc
import umap.umap_ as umap
#import matplotlib.pyplot as plt
from scipy.stats import zscore
from tqdm import tqdm
from adjustText import adjust_text
from numpy import where
from sklearn.cluster import DBSCAN
from matplotlib import pyplot as plt
import os

# define functions
def CoExpression(adata, samplename, min_cells, saveoutput):
    # make output folders
    if not os.path.isdir('./Results/'):
        os.mkdir('./Results/')
    if not os.path.isdir('./Results/01. Zscores/'):
        os.mkdir('./Results/01. Zscores/')
    if not os.path.isdir('./Results/01. Zscores/' + samplename):
        os.mkdir('./Results/01. Zscores/' + samplename)

    # extract raw countmatrix
    countmtx = adata.raw.X
    df = pd.DataFrame(countmtx.toarray(), index=adata.obs.index, columns=adata.var.features)
    col_sums = (df != 0).sum(axis=0)
    col_sums.to_csv('./Results/01. Zscores/' + samplename + '/genes.csv') # export list of the genes and total counts

    # filter for genes  
    df = df.loc[:, col_sums >= min_cells] 
    nCells, nGenes = df.shape
    print("Generating co-expression matrix of " + str(nGenes) + " genes expressed in " + str(nCells) + " cells.")

    # generating count table, only include cells with at least 2 counts of a gene
    greater_than_1 = df > 1
    row_indices = [np.where(greater_than_1[col])[0] for col in df.columns]
    CoExprMat = np.zeros((len(row_indices), df.shape[1]), dtype=float)

    # subset table for geneX-positive cells and sum the counts 
    with tqdm(total=len(row_indices), leave=True) as pbar:
        for i, indices in enumerate(row_indices):
            if len(indices) > 0:
                sub = df.values[indices, :]
                CoExprMat[i,:] = (sub.sum(axis=0) / len(indices))
            pbar.update(1) 
    pbar.close()
    
    # zscore by column
    CoExprMat = pd.DataFrame(CoExprMat).dropna(axis=0) 
    CoExprMat_Z = zscore(CoExprMat, axis=0)
    CoExprMat_Z.columns=df.columns
    CoExprMat_Z.index=df.columns
    CoExprMat_Z = CoExprMat_Z.dropna(axis=1).T

    # export z-score table
    if saveoutput==True:
        print("Exporting z-scored co-expression matrix")
        CoExprMat_Z.to_csv('./Results/01. Zscores/' + samplename + '/coexpmat_z.csv')

    return CoExprMat_Z

def VisualizeNetwork(coexpmat, samplename, genes):
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
    umap_result = reducer.fit_transform(coexpmat)
    umap_result = pd.DataFrame(umap_result, columns=['x', 'y'])

    # Visualize the UMAP result
    plt.scatter(umap_result['x'], umap_result['y'], s=0.8, c="black", alpha=0.1, linewidths=0)
    plt.savefig("./Results/01. Zscores/" + samplename + "/UMAP.pdf", format = "pdf", transparent = True)
    plt.close()

    # add gene names to the plot
    umap_result.index = coexpmat.columns
    label_df = umap_result[umap_result.index.isin(genes)]
    plt.scatter(umap_result['x'], umap_result['y'], s=0.5, color='grey', alpha=0.1, linewidths=0)
    plt.scatter(label_df['x'], label_df['y'], s=0.5, color='red', label="Labels")
    texts = [plt.text(x, y, label) for label, x, y in zip(label_df.index, label_df['x'], label_df['y'])]
    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'), force_text=(0.1, 0.1))
    plt.savefig("./Results/01. Zscores/" + samplename + "/UMAP_geneannotation" + ".pdf", format = "pdf", transparent = True)
    plt.close()

    return umap_result

def ClusterGenes(umap_data, samplename, eps, min_samples):
    #%% dbscan clustering
    model = DBSCAN(eps=eps, min_samples=min_samples)
    # fit model and predict clusters
    yhat = model.fit_predict(umap_data)
    clusters = np.unique(yhat)
    # define colormap
    colors = plt.cm.rainbow(np.linspace(0, 1, len(clusters)))
    # create scatter plot for samples from each cluster
    for cluster, color in zip(clusters, colors):
        # get row indexes for samples with this cluster
        row_ix = where(yhat == cluster)
    # create scatter of these samples
    plt.scatter(umap_data['x'].iloc[row_ix], umap_data['y'].iloc[row_ix], s=0.2, linewidth=0, label=f'Cluster {cluster}', c=[color])
    # calculate the centroid of the cluster
    cluster_center = np.mean(umap_data.iloc[row_ix], axis=0)
    # label the centroid with the cluster number
    plt.text(cluster_center[0], cluster_center[1], str(cluster), fontsize=8, color='black', ha='center', va='center')
    plt.savefig("./Results/01. Zscores/" + samplename + "/UMAP_geneclustering" + ".pdf", format = "pdf", transparent = True)
    plt.close()
    return yhat

def ExportClustering(umap_data, samplename, coexpmat, cluster_annotation):
    #%% extract zscore lists per cluster
    umap_data.to_csv('./Results/01. Zscores/' + samplename + '/Cluster_annotation.csv')

    #coexpmat.columns = df.columns
    #coexpmat.index = df.columns

    for cluster in np.unique(cluster_annotation):
        row_ix = where(cluster_annotation == cluster)
        res_zscore_sub = coexpmat.iloc[row_ix] 
        result_mean = res_zscore_sub.mean(axis = 0)
        result_sum = res_zscore_sub.sum(axis = 0)
    
        result_df = pd.DataFrame({'mean': result_mean, 'sum': result_sum})
        result_df.to_csv('./Results/01. Zscores/' + samplename + '/Cluster' + str(cluster) + '.csv')











