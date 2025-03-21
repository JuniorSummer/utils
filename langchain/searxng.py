from langchain_community.utilities import SearxSearchWrapper
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.schema import HumanMessage

def searxng_search(query):
    search = SearxSearchWrapper(searx_host="http://localhost:9003/")
    results = search.results(
        query,                                  # 搜索内容
        language="zh-CN",                       # 语言
        safesearch=2,                           # 可选0(不过滤任何结果),1(中等级别内容过滤),2(严格级别内容过滤)
        categories="general",                   # 搜索内容，取值general/images/videos等
        engines=["baidu", "360search", "bing", "sougo", "bing_news"],    # 搜索引擎
        num_results=5                          # 返回内容数
    )

    # print(f"search results: {results}")

    return results


if __name__ == "__main__":
    query = "langchain如何搭建大模型"
    results = searxng_search(query)

    # print(type(results))

    for result in results:
        print(f"Snippet: {result['snippet']}")
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print(f"Source: {result['engines']}")
        print("------------------------------")
    
    prompt_template = PromptTemplate(
    input_variables=["snippet1", "link1", "snippet2", "link2", "snippet3", "link3"],
    template="""
    请结合检索到的三个相关度最高的网页内容生成合适的回复：
    第一个网页摘要：{snippet1}
    第一个网页链接：{link1}

    第二个网页摘要：{snippet2}
    第二个网页链接：{link2}

    第三个网页摘要：{snippet3}
    第三个网页链接：{link3}
    """
    )

    # TODO：补充本地模型调用方式
    chat_llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=0.7,
        max_tokens=200
        )

    chain = LLMChain(
        llm=chat_llm,
        prompt=prompt_template
        )
    
    result = chain.run(
        snippet1="results[0]['snippet']",
        link1="results[0]['link']"
        snippet2="results[1]['snippet']",
        link2="results[1]['link']",
        snippet3="results[2]['snippet']",
        link3="results[2]['link']"
        )
    
    print(result)
