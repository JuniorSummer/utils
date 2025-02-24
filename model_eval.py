import time
import tiktoken

# 模拟一个生成器，用于模拟模型输出
def mock_model(prompt):
    outputs = ["This", " is", " a", " mock", " output."]
    for output in outputs:
        time.sleep(0.1)  # 模拟模型生成延迟
        yield output

def calculate_token_stats(prompt):
    # 计算提示中的 token 数，首次运行会需要下载模型
    # 原理和huggingface的tokenizer一样，tiktoken更加高效
    # encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    encoding = tiktoken.get_encoding("cl100k_base")
    prompt_tokens = len(encoding.encode(prompt))

    # 记录开始时间
    start_time = time.time()
    first_token_time = None
    output_tokens = 0
    output_text = ""

    # 模拟模型输出，需要结合模型流式输出调整
    for token in mock_model(prompt):
        if first_token_time is None:
            # 记录输入提示到产生第一个 token 的时间
            first_token_time = time.time() - start_time
        output_text += token
        output_tokens = len(encoding.encode(output_text))

    # 记录完整输出后所需的时间
    total_time = time.time() - start_time

    return {
        "prompt_tokens": prompt_tokens,
        "first_token_time": first_token_time,
        "output_tokens": output_tokens,
        "total_time": total_time
    }


if __name__ == '__main__':
    # 示例使用
    prompt = "Please generate a response."
    stats = calculate_token_stats(prompt)
    print(f"prompt eval count:    {stats['prompt_tokens']} token(s)") # 输入提示Token数
    print(f"prompt eval duration: {stats['first_token_time']:.3f}s") # 首token响应时间
    print(f"prompt eval rate:     {stats['prompt_tokens']/stats['first_token_time']:.3f} tokens/s") # 模型响应速度
    print(f"eval count:           {stats['output_tokens']} token(s)") # 输出内容token数
    print(f"eval duration:        {stats['total_time']:.3f}s") # 总生成耗时
    print(f"eval rate:            {stats['output_tokens']/stats['total_time']:.3f} tokens/s") # 输出速度