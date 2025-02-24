import psutil
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlShutdown
import subprocess
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import time
import tiktoken


def run_ollama_model(model_name):
    try:
        # 执行 ollama run 命令
        command = f"ollama run {model_name}"
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print("命令执行成功")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"执行命令时出错：{e.stderr}")

def stop_ollama_model(model_name):
    try:
        # 执行 ollama stop 命令
        command = f"ollama stop {model_name}"
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print("命令执行成功")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"执行命令时出错：{e.stderr}")

# 流式输出，便于分析生成速度
def model_inference_stream(model_name, question):
    llm = ChatOllama(
        model = model_name,
        temperature = 0.8,
        num_predict = 1024,
    )

    
    template = """
    Question: {question_}
    Answer: 请一步一步思考
    """

    chunks = []
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    # 设定编码，进行分词
    encoding = tiktoken.get_encoding("cl100k_base")
    prompt_tokens = len(encoding.encode(prompt.format(question_=question)))
    
    # 记录开始时间
    start_time = time.time()
    first_token_time = None
    output_tokens = 0
    output_text = ""
    
    for chunk in chain.stream({"question_": question}):
        if first_token_time is None:
            # 记录输入提示到产生第一个 token 的时间
            first_token_time = time.time() - start_time
        chunks.append(chunk)
        print(chunk.content, end="", flush=True)
    
    output_tokens = len(encoding.encode(str(chunks)))
    # 记录完整输出后所需的时间
    total_time = time.time() - start_time
    
    return {
        "prompt_tokens": prompt_tokens,
        "first_token_time": first_token_time,
        "output_tokens": output_tokens,
        "total_time": total_time
    }


def get_gpu_memory_():
    """
    获取指定 GPU 的已用显存（单位：MB）
    """
    info = nvmlDeviceGetMemoryInfo(handle)
    used = info.used / 1024 ** 2  # 转换为 MB
    return used

def get_gpu_memory():
    try:
        used = get_gpu_memory_()
    except Exception as e:
        print(f"获取GPU显存信息时出错: {e}")
        used = 0
    return used

def get_cpu_memory():
    """
    获取指定 CPU 的已用显存（单位：MB）
    """
    # 获取当前进程的内存信息
    process = psutil.Process()
    # 模型加载前的 CPU 和 GPU 内存
    used = process.memory_info().rss / 1024 ** 2  # 转换为 MB
    return used

if __name__ == '__main__':
    # 初始化 NVML
    nvmlInit()
    # 获取 GPU 句柄（假设使用的是 GPU 0）
    gpu_index = 0
    handle = nvmlDeviceGetHandleByIndex(gpu_index)
    
    # 模型加载前的 CPU 和 GPU 内存
    cpu_before = get_cpu_memory()
    gpu_used_before = get_gpu_memory()

    model_name = 'deepseekv2-lite-chat'
    run_ollama_model(model_name)

    # 模型加载后的 CPU 和 GPU 内存
    cpu_after_load = get_cpu_memory()
    gpu_used_after_load = get_gpu_memory()

    # 计算加载模型后的内存变化量
    cpu_change_load = cpu_after_load - cpu_before
    gpu_change_load = gpu_used_after_load - gpu_used_before

    print(f"加载模型后CPU内存变化量：{cpu_change_load:+.2f} MB")
    print(f"加载模型后GPU显存变化量：{gpu_change_load:+.2f} MB")
    print(f"\n")

    # 生成文本前的内存状态
    cpu_before_inference = get_cpu_memory()
    gpu_used_before_inference = get_gpu_memory()

    # 推理阶段
    question = "用200-300字简单介绍下舟山对浙江的意义"
    stats = model_inference_stream(model_name, question)

    # 推理后的 CPU 和 GPU 内存
    cpu_after_inference = get_cpu_memory()
    gpu_used_after_inference = get_gpu_memory()

    # 计算推理后的内存变化量
    cpu_change_inference = cpu_after_inference - cpu_before_inference
    gpu_change_inference = gpu_used_after_inference - gpu_used_before_inference

    print(f"\n")
    print(f"推理后CPU内存变化量：{cpu_change_inference:+.2f} MB")
    print(f"推理后GPU显存变化量：{gpu_change_inference:+.2f} MB")
    print(f"\n")
    print(f"prompt eval count:    {stats['prompt_tokens']} token(s)") # 输入提示Token数
    print(f"prompt eval duration: {stats['first_token_time']:.3f}s") # 首token响应时间
    print(f"prompt eval rate:     {stats['prompt_tokens']/stats['first_token_time']:.3f} tokens/s") # 模型响应速度
    print(f"eval count:           {stats['output_tokens']} token(s)") # 输出内容token数
    print(f"eval duration:        {stats['total_time']:.3f}s") # 总生成耗时
    print(f"eval rate:            {stats['output_tokens']/stats['total_time']:.3f} tokens/s") # 输出速度

    # 关闭 NVML
    nvmlShutdown()
    stop_ollama_model(model_name)