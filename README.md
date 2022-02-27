

# GeSERA

This repository contains the dataset and code of our work *"GeSERA: General-domain Summary Evaluation by Relevance Analysis"*.

## Abstract

 We present GeSERA, an open-source improved version of SERA for evaluating automatic extractive and abstractive summaries from the general domain. SERA is based on a search engine that compares candidate and reference summaries (called queries) against an information retrieval document base (called index). SERA was originally designed for the biomedical domain only, where it showed a better correlation with manual methods than the widely used lexical-based ROUGE method. In this paper, we take out SERA from the biomedical domain to the general one by adapting its content-based method to successfully evaluate summaries from the general domain. First, we improve the query reformulation strategy with POS Tags analysis of general-domain corpora. Second, we replace the biomedical index used in SERA with two article collections from AQUAINT-2 and Wikipedia. We conduct experiments with TAC2008, TAC2009, and CNNDM datasets. Results show that, in most cases, GeSERA achieves higher correlations with manual evaluation methods than SERA, while it reduces its gap with ROUGE for general-domain summary evaluation. GeSERA even surpasses ROUGE in two cases of TAC2009. Finally, we conduct extensive experiments and provide a comprehensive study of the impact of human annotators and the index size on summary evaluation with SERA and GeSERA. 

## Installation

GeSERA was developed with python 3.6.7 using [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html) as search engine library.
First download anaconda3 from the [official website](https://www.anaconda.com/products/individual), then clone this repository.
You can install all the requirements you need to run GeSERA with the following instructions:

 ```bash
 $ conda create -n gesera_env python=3.6.7
 $ conda activate gesera_env
 $ cat requirements.txt | while read x; do conda install "$x" ;done
 $ python -m spacy download en_core_web_sm
 $ cd data
 $ tar xzvf wiki10000.tar.gz
 $ cd ..
 ```

## How to run
### Basic execution
A command for running **GeSERA** on candidate and reference summaries. 
```
$ python gesera.py -c test/candidates/ -r test/references/ -o test/output/
```
Files names from the `test/candidates` folder must respect the `source_name.system_number` syntax.  

Files names from the `test/references` folder must respect the `source_name.reference_name` syntax.

The `test/output/` folder is where the GeSERA evaluation file will be written.

Example of file names syntax from [TAC 2009](https://tac.nist.gov/2009/Summarization/) summarization track. 
```bash
test/candidates$ ls 
D0901-A.M.100.A.1   D0901-A.M.100.A.2  D0901-A.M.100.A.3  D0901-A.M.100.A.4  D0901-A.M.100.A.5  D0901-A.M.100.A.6  D0901-A.M.100.A.7  D0901-A.M.100.A.8
```

In the above example, the summarized source topic's name is `D0901-A`, where `A` refers to the set `A` of TAC 2009. `100` refers to the summary length. The evaluated summarization systems are indicated as `.1` (system 1), `.2` (system 2), etc. 

In this case, we would have the following references folder:
```bash
test/references$ ls
D0901-A.M.100.A.A  D0901-A.M.100.A.C  D0901-A.M.100.A.F  D0901-A.M.100.A.H
```
Where the human gold standard reference summaries for the topic `D0901-A` are indicated with `.A`, `.C`, etc.

The result of this minimal execution should be:
```bash
********** Found 8 query summaries **********
Interval of summaries to evaluate: 0-8
Using a  10000  Wikipedia documents index
********** Processing 8 summary queries : 0->8 **********
test/candidates/D0901-A.M.100.A.1
test/candidates/D0901-A.M.100.A.2
test/candidates/D0901-A.M.100.A.3
test/candidates/D0901-A.M.100.A.4
test/candidates/D0901-A.M.100.A.5
test/candidates/D0901-A.M.100.A.6
  6/8. elapsed time : 49.319s
test/candidates/D0901-A.M.100.A.7
test/candidates/D0901-A.M.100.A.8
  8/8. elapsed time : 63.122s
********** Evaluation done in 63.133s **********
```

The `test/output/` folder contains two files:
```bash
$ ls /test/output/
score_sera_raw_5_0-8.2021.01.12.00h49.txt  sera_raw_5_0-8.2021.01.12.00h49.txt
```
The content of the `test/output/score_sera_raw_5_0-8.2021.01.12.00h49.txt` shows the GeSERA score for each candidate-reference comparison. The last column is the average each candidate-reference score. In our example from TAC 2009 we have 4 columns (one for each reference summary). The fifth column is the average GeSERA score: 
```
D0901-A.M.100.A.1       0.2 0.2 0.2 0.2 0.20
D0901-A.M.100.A.2       0.4 0.8 1.0 0.6 0.70
D0901-A.M.100.A.3       0.6 0.4 0.6 0.4 0.50
D0901-A.M.100.A.4       0.4 0.6 0.6 0.4 0.50
D0901-A.M.100.A.5       0.6 0.6 0.6 0.6 0.60
D0901-A.M.100.A.6       0.4 0.6 0.8 0.4 0.55
D0901-A.M.100.A.7       0.6 0.6 0.6 0.6 0.60
D0901-A.M.100.A.8       0.4 0.6 0.6 0.4 0.50
```

The output file `test/output/sera_raw_5_0-8.2021.01.12.00h49.txt` shows retrieved documents from the Wikipedia subset for each evaluated file and its references:
```
$ head test/output/sera_raw_5_0-8.2021.01.12.00h49.txt 
D0901-A.M.100.A.1       ('id_51299_Jammu-and-Kas', 'id_59659_Vallabhbhai-P', 'id_2269057_Mansoor-', 'id_16826_K', 'id_554578_Maurya-Em')
D0901-A.M.100.A.A       ('id_51299_Jammu-and-Kas', 'id_59659_Vallabhbhai-P', 'id_2188274_Pokhra', 'id_2084667_Jammu-Kashmir-Liberation-F', 'id_22158_Nuclear-prolifera')
D0901-A.M.100.A.C       ('id_2269057_Mansoor-', 'id_51299_Jammu-and-Kas', 'id_59659_Vallabhbhai-P', 'id_2084667_Jammu-Kashmir-Liberation-F', 'id_373733_V-P-S')
D0901-A.M.100.A.F       ('id_2269057_Mansoor-', 'id_51299_Jammu-and-Kas', 'id_2084667_Jammu-Kashmir-Liberation-F', 'id_2188274_Pokhra', 'id_22158_Nuclear-prolifera')
D0901-A.M.100.A.H       ('id_51299_Jammu-and-Kas', 'id_2269057_Mansoor-', 'id_59659_Vallabhbhai-P', 'id_2084667_Jammu-Kashmir-Liberation-F', 'id_22158_Nuclear-prolifera')
```
### Advanced execution

```bash
$ python gesera.py 
           -c candidates/ 
           -r references/ 
           -o output/
           -q raw
           -t sera
           -p 5
           -n 10000
           -i 0-2
           -x wiki
           -d data/wiki10000/
           -s data/index/
  ```
<!--
python gesera.py 
-index_docs_folder /path/index/txt/
-save_index_folder /path/save_index/
-reference_folder /path/models/ 
-candidate_folder /path/candidates/
-results_folder /path/results/
-refine_query raw -sera_type sera
-cut_off_point 5 -num_docs_index 10000 
-index_name name  -interval 0-2
***fixed parameters:
index_docs_folder
save_index_folder
index_name
***optional parameters
-refine_query raw
-sera_type sera
-cut_off_point 5
-num_docs_index 10000
-interval 0-2
*** TODO: 
1) Fixed and optional parameters
2) Dependencies installation script
7) File Names
1) provide a limited set of the TAC 2008 corpus
2) provide a limted set of the TAC 2009 corpus
3) provide a limited set of the Cohan 2018 corpus
4) Add GPL licenses
5) Fork to an anonymous gitlab or github repository
--> 

### Parameters
In the following list, we explain the parameters that you should use:


- `-r: str -` Path where the gold standard reference summaries are located
- `-c: str -` Path where the candidate summaries to be evaluated are located
- `-o: str -` Output folder path
- `-p: int -` Cut-off point. This parameter indicates the number of resulting documents selected by a query.
- `-n: int -` Number of indexed documents
- `-i: str[int-int] -` Interval of summaries to evaluate (i.e. 0-10 will evaluate only the first 10 summaries of the candidates folder)
- `-t: int -` Sera variant to be use. It can be *sera* (the order of the documents in the resulting vector is not taken into account) or *dis* (the order matters)
- `-x: str -` Name of the index 
- `-d: str -` Path containing the documents to index
- `-s: str -` Path where the index is stored
- `-q: int -` Query redefinition parameter:

      1. raw - use all text without changes
      2. np - keep only noun phrases
      3. kw - keep only keywords
      4. gesera - keep nouns, verbs, and adjectives


### GeSERA correlations
The module `correlation/gesera_correlations.py` computes Pearson, Spearman, and Kendall correlations between GeSERA automatic evaluations and Pyramid manual evaluations on TAC 2009 dataset. The program's main goal is to reproduce the correlations reported in the paper and compare them to other evaluation measures like ROUGE.

### SERA-DIS
The module `SERA-DIS/ComputeSERADIS.py` takes into consideration the order of the articles in the Wikipedia resulting vector when computing SERA scores. It relies on the document vectors output file to optimize the relevance analysis ordered comparison of the candidate and the reference Wikipedia document vectors (from sera_raw* output file)



## Paper
The paper was published in the RANLP 2021 conference. Paper link : https://hal-cnrs.archives-ouvertes.fr/hal-03408902/document

To cite this work:

```
@article{lopez2021_gesera,
  title={GeSERA: General-domain Summary Evaluation by Relevance Analysis},
  author={L{\'o}pez Espejel, Jessica and de Chalendar, Ga{\"e}l and Garcia Flores, Jorge and Charnois, Thierry and Vladimir Meza Ruiz, Ivan},
  booktitle={Conference on Recent Advances in Natural Language Processing (RANLP)},
  year={2021}
}
```

