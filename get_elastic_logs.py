from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime, timedelta, timezone
from re import search

load_dotenv()

def get_elasticsearchdata():
    indexer_es = Elasticsearch([os.getenv("ELASTIC_URL")],
                               basic_auth=(os.getenv("ELASTIC_USERNAME"), os.getenv("ELASTIC_PASSWORD")),
                               verify_certs=False)
    print("Elasticsearch connection is successful")
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "wildcard": {
                            "sitename": "**"
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "now-1m"
                            }
                        }
                    }
                ]
            }
        }
    }

    part_of_index = scan(client=indexer_es,
                         query=query,
                         index=('*'),
                         raise_on_error=True,
                         preserve_order=False,
                         clear_scroll=True
                         )

    result = list(part_of_index)

    temp = []
    # We need only '_source', which has all the fields required.
    # This elimantes the elasticsearch metdata like _id, _type, _index.
    for hit in result:
        temp.append(hit['_source'])

    df = pd.DataFrame(temp)

    return df


df = get_elasticsearchdata()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
df.columns.values.tolist()

print(df)

