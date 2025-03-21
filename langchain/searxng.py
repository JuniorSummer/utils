from langchain_community.utilities import SearxSearchWrapper

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

    for result in results:
        print(f"Snippet: {result['snippet']}")
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print(f"Source: {result['engines']}")
        print("------------------------------")
