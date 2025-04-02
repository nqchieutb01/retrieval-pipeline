from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, MilvusClient, utility

class MilvusClientCustom:
    def __init__(self, host: str = "milvus_standalone", port = 19530):

        connections.connect(host=host, port=port)
        # self.client = MilvusClient(host=host, port=port)
        self.collection_name = "retrieval_1"
        self.dim = 384  # Dimension of BGE-M3 embeddings
        if not self._collection_exists():
            self._create_collection()
        else:
            self.collection = Collection(self.collection_name)
        
        index_params = {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 128}}
        self.collection.create_index("embedding", index_params)
        self.collection.load()

    def _collection_exists(self):
        return utility.has_collection(self.collection_name)

    def _create_collection(self):
        fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=50000)
            ]
        schema = CollectionSchema(fields, "Semantic Search Collection")
        index_params = {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 128}}
        self.collection = Collection(self.collection_name,schema)
        self.collection.create_index("embedding", index_params)

        # self.client.create_collection(collection_name="retrieval", schema=schema,index_params= index_params)

    def insert(self, text: str, embedding):
        entity = [
            {
                "embedding": embedding,
                "text": text
            }
        ]
        self.collection.insert(entity)
 
    def search(self, query_embedding, top_k: int = 10):
        search_params = {"metric_type": "L2", "params": {"nprobe": 16}}
        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding", 
            limit=3, 
            param=search_params,
            output_fields=["text"]
        )
        return results