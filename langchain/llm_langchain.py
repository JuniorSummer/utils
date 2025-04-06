from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

# 检查是否有可用的GPU/NPU
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"有 {torch.cuda.device_count()} 个GPU可用")
else:
    device = torch.device("cpu")
    print("使用CPU")

# 通过离线方式加载huggingface中的开源模型
model_dir = '../packages/DeepSeek-R1-Distill-Qwen-1.5B'
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    torch_dtype="auto",
    device_map="auto"
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=512,
    temperature=0.8,
    top_p=1,
    repetition_penalty=1.15
)
llm = HuggingFacePipeline(pipeline=pipe)
# print(llm.invoke("王者荣耀是什么时候推出的？"))

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的AI助手"),
    ("user", "{input}")
])
chain = prompt | llm
print(chain.invoke({"input": "王者荣耀是什么时候推出的？"}))

loader = PyPDFLoader("./28-2024年浙江省特殊食品监督抽检分析报告-提交版.pdf")
pages = loader.load_and_split()
# 查看加载后的文档
print(pages)

docs = ""
for item in pages:
    docs += item.page_content
    docs + "\n"

embeddings_path = 'moka-ai/m3e-base'
embeddings = HuggingFaceEmbeddings(model_name=embeddings_path)
vectorStoreDB = FAISS.from_documents(docs, embedding=embeddings)
print(vectorStoreDB)

# 加载问答链
qa_chain = load_qa_chain(llm, chain_type="stuff")
# 定义问题
question = "文档中关于某个关键内容的描述是什么？"
# 从向量数据库中检索相关文档
similar_docs = vectorStoreDB.similarity_search(question)
# 使用问答链进行问答
answer = qa_chain.run(input_documents=similar_docs, question=question)

print(f"问题: {question}")
print(f"答案: {answer}")   
