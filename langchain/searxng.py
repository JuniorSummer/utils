from langchain_community.utilities import SearxSearchWrapper

# print(search.run("《王者荣耀》这款游戏是什么时候发行的"))
search = SearxSearchWrapper(searx_host="http://localhost:9003/")
query = "今天是几号"
results = search.results(
    query,                                  # 搜索内容
    language="zh-CN",                       # 语言
    safesearch=0,                           # 可选0(不过滤任何结果),1(中等级别内容过滤),2(严格级别内容过滤)
    categories="general",                   # 搜索内容，取值general/images/videos等
    engines=["baidu", "bing", "brave"],    # 搜索引擎
    num_results=3                           # 返回内容数
)
print(f"search results: {results}")
