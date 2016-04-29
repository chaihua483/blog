Title: Elasticsearch From Scratch
Date: 2015-12-20
Category: Useful Tools
Tag: ES, Mongo-connector, Elasticsearch

## 0. Working at Moseeker

&nbsp;&nbsp; When I started doing such an exciting and exhausting work, I had never considered we were making a huge change of our life. Nowadays, it is coming to realize our dream with the efforts building [Moseeker](http://www.moseeker.com). From the beginning I was playing as a developer, now I am taking part in some works related to products, more about data warehouse. After all, it is one of the biggest project in Moseeker and most important part, I think.

&nbsp;&nbsp; What I am doing now is develop an API to source our resumes. All is needed would be a Search Engine. Tools based on Lucene will be a decent choice as told. With the comparision of Solr and Elasticsearch (Abbreviated as ES), I chose ES to be our assistant.

## 1. Solr or ES, that won't be a problem.
&nbsp;&nbsp; While Solr and ES both perform as index tools. Each of them does have its advantages compared to the other one.

&nbsp;&nbsp; Here I won't spend much time explaining what is Solr or ES, you could get information at [Solr](http://lucene.apache.org/solr/) and [Elasticsearch](https://www.elastic.co/webinars/get-started-with-elasticsearch?elektra=home&storm=banner). I'm going to talk about the differences in every detail aspect.

&nbsp;&nbsp; This table is quoted from [solr-vs-elasticsearch.com](http://solr-vs-elasticsearch.com/)

Condition | Solr | ES
--|--|--
Data format|XML, CSV, json | json
JMX support| Yes | No
Product integration| More | Less
Output| More| Json only
Data import| JDBC, CSV, XML, Tika, URL, Flat File|Rivers modules: Git, MongoDB etc.
Analyzer chain| No | Yes
Multiple document types per schema| No | Yes
Hash-based deduplication | Yes| No
DSL| Inflexible | Wide usage
Aggregations | facet| aggs
Simpleness | Not well| Very much
Field declaration| Required | Automatical
Lots of fields| Not well | Recommended
Bulk upsert velocity| Slow | Quick

&nbsp;&nbsp; Now it is time to discuss my usage of the index tools. Our purpose is to sync the index with data in Mongo. A tool named [mongo-connector](https://github.com/mongodb-labs/mongo-connector) is used in this step. Mongo-connector will run a thread which reads from Mongo and upsert or update to index.

&nbsp;&nbsp; At first, I tried to deploy the system with Solr. When running with Solr, a statement must be written in XML to declare which fields to index and to store. For a nest object, this procudure might be complicated.

&nbsp;&nbsp; Another big problem is time consumption. Records already in Mongo need to sync at first, bulk upsert method will be used. Because of the storage ways of Mongo, data are separated info several collections, I ought to merge records related to one main record, which seems quite time-consuming.

&nbsp;&nbsp; There is the third trouble that usage of memory and CPU became really high and sometimes run into out-of-memory error.

&nbsp;&nbsp; To deal with time and space problem, we applied a new machine. And for simple using, Solr was replaced with ES. After that, everything gets easier.

## 2. Environment and Deployment
#### 2.0 A metion of Solr installation.

&nbsp;&nbsp; Download Solr from [apache solr](http://apache.fayea.com/lucene/solr/) and unzip the package. You can start or stop Solr with

```
 bin/solr start -e techproducts -noprompt
 bin/solr stop -all ; rm -Rf example/techproducts/
```

&nbsp;&nbsp; To sync data from Mongo, you need create a replica set of Mongo database as follows:

```
pkill mongod
mongod --replSet myDevReplSet
rs.initiate()
// well, some of the db need auth to local, so add one
db.grantRolesToUser(
  "admin",
  [
    { role: "read", db: "local" }
  ]
)
```

&nbsp;&nbsp; Modify `./server/solr/configsets/basic_configs/conf/schema.xml`

```
replace <uniqueKey>id</uniqueKey> to <uniqueKey>_id</uniqueKey>
add
<field name="_id" type="string" indexed="true" stored="true" ></field>
<field name="_ts" type="long" indexed="true" stored="true" ></field>
<field name="ns" type="string" indexed="true" stored="true"></field>
comment
<field name="id" type="string" indexed="true" stored="true" required="true" multiValued="false" ></field>
```

&nbsp;&nbsp; Modify `./server/solr/configsets/sample_techproducts_configs/conf/solrconfig.xml`, add luke request.

```
add <requestHandler name="/admin/luke" class="solr.admin.LukeRequestHandler" ></requestHandler>
```

#### 2.1 ES Configuration.
&nbsp;&nbsp; Regardless of Solr, we turn attention to deploy Elasticsearch.

&nbsp;&nbsp; Download ES at [the official website](https://www.elastic.co/downloads/elasticsearch). Unzip and run, that's all.

```
bin/elasticsearch
```

&nbsp;&nbsp; If you want to limit the IPs who can request for ES data, change the iptables.

```
-A INPUT -s XXX.XXX.XXX.XXX/32 -p tcp -m tcp --dport 9200 -j ACCEPT
```

&nbsp;&nbsp; ES configuration file locates at `./config/elasticsearch.yml`, you could define your application for yourself compared to the[ document](https://www.elastic.co/guide/en/elasticsearch/reference/1.4/setup-configuration.html)

#### 2.2 Mongo connector
&nbsp;&nbsp; [Mongo connector](https://github.com/mongodb-labs/mongo-connector/wiki) is an extremely useful tool for syncing records between mongo and search engine. With the help of connector, we are able to setup a bridge from Mongo database to Index.

&nbsp;&nbsp; To install Mongo-connector, just use

```
pip install mongo-connector
```

&nbsp;&nbsp; Mongo-connector starts a new thread for upserting or updating index with the change of Mongodb, with which we are able to sync data. To run the thread, run script:

```
$ mongo-connector -m XXX.XXX.XXX.XXX:27017 --admin-username admin --password password -n dbX.collectionX,dbX.collectionY  --auto-commit-interval=0 -d my_es_docmanager -t http://XXX.XXX.XXX.XXX:9200
```
&nbsp;&nbsp; Param `-m` points to the location of Mongodb. `-n` indicates collections you want to index. `-d` chooses a docmanager to tranform data format. Make sure that you are taking an admin account of Mongodb.

&nbsp;&nbsp; It is the most flexable and convenient of Mongo-connector when customizing your own docmanager. Docmanagers usually locates in

```
XXX/python2.7/dist-packages/mongo_connector/doc_managers/
```
&nbsp;&nbsp; You can copy a `elastic_doc_manager.py` and rewrite functions in the module such as `upsert`, `update`, `remove`, `bulk` etc.

#### 2.3 Python-elasticsearch
&nbsp;&nbsp; There is a python package `elasticsearch` (here we simply name it `pyes`) for us to operate es instead of sending requests directly. It is recommended to use this package cause it seems easier to control user access.

&nbsp;&nbsp; Installation is easy,

```
pip install elasticsearch
```
&nbsp;&nbsp; With Clients provided by `pyes`, we create index with client `IndicesClient`, submit query request with method `search` from `Elasticsearch` class.

&nbsp;&nbsp; Here is an example for searching.

```
elastic = Elasticsearch(
            hosts=[url], **kwargs.get('clientOptions', {}))
result = elastic.search(index='resume', doc_type='resume', body=json.dumps(body))
```

#### 2.3 Customize index configuration
&nbsp;&nbsp; If you consider your elasticsearch as an online product, it is better to setup a fixed setting for the index rather than let ES make decisions. It is not a must for mappings could be added whenever you want with [Put mapping API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html). Within the `mapping` option, every field could set its own properties. Here is an example:

```
elasticsearch.indices.create(index=index,
    body = {
        "mappings": {
            "resume": {
                "properties": {
                    "info": {
                        "type": "nested",
                        "properties": {
                            "qq": {"type": "string"}
                        }
                    },
                    "mobile": {"type": "string"}
                }
            }
        }
    }
)
```

&nbsp;&nbsp; It is worth metioning that if one of the fields is recognized as `date` automatically, documents of it must have the same format and could not be `null`. If you manually set fields type as `date` and set `format` to multiple forms, you could upsert any type you want. Read [Date Format](https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html#date-params) to learn more about field `date`.

&nbsp;&nbsp; With the interface, you can also set how many shards should be used for indexing. More details [Here](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html)

#### 2.4 Bulk

&nbsp;&nbsp; ES provides bulk APIs for us to operate with large mounts of documents. See [details](https://elasticsearch-py.readthedocs.org/en/master/api.html?highlight=bulk#elasticsearch.Elasticsearch.bulk).


## 3. DSL queries

&nbsp;&nbsp; Sending requests of `get` will obtain documents you want, but using DSL might be safer and more formal. DSL jsons are packeged in function `elasticsearch.search()`, usage as follows:

```
elasticsearch.search(
    index=index,
    doc_type="resume",
    body={
        "query": {
            "match_all": {}
        }
    }
)
```

&nbsp;&nbsp; Of course you can put `index` and `doc_type` into `body` so that the query will support multi-index and multi-type. Good DSL queries could lead to any result you wish to get.

&nbsp;&nbsp; I am not going to write this part like a document API, instead, I am seeking for proper query from requirements externally which are about personal profiles. We assume a profile like this:

```
{
    "id": "12345",
    "info": {
        "name": "Nick",
        "birthday": "19881001"
    },
    "education": [
        {
            "from": "20111212",
            "to": ""
        }
    ]
}
```

#### 3.1 Find proper profiles on some keywords

&nbsp;&nbsp; To search profiles contains `java` and `android`, send

```
{
    "query":{
        "match":{"_all": "java android"}
    }
}
```









