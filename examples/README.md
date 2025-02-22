### Example scripts for pre-train and finetuning 
These scripts run a recommended config for GPT, LLAMA2, Nemotron pretraining, and finetuning for various model sizes on A100, H100. For example, for GPT3 pretrain the following folders provide sample scripts.

- [a100](https://github.com/NVIDIA/NeMo-Megatron-Launcher/tree/master/examples/training/gpt/a100)
: Scripts to run GPT pretraining on NVIDIA A100, in bf16 data type

- [h100](https://github.com/NVIDIA/NeMo-Megatron-Launcher/tree/master/examples/training/gpt/h100)
: Scripts to run GPT pretraining for NVIDIA H100, in fp8 data type

#### Setup
1. To run these scripts, you must have access to the nemo container (https://catalog.ngc.nvidia.com/orgs/nvidia/containers/nemo)
     - Please sign in at [NGC](https://ngc.nvidia.com/signin) (user = ea-bignlp/ga-participants) to access the catalog.
       
2. Update the following bash variables in the example run scripts:
     - ``` NEMO_MEGATRON_LAUNCHER_DIR ``` : the directory of where this repository is located

     - ``` DATA_DIR ``` : the directory of the dataset used for pretraining, by default this is ``` NEMO_MEGATRON_LAUNCHER_DIR/data ```

3. Enter your cluster enviroment settings at 
  [config.yaml](https://github.com/NVIDIA/NeMo-Megatron-Launcher/blob/master/launcher_scripts/conf/config.yaml)
    
    For bcm type clusters update the job name, partition, and account at [bcm.yaml]( https://github.com/NVIDIA/NeMo-Megatron-Launcher/blob/master/launcher_scripts/conf/cluster/bcm.yaml)

4. For testing performance with synthetic data on an interactive node, you need to add the following options to your bash script:
    ```
            cluster_type=interactive \
            ++training.cluster_type=BCP \
            training.model.data.data_impl="mock" \
            training.model.data.data_prefix=[]
    ```
    
For further details see [General Configuration](https://docs.nvidia.com/nemo-framework/user-guide/latest/modelguide/usingautoconfigurator.html#general-configuration) 

#### Results
For performance, the "step_time_per_sec" variable on the console out provides a quick way to read performance of a workload.

For more details and graphics, one can use tensorboard or Weights and Biases. In order to use that, please use results stored at ``` NEMO_MEGATRON_LAUNCHER_DIR/results/<experiment_name> ``` with the following structure:

- ``` NEMO_MEGATRON_LAUNCHER_DIR/results/<experiment_name>/<experiment_name>.yaml ``` : The config of the pretrained model
- ``` NEMO_MEGATRON_LAUNCHER_DIR/results/<experiment_name>/<jobname>_<experiment_name>.sh ``` : The autogenerated .sh file that was run
- ``` NEMO_MEGATRON_LAUNCHER_DIR/results/<experiment_name>/results/ ``` : Directory contained per rank logs, and tensorboard data.

For further details see [Interpreting the Results](https://docs.nvidia.com/nemo-framework/user-guide/latest/modelguide/usingautoconfigurator.html#interpreting-the-results) 

### Benchmark performance numbers (pretraining)

- The results in the table below show pre-training performance of various models on DGXH100, with FP8.
- Please refer to [MLCommons Training results](https://mlcommons.org/benchmarks/training/) for performance of GPT3-175B pre-training on large scale H100 systems. 
- To calculate Model TFLOPs, please see Appendix A in [paper](https://arxiv.org/pdf/2205.05198.pdf).
  
  
| Model | #-GPUs | GBS | MBS | Sequence <br> Length | TP | PP | Tokens <br>/ sec / GPU | Model TFLOP <br> / sec / GPU | Est. time to train <br> in days <br> (1T tokens, 1K GPUs) |
| ---      | ---      |----   |----   | ---      |----   | ---      | ---      | ---     | ---     |
| GPT3-175B    | 512 | 2048 | 1 | 2048 | 4 | 8 | 741 |  [797*](https://developer.nvidia.com/blog/setting-new-records-at-data-center-scale-using-nvidia-h100-gpus-and-quantum-2-infiniband/) | 15.3  |
| GPT3-5B       | 64 | 2048 | 4 | 2048 | 1 | 1 | 23574 | 746 | 0.5  |
| GPT3-20B      | 64 | 256  | 2 | 2048 | 2 | 1 | 5528 | 708 | 2.0  |
| LLAMA2-7B     | 8  | 128  | 1 | 4096 | 1 | 1 | 16290 | 751 | 0.7  |
| LLAMA2-13B    | 16 | 128  | 1 | 4096 | 4 | 1 | 8317 | 725 | 1.4  |
| LLAMA2-70B    | 64 | 128  | 1 | 4096 | 4 | 4 | 1725 | 767 | 6.6  |
| Nemotron-8B   | 8  | 32   | 2 | 4096 | 2 | 1 | 11538 | 593 | 1.0  |
| Nemotron-22B  | 16 | 32   | 2 | 4096 | 1 | 4 | 3828 | 499 | 3.0  |


### Benchmark performance numbers (finetuning)

- The following table provides performance benchmarking of LLAMA2 models with SFT (supervised fine-tuning), and LoRA (Low-rank adaptors) on DGXH100, with FP8.
- For fine-tuning, we use [SQuAD-v1.1](https://rajpurkar.github.io/SQuAD-explorer/) dataset, and the inputs are packed to 4096 tokens.
- To calculate Model TFLOPs, please see Appendix A in [paper](https://arxiv.org/pdf/2205.05198.pdf).


| Model | Mode | #-GPUs | GBS | MBS | Sequence <br> Length | TP | PP | Tokens <br>/ sec / GPU | Model TFLOP <br> / sec / GPU | Est. time to <br> complete in mins <br> (10M tokens) |
| ---     | ---      |----   | ---      |----   | ---      |----   | ---      | ---      | ---     | ---     |
| LLAMA2-7B  | SFT   | 8  | 32 | 1 | 4096 | 1 | 1 | 14761 | 591 | 1.4 |
| LLAMA2-13B | SFT   | 8  | 32 | 1 | 4096 | 1 | 4 | 8989  | 698 | 2.3 |
| LLAMA2-70B | SFT   | 16 | 32 | 1 | 4096 | 4 | 4 | 1470  | 609 | 7.1 |
| LLAMA2-7B  | LoRA  | 8  | 32 | 1 | 4096 | 1 | 1 | 20750 | 556 | 1.0 |
| LLAMA2-13B | LoRA  | 8  | 32 | 1 | 4096 | 1 | 1 | 12584 | 654 | 1.7 |
| LLAMA2-70B | LoRA  | 8  | 32 | 1 | 4096 | 2 | 4 | 2279  | 631 | 9.1 |
