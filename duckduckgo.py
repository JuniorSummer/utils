from duckduckgo_search import DDGS
from pprint import pprint

with DDGS() as ddgs:
    pprint([r for r in ddgs.text("大模型", region='cn-zh', max_results=10)])

ddgs = DDGS(proxy="socks5://user:password@geo.iproyal.com:32325", timeout=20)
results = ddgs.text("你需要的内容", max_results=50)
print(results)
