

# wikiSERA

SERA (Summarization Evaluation by Relevance Analysis) is an evaluation method for automatic 
summarization proposed by [(Cohan and Goharian, 2016)](https://arxiv.org/pdf/1604.00400.pdf). Here, you can find SERA implementation and wikiSERA.
**wikiSERA** is a SERA extension to evaluate summaries. 

## About this code

This code was developed with  python 3.6.7 using [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html) as search
engine library. You can install all the requirements you need to run SERA evaluation system with the following instruction:

 ```bash
 $ pip install -r requirements.txt
 $ python -m spacy download en_core_web_sm
 $ tar xzvf 
 ```

## How to run
### Basic execution
A command for running **wikiSERA** on candidate and reference summaries. 
```
$ python wikisera.py -c test/candidates/ -r test/references/ -o test/output/
```
Files names from the `candidates` folder must respect the `source_name.system_number` syntax.  

Files names from the `references` folder must respect the `source_name.reference_name` syntax

The `output/` folder is where the wikiSERA evaluations file will be written.

Example of file names syntax from the [TAC 2009](https://tac.nist.gov/2009/Summarization/) summarization track. 
```bash
wikiSERA/candidates$ ls 
D0901-A.M.100.A.1   D0901-A.M.100.A.2  D0901-A.M.100.A.3  D0901-A.M.100.A.4  D0901-A.M.100.A.5  D0901-A.M.100.A.6  D0901-A.M.100.A.7  D0901-A.M.100.A.8
```
In the above example, the summarized source document name is `D0901-A.M.100.A` and the evaluated summarization systems are indicated as `.1` (system 1), `.2` (system 2), etc. In this case, we would have the following references folder:
```bash
wikiSERA/references$ ls
D0901-A.M.100.A.A  D0901-A.M.100.A.C  D0901-A.M.100.A.F  D0901-A.M.100.A.H
```
Where the source document name is `D0901-A.M.100.A` and the human gold standard reference summaries for the that document are indicated with `.A`, `.C`, etc. 

The result of this minimal execution should be:
```bash
********** Found 8 query summaries **********
dic_automatic_summaries:  8
lst_articlesIndex_random_files 10000
********** Processing 8 summary queries : 0->8 **********
.......... candidates/D0901-A.M.100.A.1
.......... candidates/D0901-A.M.100.A.2
.......... candidates/D0901-A.M.100.A.3
.......... candidates/D0901-A.M.100.A.4
.......... candidates/D0901-A.M.100.A.5
.......... candidates/D0901-A.M.100.A.6
  6/8. elapsed time : 22.686s
.......... candidates/D0901-A.M.100.A.7
.......... candidates/D0901-A.M.100.A.8
  8/8. elapsed time : 30.531s
  output evaluation files:
.......... output/wikisera_scores_0-8.txt
.......... output/wikisera_retrieved_docs_0-8.txt
********** Evaluation done in 30.54s **********
```

The content of the `wikisera/output/wikisera_scores.txt` shows wikiSERA score for each reference and the wikiSERA average score for that file: 
```
D0901-A.M.100.A.1       0.4 0.6 0.4 0.6 --> 0.X x es el promedio (cuando lo termines)
D0901-A.M.100.A.2       0.8 0.6 1.0 0.8 --> 0.X
D0901-A.M.100.A.3       0.6 0.8 0.6 0.8 --> 0.X
D0901-A.M.100.A.4       0.6 1.0 0.6 0.8 --> 0.X
D0901-A.M.100.A.5       0.6 1.0 0.6 0.8 --> 0.X
D0901-A.M.100.A.6       0.6 1.0 0.6 0.8 --> 0.X
D0901-A.M.100.A.7       0.8 0.8 0.8 0.8 --> 0.X
D0901-A.M.100.A.8       0.6 0.6 0.4 0.6 --> 0.X
<!--
```

The output file `wikisera/output/wikisera_retrieved_docs.txt` shows retrieved documents from the Wikipedia subset for each evaluated file and its references:
```
$ head output/wikisera_retrieved_docs_0-8.txt 
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
- `-r folder_name` In this folder we have the gold standard summaries
- `-c folder_name` It is the folder where there are the candidate docs
- `-o folder_name` It is the folder where the scores are stored
- `-p number` Number equal to the rank of the cut-off point. It is the number of documents selected from the index, most related to a query.
                   We experimented with 5 and 10 ranke check-off point.
- `-n number` It is the number of documents that are indexed
- `-i number-number` Interval of the number of summaries to evaluate
- `-t value` Sera type: There are two possible values: *sera* or *dis*
- `-q value` It is the method by which the query is redefined. There are four options:

    1. raw - use all text without changes
    2. np - noun phrases
    3. kw - keywords
    4. plus - noun, verb, adjective

<!--
- `-index_docs_folder` It is the folder where the documents that are indexed are. 
The files are .txt
- `-save_index_folder` It is the folder where the index files generated by whoosh are stored
- `-reference_folder` In this folder we have the gold standard summaries
- `-candidate_folder` It is the folder where there are the candidate docs
- `-results_folder` It is the folder where the scores are stored
- `-index_name` It is the name with which the index generated by whoosh is saved
- `-cut_off_point` It is the  rank cut-off point . It is the number of documents selected from the index, most related to a query.
                   We experimented with 5 and 10 ranke check-off point.
- `-num_docs_index` It is the number of documents that are indexed
- `-interval` Interval of the number of summaries to evaluate
- `-sera_type` There are two possible values: *sera* or *dis*
- `-refine_query` It is the method by which the query is redefined. There are four options:

    1. raw - use all text without changes
    2. np - noun phrases
    3. kw - keywords
    4. plus - noun, verb, adjective
-->
## Dataset

#### Queries
We used the summaries from [TAC 2008](https://tac.nist.gov/data/past/2008/UpdateSumm08.html) as 
queries. TAC 2008 contains 48 document sets; each set represents a different topic. 
Each topic consists of two subsets: A and B. Each subset includes ten documents. 
Subset B is the update of the documents in subset A.

#### Index dataset
 
For the indexing of documents we use two databases: [AQUAINT-2](https://catalog.ldc.upenn.edu/LDC2008T25)
and [Wikipedia]().

AQUAINT-2 is a news article collection. It contains approximately 2.5 GB of text (about 907k). The articles are from October 2004 to March 2006. 
All the articles are written in English. On the other hand, Wikipedia corpus contains approximately
1,778k of documents.  


   

