source /home/users/jlopez/installs/anaconda3/bin/activate
conda activate python3.6_SERA


python /home/users/jlopez/codes/SERA-plus/run.py \
-index_docs_folder /home/users/jlopez/dataset/TAC2008_AQUAINT-2/index_wikipedia/txt/ \
-save_index_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/indexes/SERA_Wiki/ \
-reference_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/queries/models/   \
-candidate_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/queries/candidates.txt \
-results_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/results/SERA_Wiki/SERA_1_5/ \
-refine_query raw -sera_type sera \
-cut_off_point 5 -num_docs_index 10000  -index_name SERA_Wiki -interval 0-2 &


python /home/users/jlopez/codes/SERA-plus/run.py \
-index_docs_folder /home/users/jlopez/dataset/TAC2008_AQUAINT-2/index_wikipedia/txt/ \
-save_index_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/indexes/SERA_Wiki/ \
-reference_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/queries/models/   \
-candidate_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/queries/candidates.txt \
-results_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/results/SERA_Wiki/SERA_2_5/ \
-refine_query np -sera_type sera \
-cut_off_point 5 -num_docs_index 10000  -index_name SERA_Wiki -interval 0-2 &

python /home/users/jlopez/codes/SERA-plus/run.py \
-index_docs_folder /home/users/jlopez/dataset/TAC2008_AQUAINT-2/index_wikipedia/txt/ \
-save_index_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/indexes/SERA_Wiki/ \
-reference_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/queries/models/   \
-candidate_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/queries/candidates.txt \
-results_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/results/SERA_Wiki/SERA_3_5/ \
-refine_query kw -sera_type sera \
-cut_off_point 5 -num_docs_index 10000  -index_name SERA_Wiki -interval 0-2 &

python /home/users/jlopez/codes/SERA-plus/run.py \
-index_docs_folder /home/users/jlopez/dataset/TAC2008_AQUAINT-2/index_wikipedia/txt/ \
-save_index_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/indexes/SERA_Wiki/ \
-reference_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/queries/models/   \
-candidate_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/queries/candidates.txt \
-results_folder /home/data/jlopez/datasets/TAC2009/my_dataset/preprocessed/results/SERA_Wiki/SERA_4_5/ \
-refine_query plus -sera_type sera \
-cut_off_point 5 -num_docs_index 10000  -index_name SERA_Wiki -interval 0-2 &

