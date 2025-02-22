import os

# 基本参数
total_files = 163
num_machines = 4
concurrency = 6  # 每台机器的并发数
model_base = "unsloth/DeepSeek-R1-BF16"
suffix = "-of-000163.safetensors"
local_dir = "./DeepSeek-R1-BF16/"

# 计算每台机器的文件数
files_per_machine = total_files // num_machines  # 每台机器的基本文件数
remainder = total_files % num_machines  # 余数

# 生成文件分配
machine_tasks = [[] for _ in range(num_machines)]
for i in range(1, total_files + 1):
    file_name = f"model-{str(i).zfill(5)}{suffix}"  # 生成文件名，如 model-00001-of-000163.safetensors
    # 根据文件序号分配到对应机器
    if i <= files_per_machine * 1:
        machine_tasks[0].append(file_name)
    elif i <= files_per_machine * 2:
        machine_tasks[1].append(file_name)
    elif i <= files_per_machine * 3:
        machine_tasks[2].append(file_name)
    else:
        machine_tasks[3].append(file_name)

# 为每台机器生成下载脚本
for machine_id, task_files in enumerate(machine_tasks, 1):
    script_name = f"download_machine_{machine_id}.sh"
    with open(script_name, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"mkdir -p {local_dir}\n")  # 确保目录存在
        f.write("download_task() {\n")
        f.write("    local file=$1\n")
        f.write(f"    nohup modelscope download --model {model_base} \"$file\" --local_dir {local_dir} > \"download_${{file}}.log\" 2>&1 &\n")
        f.write("}\n\n")
        f.write("# Control concurrency\n")
        f.write(f"MAX_CONCURRENT={concurrency}\n")
        f.write("current_jobs=0\n\n")
        f.write("for file in \\\n")
        
        # 写入文件列表
        for i, file in enumerate(task_files):
            if i == len(task_files) - 1:
                f.write(f"    \"{file}\" ; do\n")  # 最后一个文件后加分号和 do
            else:
                f.write(f"    \"{file}\" \\\n")
        
        # 并发控制逻辑
        f.write("    # Check current running jobs\n")
        f.write("    while [ $current_jobs -ge $MAX_CONCURRENT ]; do\n")
        f.write("        sleep 1\n")
        f.write("        current_jobs=$(jobs -r | wc -l)\n")
        f.write("    done\n")
        f.write("    download_task \"$file\"\n")
        f.write("    current_jobs=$(jobs -r | wc -l)\n")
        f.write("done\n\n")
        f.write("# Wait for all downloads to complete\n")
        f.write("wait\n")
        f.write("echo \"All downloads completed for machine $machine_id\"\n")
    
    # 设置脚本可执行权限
    os.chmod(script_name, 0o755)

print("已生成 4 个下载脚本：")
for i in range(1, 5):
    print(f"download_machine_{i}.sh")
