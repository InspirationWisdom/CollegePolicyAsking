import datetime
from elasticsearch import Elasticsearch

# Create the client instance
client = Elasticsearch(
    "https://localhost:9200",
)

# Successful response!
# {'name': 'instance-0000000000', 'cluster_name': ...}
print(client.info())

doc = {
    'author': 'author_name',
    'text': 'Interesting content...',
    'timestamp': datetime.datetime.now(),
}

#创建索引
resp = client.index(index="test-index", id=1, body=doc)
print(resp['result'])

#获取文档
resp = client.get(index="test-index", id=1)
print(resp['_source'])

#刷新索引
client.indices.refresh(index="test-index")

#搜索文档
resp = client.search(index="test-index", query={"match_all": {}})
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

#更新文档
doc = {
    'author': 'author_name',
    'text': 'Interesting modified content...',
    'timestamp': datetime.datetime.now(),
}
resp = client.update(index="test-index", id=1, doc=doc)
print(resp['result'])

#删除文档
client.delete(index="test-index", id=1)
