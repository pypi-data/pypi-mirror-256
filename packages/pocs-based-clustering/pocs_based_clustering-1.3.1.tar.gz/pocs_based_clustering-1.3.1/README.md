# POCS-based Clustering Algorithm 

[![Paper](https://img.shields.io/badge/Paper-PDF-red)](https://tranleanh.github.io/assets/pdf/IWIS_2022.pdf)
[![Paper](https://img.shields.io/badge/Conference-IEEE-blue)](https://ieeexplore.ieee.org/document/9920762)
[![Blog](https://img.shields.io/badge/Blog-Medium-blue)](https://towardsdatascience.com/pocs-based-clustering-algorithm-explained-2f7d25183eff)
[![Blog](https://img.shields.io/badge/Package-PyPI-white)](https://pypi.org/project/pocs-based-clustering/)


Official implementation of the Projection Onto Convex Set (POCS)-based clustering algorithm.

## Introduction

 - Main authors: [Le-Anh Tran](https://scholar.google.com/citations?user=WzcUE5YAAAAJ&hl=en), [Dong-Chul Park](https://scholar.google.com/citations?user=VZUH4sUAAAAJ&hl=en)

 - Abstract:
     <p align="justify">
     This paper proposes a data clustering algorithm that is inspired by the prominent convergence property of the Projection onto Convex Sets (POCS) method, termed the POCS-based clustering algorithm. For disjoint convex sets, the form of simultaneous projections of the POCS method can result in a minimum mean square error solution. Relying on this important property, the proposed POCS-based clustering algorithm treats each data point as a convex set and simultaneously projects the cluster prototypes onto respective member data points, the projections are convexly combined via adaptive weight values in order to minimize a predefined objective function for data clustering purposes. The performance of the proposed POCS-based clustering algorithm has been verified through a large scale of experiments and data sets. The experimental results have shown that the proposed POCS-based algorithm is competitive in terms of both effectiveness and efficiency against some of the prevailing clustering approaches such as the K-means/K-Means++ and Fuzzy C-Means (FCM) algorithms. Based on extensive comparisons and analyses, we can confirm the validity of the proposed POCS-based clustering algorithm for practical purposes.
     </p>

## Usage

### Installation


```
pip install pocs-based-clustering
```

### Function


```
from pocs_cluster_analysis import pocs_clustering

centroids, labels = pocs_clustering(input_data, num_clusters, num_iterations)
```


## Citation

Please cite our works if you utilize any data from this work for your study.

```bibtex
@inproceedings{tran2022pocs,
  title={POCS-based Clustering Algorithm},
  author={Tran, Le-Anh and Deberneh, Henock M and Do, Truong-Dong and Nguyen, Thanh-Dat and Le, My-Ha and Park, Dong-Chul},
  booktitle={2022 International Workshop on Intelligent Systems (IWIS)},
  pages={1--6},
  year={2022},
  organization={IEEE}
}

@article{tran2024cluster,
  title={Cluster Analysis via Projection onto Convex Sets},
  author={Tran, Le-Anh and Kwon, Daehyun and Deberneh, Henock Mamo and Park, Dong-Chul},
  journal={Intelligent Data Analysis},
  year={2024},
  publisher={IOS Press}
}
```

Have fun!

LA Tran
