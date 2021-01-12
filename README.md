

# wikiSERA
<!--
SERA (Summarization Evaluation by Relevance Analysis) is an evaluation method for automatic 
summarization proposed by [(Cohan and Goharian, 2016)](https://arxiv.org/pdf/1604.00400.pdf). Candidate (automatic) summaries are compared to (human) references by means of an information retrieval query to an indexed document corpus, where each summary is considered as a query and the resulting document vectors are compared. **wikiSERA** is an open source implementation of the SERA method that uses Wikipedia documents as a corpus for general domain summaries evaluation. 
-->

**wikiSERA** is an open-source system for evaluating the quality of automatically generated summaries by comparing them to a set of reference human-written summaries. The original SERA (Summarization Evaluation by Relevance Analysis) method proposed by   [(Cohan and Goharian, 2016)](https://arxiv.org/pdf/1604.00400.pdf) uses candidate and reference summaries as information retrieval queries against a scientific document base. Then, it evaluates their similarity by comparing the overlap of the retrieved results. wikiSERA adapts this content-based evaluation method to general domain summarization by using a subset of long Wikipedia articles as its information retrieval document base. Furthermore, it improves the query strategy with Part-Of-Speech analysis of general domain newswire documents.

## About this code

This code was developed with python 3.6.7 using [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html) as search
engine library. You can install all the requirements you need to run SERA evaluation system with the following instructions:

 ```bash
 $ pip install -r requirements.txt
 $ python -m spacy download en_core_web_sm
 $ cd data
 $ tar xzvf wiki10000.tar.gz
 $ cd ..
 ```

## How to run
### Basic execution
A command for running **wikiSERA** on candidate and reference summaries. 
```
$ python wikisera.py -c test/candidates/ -r test/references/ -o test/output/
```
Files names from the `candidates` folder must respect the `source_name.system_number` syntax.  

Files names from the `references` folder must respect the `source_name.reference_name` syntax.

The `output/` folder is where the wikiSERA evaluation file will be written.

Example of file names syntax from [TAC 2009](https://tac.nist.gov/2009/Summarization/) summarization track. 
```bash
wikiSERA/candidates$ ls 
D0901-A.M.100.A.1   D0901-A.M.100.A.2  D0901-A.M.100.A.3  D0901-A.M.100.A.4  D0901-A.M.100.A.5  D0901-A.M.100.A.6  D0901-A.M.100.A.7  D0901-A.M.100.A.8
```

In the above example, the summarized source topic's name is `D0901-A`, where `A` refers to the set `A` of TAC 2009. `100` refers to the summary length. The evaluated summarization systems are indicated as `.1` (system 1), `.2` (system 2), etc. 

In this case, we would have the following references folder:
```bash
wikiSERA/references$ ls
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
The content of the `test/output/score_sera_raw_5_0-8.2021.01.12.00h49.txt` shows the wikiSERA score for each candidate-reference comparison. The last column is the average each candidate-reference score. In our example from TAC 2009 we have 4 columns (one for each reference summary). The fifth column is the average wikiSERA score: 
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

The output file `wikisera/output/sera_raw_5_0-8.2021.01.12.00h49.txt` shows retrieved documents from the Wikipedia subset for each evaluated file and its references:
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
$ python wikisera.py 
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
python wikisera.py 
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
In the following list we explain the parameters you should use:

###### Parameters:
- `-r folder_name` Path of the gold standard reference summaries are located
- `-c folder_name` Path of the candidate summaries to be evaluated
- `-o folder_name` Output path
- `-p number` Cut-off point. This parameter indicates the number of resulting documents selected from a query.
- `-n number` Number of indexed documents
- `-i number-number` Interval of summaries to evaluate (i.e. 0-10 will evaluate only the first 10 summaries of the candidates folder)
- `-t value` Sera variant to be use. It can be *sera* (the order of the documents in the resulting vector is not taken into account) or *dis* (the order matters)
- `-x index_name` Name of the index 
- `-d folder_name` Path containing the documents to index
- `-s folder_name` Path where the index is stored
- `-q value` Query redefinition parameter:

    1. raw - use all text without changes
    2. np - noun phrases
    3. kw - keywords
    4. wikisera - noun, verb, adjective


   

