from models.core import *

class Gendata:
    def create_consumer(self):
        consumer = Consumer(name="Consumer 1")
        consumer.put()
        consumer = Consumer(name="Consumer 2")
        consumer.put()
        consumer = Consumer(name="Consumer 3")
        consumer.put()

    def create_supplier(self):
        supplier = Supplier(name="Supplier 1")
        supplier.put()
        supplier = Supplier(name="Supplier 2")
        supplier.put()
        supplier = Supplier(name="Supplier 3")
        supplier.put()
        supplier = Supplier(name="Supplier X")
        supplier.put()

    def create_dataformat(self):
        data_format=DataFormat(name="in1", semantics="some input")
        data_format.put()
        data_format=DataFormat(name="out1", semantics="some output")
        data_format.put()
    
    def create_algorithm(self):
        in_format=DataFormat.query(DataFormat.name == "in1").fetch(1)
        out_format = DataFormat.query(DataFormat.name == "out1").fetch(1)
        suppliers = Supplier.query().fetch(10)
        alg_names = ["alg1", "alg2", "alg3"]
        for s in suppliers:
            for alg_name in alg_names:
                algorithm=Algorithm(name=alg_name+"_"+s.name,
                                semantics="sem1",
                                source_code="code1",
                                version="1.0",
                                supplier=s.key,
                                input_format=in_format[0].key,
                                output_format=out_format[0].key)
                algorithm.put()

    def empty_table(self, kind_name):
        entity_class = globals()[kind_name]
        entity_query = entity_class.query()
        entities = entity_query.fetch()
        for e in entities:
            e.key.delete()

        




