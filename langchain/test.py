from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

loader = PyPDFLoader("/root/llm/28-2024年浙江省特殊食品监督抽检分析报告-提交版.pdf")
pages = loader.load_and_split()
# 查看加载后的文档
print(pages)

docs = ""
for item in pages:
    docs += item.page_content
    docs + "\n"

embeddings_path = "/root/packages/m3e-small/"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_path)
vectorStoreDB = FAISS.from_documents(pages, embedding=embeddings)
print(vectorStoreDB)
