import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec, colors
from datetime import datetime
from sklearn.manifold import TSNE
from absl import flags
import pandas as pd
import seaborn as sns
import scanpy as sc

def read_dataset(input,highly_genes=4000):
    
    adata=sc.read_h5ad(input)

    adata_sel=adata

    if highly_genes > 0:
        adata_sel.var_names_make_unique()

        sc.pp.filter_genes(adata_sel, min_cells=3)
        sc.pp.normalize_per_cell(adata_sel, counts_per_cell_after=1e4)
        sc.pp.log1p(adata_sel)
        adata_sel.raw = adata_sel
        sc.pp.highly_variable_genes(adata_sel, min_mean=0.0125, max_mean=3, min_disp=0.5, n_top_genes=highly_genes)
        adata_sel = adata_sel[:, adata_sel.var['highly_variable']].copy()
        
    counts=pd.DataFrame(adata_sel.X)
    m, n = counts.shape
    print('the num. of cell = {}'.format(m))
    print('the num. of genes = {}'.format(n))

    print('suceed to read input data')
    return adata_sel