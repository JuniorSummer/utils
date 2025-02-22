# ref：https://blog.csdn.net/weixin_42426841/article/details/142745525
import psutil
from transformers import AutoTokenizer, AutoModelForCausalLM
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlShutdown

# 初始化 NVML
nvmlInit()

# 获取 GPU 句柄（假设使用的是 GPU 0）
gpu_index = 0
handle = nvmlDeviceGetHandleByIndex(gpu_index)

def get_gpu_memory():
    """
    获取指定 GPU 的已用显存（单位：MB）
    """
    info = nvmlDeviceGetMemoryInfo(handle)
    used = info.used / 1024 ** 2  # 转换为 MB
    return used

# 获取当前进程的内存信息
process = psutil.Process()

# 获取模型加载前的 CPU 和 GPU 内存
cpu_before = process.memory_info().rss / 1024 ** 2  # 转换为 MB
try:
    gpu_used_before = get_gpu_memory()
except Exception as e:
    print(f"获取GPU显存信息时出错: {e}")
    gpu_used_before = 0

# 加载模型和分词器
model_path = "./"  # 如果模型文件在当前目录下

# 合并后的 GGUF 文件名
gguf_file = "qwen2.5-7b-instruct-q4_k_m.gguf"

# 从本地加载模型
# transformers对gguf支持不全，很多模型无法加载
tokenizer = AutoTokenizer.from_pretrained(model_path, gguf_file=gguf_file, clean_up_tokenization_spaces=True)
model = AutoModelForCausalLM.from_pretrained(model_path, gguf_file=gguf_file)

# 获取模型加载后的 CPU 和 GPU 内存
cpu_after_load = process.memory_info().rss / 1024 ** 2
try:
    gpu_used_after_load = get_gpu_memory()
except Exception as e:
    print(f"获取GPU显存信息时出错: {e}")
    gpu_used_after_load = 0

# 计算加载模型后的内存变化量
cpu_change_load = cpu_after_load - cpu_before
gpu_change_load = gpu_used_after_load - gpu_used_before

print(f"加载模型后CPU内存变化量：{cpu_change_load:+.2f} MB")
print(f"加载模型后GPU显存变化量：{gpu_change_load:+.2f} MB")

# 在生成文本前的内存状态
input_text = "Hello, World!"
inputs = tokenizer(input_text, return_tensors="pt")
cpu_before_inference = process.memory_info().rss / 1024 ** 2
try:
    gpu_used_before_inference = get_gpu_memory()
except Exception as e:
    print(f"获取GPU显存信息时出错: {e}")
    gpu_used_before_inference = 0

# 生成文本
outputs = model.generate(**inputs, max_new_tokens=50)

# 获取推理后的 CPU 和 GPU 内存
cpu_after_inference = process.memory_info().rss / 1024 ** 2
try:
    gpu_used_after_inference = get_gpu_memory()
except Exception as e:
    print(f"获取GPU显存信息时出错: {e}")
    gpu_used_after_inference = 0

# 计算推理后的内存变化量
cpu_change_inference = cpu_after_inference - cpu_before_inference
gpu_change_inference = gpu_used_after_inference - gpu_used_before_inference

print(f"推理后CPU内存变化量：{cpu_change_inference:+.2f} MB")
print(f"推理后GPU显存变化量：{gpu_change_inference:+.2f} MB")

# 输出生成的文本
print("\n生成的文本：")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

# 关闭 NVML
nvmlShutdown()

