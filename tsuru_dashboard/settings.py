import os


TSURU_HOST = os.environ.get("TSURU_HOST", "http://localhost:8080")
ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST", "http://localhost:9200")
