# fCAT
[![PyPI version](https://badge.fury.io/py/fcat.svg)](https://pypi.org/project/fcat/)
[![Poster at: ECCB2022](https://img.shields.io/badge/Poster%20at-ECCB2022-orange)](https://doi.org/10.7490/f1000research.1119126.1)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/BIONF/fCAT.svg?branch=main)](https://travis-ci.com/BIONF/fCAT)
![Github Build](https://github.com/BIONF/fCAT/workflows/build/badge.svg)

One of the critical steps in a genome sequencing project is to assess the completeness of the predicted gene set. The standard workflow starts with the identification of a set of core genes for the taxonomic group, in which the target species belongs to. The fraction of missing core genes serves then as a proxy of the target gene set completeness.

fCAT is a **f**eature-aware **C**ompleteness **A**ssessment **T**ool, that helps to answer the question "How complete is my gene set?". In particularly, fCAT checks for the presence of conserved genes (the core genes) of a specific taxonomy clade in the target gene set using feature-aware directed ortholog search [fDOG](https://github.com/BIONF/fDOG). In addition to the length criteria for classifying the found orthologs (as same as [BUSCO](https://busco.ezlab.org)), fCAT utilizes the domain architecture similarity [FAS scores](https://github.com/BIONF/FAS) to further validate the orthologs. The later gives an alternative view on the accuracy of the target gene models, which shows how different the target orthologs in comparison to the core genes in their domain architecture.

fCAT outputs both the summary result in a tabular text file and the phylogenetic profile of the core genes, which can be visualized using the tool [PhyloProfile](https://github.com/BIONF/PhyloProfile). By analyzing the profiles of the entire orthologous groups within a specific taxonomy clade, we can further identify and ultimately correct erroneous gene annotations.

[Click here for the full PDF version of the ECCB2022 poster](https://doi.org/10.7490/f1000research.1119126.1)

<p align="center">
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/19269760/202210213-5ed72144-fa43-4d60-8e90-a95df5afcca5.png">
</p>

# Table of Contents
* [How to install](#how-to-install)
* [Usage](#usage)
* [Output](#output)
* [fCAT score modes](#fcat-score-modes)
* [Bugs](#bugs)
* [Contributors](#contributors)
* [How-To Cite](#how-to-cite)
* [Contact](#contact)

# How to install

*fCAT* tool is distributed as a python package called *fcat*. It is compatible with [Python ≥ v3.9](https://www.python.org/downloads/).

You can install *fcat* using `pip`:
```
python3 -m pip install fcat
```

or, in case you do not have admin rights, and don't use package systems like [Anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) to manage environments you need to use the `--user` option:
```
python3 -m pip install --user fcat
```

and then add the following line to the end of your **~/.bashrc** or **~/.bash_profile** file, restart the current terminal to apply the change (or type `source ~/.bashrc`):

```
export PATH=$HOME/.local/bin:$PATH
```

*__Note:__ fCAT requires [R](https://cran.r-project.org) to be present! Please make sure that you have R installed on your computer.*

# Usage

The complete process of *fCAT* can be done using one function `fcat`
```
fcat --coreDir /path/to/fcat_data --coreSet eukaryota --refspecList "HOMSA@9606@2" --querySpecies /path/to/query.fa [--annoQuery /path/to/query.json] [--outDir /path/to/fcat/output]
```

where **eukaryota** is name of the fCAT core set (equivalent to [BUSCO](https://busco.ezlab.org/) set); **HOMSA@9606@2** is the reference species from that core set that will be used for the ortholog search; **query** is the name of species of interest. If `--annoQuery` not specified, *fCAT* fill do the feature annotation for the query proteins using [FAS tool](https://github.com/BIONF/FAS).

# Output
You will find the output in the */path/to/fcat/output/fcatOutput/eukaryota/query/* folder, where */path/to/fcat/output/* could be your current directory if you not specified `--outDir` when running `fcat`. The following important output files/folders can be found:

- *all_summary.txt*: summary of the completeness assessment using all 4 score modes
- *all_full.txt*: the complete assessment of 4 score modes in tab delimited file
- *fdogOutput.tar.gz*: a zipped file of the ortholog search result
- *mode_1*, *mode_2*, *mode_3* and *mode_4*: detailed output for each score mode
- *phyloprofileOutput*: folder contains output phylogenetic profile data that can be used with [PhyloProfile tool](https://github.com/BIONF/PhyloProfile)

Besides, if you have already run *fCAT* for several query taxa with the same fCAT core set, you can find the merged phylogentic profiles for all of those taxa within the corresponding core set output (e.g. _/path/to/fcat/output/fcatOutput/eukaryota/*.phyloprofile_).

# fCAT score modes

The table below explains how the *specific ortholog group cutoffs* for each fCAT core set were calculated, and which *value of the query ortholog* is used to assess its completeness, or more precisely, its functional equivalence to the ortholog group it belongs to. If the value of a query ortholog is *not less than* its ortholog group cutoff, that group will be evaluated as **similar** or **complete**. In case co-orthologs have been predicted, the assessment for the core group will be **duplicated**. Depending on the value of each single ortholog, a *duplicated* group can be seen as **duplicated (similar)** or **duplicated (dissimilar)** in the full report (e.g. *all_full.txt*).

| Score mode | Cutoff | Value used for comparing |
|---|---|---|
| Mode 1 - Strict mode | Mean of FAS scores between all core orthologs | Mean of FAS scores between query ortholog and all core proteins |
| Mode 2 - Reference mode | Mean of FAS scores between refspec and all other core orthologs | Mean of FAS scores between query ortholog and refspec protein |
| Mode 3 - Relaxed mode | The lower bound of the confidence interval calculated by the distribution of all-vs-all FAS score in a core group | Mean of FAS scores between query ortholog and all core proteins |
| Mode 4 - Length mode | Mean and standard deviation of all core protein lengths | Length of query ortholog |

<p align="center">
  <img width="500" alt="image" src="https://user-images.githubusercontent.com/19269760/202210343-aefbdf7b-4a38-44bf-9862-f74cc3bdd52a.png">
</p>

*Note: __FAS scores__ are bidirectional FAS scors; __core protein__ or __core ortholog__ is protein in the core ortholog groups; __query protein__ or __query ortholog__ is ortholog protein of query species; __refspec__ is the specified reference species*

# Bugs
Any bug reports or comments, suggestions are highly appreciated. Please [open an issue on GitHub](https://github.com/BIONF/fCAT/issues/new) or be in touch via email.

# Contributors
- [Vinh Tran](https://github.com/trvinh)
- [Giang Nguyen](https://github.com/giangnguyen0709)
- [Ingo Ebersberger](https://github.com/ebersber)

# How-To Cite
Tran V and Ebersberger I. fCAT: Assessing gene set completeness using domain-architecture aware targeted ortholog searches. F1000Research 2022, 11:1091 (poster) (doi: [10.7490/f1000research.1119126.1](https://doi.org/10.7490/f1000research.1119126.1))

# Contact
For further support or bug reports please contact: tran@bio.uni-frankfurt.de
