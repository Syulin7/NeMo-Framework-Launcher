import os
import sys
import json
from CITestHelper import CITestHelper
import time
from os.path import exists

if __name__ == '__main__':
    args = sys.argv[1:]
    ci_job_results_dir = args[0] # eg. '/home/shanmugamr/bignlp-scripts/results/train_gpt3_126m_tp1_pp1_1node_100steps'
    git_results_dir_path = args[1]
    base_image = args[2]
    current_timestamp = time.time()

    train_time_list = CITestHelper.read_tb_logs_as_list(ci_job_results_dir, "train_step_timing")
    train_time_list = train_time_list[len(train_time_list) // 2:]  # Discard the first half.
    train_time_avg = sum(train_time_list) / len(train_time_list)

    output_file_name = ci_job_results_dir.rsplit("/", 1)[1]+".json"
    release_perf_file = os.path.join(git_results_dir_path, output_file_name)

    if not exists(release_perf_file):
        new_result={}
        new_result[base_image] = [current_timestamp,train_time_avg]
        final_result={}
        final_result["train_time_metrics"] = new_result
        final_result["peak_memory_metrics"] = {}
        with open(release_perf_file, "w") as f:
            json.dump(final_result, f)
    else:
        with open(release_perf_file) as f:
            previous_results = json.load(f)    
        previous_results["train_time_metrics"][base_image] = [current_timestamp,train_time_avg] 
        final_result = previous_results
        with open(release_perf_file, 'w') as f:
             json.dump(final_result, f)

    print(f" ****** Release Performance timeline : {final_result} logged in  {release_perf_file}", flush=True)
