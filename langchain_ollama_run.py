import subprocess
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

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

def model_inference(model_name):
    llm = ChatOllama(
        model = model_name,
        temperature = 0.8,
        num_predict = 256,
    )

    
    template = """
    Question: {question}
    Answer: 请一步一步思考
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    response = chain.invoke({"question": "What is LangChain?"})
    print(response.content)

    # model = OllamaLLM(model='deepseekv2-lite-chat')
    # print(model.invoke("Come up with 10 names for a song about parrots"))

if __name__ == "__main__":
    model_name = "deepseekv2-lite-chat"
    # 运行模型
    run_ollama_model(model_name)
    model_inference(model_name)
    # 停止模型
    stop_ollama_model(model_name)
