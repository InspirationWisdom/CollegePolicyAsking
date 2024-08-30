from elasticsearch import Elasticsearch

# Password for the 'elastic' user generated by Elasticsearch

# Create the client instance
client = Elasticsearch(
    hosts="http://localhost:9200"
)

'''
#功能：搜索文本
#参数：index:索引名称
#     query:搜索关键词
#     start:搜索结果的起始位置(默认为0)
'''


def search_text(index, query, start=0):
    # 如果搜索关键词为空，则获取所有全部内容，同时按照时间排序
    if query == '':
        request_body = {
            "query": {
                "match_all": {}
            },
            "sort": [
                {
                    "notice_time": "desc"
                }
            ],
            "size": 10,  # 返回前10条数据
            "from": start
        }
    else:
        request_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["notice_title", "notice_text"]
                }
            },
            "sort": [
                {"_score": {"order": "desc"}},
                {"notice_time": {"order": "desc"}}
            ],
            "size": 10,  # 返回前10条数据
            "from": start
        }

    resp = client.search(index=index, body=request_body)
    return resp


'''
功能：获取指定文本的记录总数
参数：index:索引名称
    query:搜索关键词
'''


def get_total(index, query):
    # 如果搜索关键词为空，则获取所有全部内容
    if query == '':
        request_body = {
            "query": {
                "match_all": {}
            }
        }
    else:
        request_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["notice_title", "notice_text"]
                },
            },

        }

    resp = client.count(index=index, body=request_body)
    return resp['count']

print(search_text('notices', '贫困补助'))
print(get_total('notices', '贫困补助'))
