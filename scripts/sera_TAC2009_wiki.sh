source /home/jessica/python3.6_SERA/bin/activate

python /home/jessica/codes/SERA-plus/run.py \
-index_docs_folder  /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/index_TAC2009/txt/ \
-save_index_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/indexes/TAC2009/SERA_1_5/ \
-reference_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/models/  \
-candidate_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/candidates/  \
-results_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/results/TAC2009/SERA_1_5/ \
-refine_query raw \
-cut_off_point 5 -num_docs_index 880  -index_name SERA_1_5 -interval 0-4840 &

python /home/jessica/codes/SERA-plus/run.py \
-index_docs_folder  /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/index_TAC2009/txt/ \
-save_index_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/indexes/TAC2009/SERA_2_5/ \
-reference_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/models/  \
-candidate_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/candidates/  \
-results_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/results/TAC2009/SERA_2_5/ \
-refine_query np \
-cut_off_point 5 -num_docs_index 880  -index_name SERA_2_5 -interval 0-4840 &

python /home/jessica/codes/SERA-plus/run.py \
-index_docs_folder  /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/index_TAC2009/txt/ \
-save_index_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/indexes/TAC2009/SERA_3_5/ \
-reference_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/models/  \
-candidate_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/candidates/  \
-results_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/results/TAC2009/SERA_3_5/ \
-refine_query kw \
-cut_off_point 5 -num_docs_index 880  -index_name SERA_3_5 -interval 0-4840 &

python /home/jessica/codes/SERA-plus/run.py \
-index_docs_folder  /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/index_TAC2009/txt/ \
-save_index_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/indexes/TAC2009/SERA_4_5/ \
-reference_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/models/  \
-candidate_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/candidates/  \
-results_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/results/TAC2009/SERA_4_5/ \
-refine_query plus \
-cut_off_point 5 -num_docs_index 880  -index_name SERA_4_5 -interval 0-4840 &


python /home/jessica/codes/SERA-plus/run.py \
-index_docs_folder  /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/index_TAC2009/txt/ \
-save_index_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/indexes/TAC2009/SERA_1_10/ \
-reference_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/models/  \
-candidate_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/candidates/  \
-results_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/results/TAC2009/SERA_1_10/ \
-refine_query raw \
-cut_off_point 10 -num_docs_index 880  -index_name SERA_1_10 -interval 0-4840 &

python /home/jessica/codes/SERA-plus/run.py \
-index_docs_folder  /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/index_TAC2009/txt/ \
-save_index_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/indexes/TAC2009/SERA_2_10/ \
-reference_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/models/  \
-candidate_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/candidates/  \
-results_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/results/TAC2009/SERA_2_10/ \
-refine_query np \
-cut_off_point 10 -num_docs_index 880  -index_name SERA_2_10 -interval 0-4840 &

python /home/jessica/codes/SERA-plus/run.py \
-index_docs_folder  /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/index_TAC2009/txt/ \
-save_index_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/indexes/TAC2009/SERA_3_10/ \
-reference_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/models/  \
-candidate_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/candidates/  \
-results_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/results/TAC2009/SERA_3_10/ \
-refine_query kw \
-cut_off_point 10 -num_docs_index 880  -index_name SERA_3_10 -interval 0-4840 &

python /home/jessica/codes/SERA-plus/run.py \
-index_docs_folder  /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/index_TAC2009/txt/ \
-save_index_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/indexes/TAC2009/SERA_4_10/ \
-reference_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/models/  \
-candidate_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/queries/candidates/  \
-results_folder /scratch_global/jessica/datasets/TAC2009/my_dataset/preprocessed/results/TAC2009/SERA_4_10/ \
-refine_query plus \
-cut_off_point 10 -num_docs_index 880  -index_name SERA_4_10 -interval 0-4840 &

wait