from __future__ import unicode_literals

#from django.db import models
from google.appengine.ext import ndb


class Supplier(ndb.Model): # todo
    name = ndb.StringProperty()

class Consumer(ndb.Model):  # todo
    name = ndb.StringProperty()


class DataFormat(ndb.Model):  # todo
    name = ndb.StringProperty()
    semantics = ndb.StringProperty()

class DataCollection(ndb.Model):
    name = ndb.StringProperty()

class DataSet(DataCollection):
    data_name = ndb.StringProperty()

class ResultSet(DataCollection):
    result_name = ndb.StringProperty()

class Resource(ndb.Model):
    name = ndb.StringProperty()

class Storage(Resource):
    mb = ndb.FloatProperty()

class CPU(Resource):
    cycles = ndb.FloatProperty()

class Billing(ndb.Model):
    name = ndb.StringProperty()
    supplier = ndb.KeyProperty(kind=Supplier, name="billings")
    consumer = ndb.KeyProperty(kind=Consumer, name="billings")

class Algorithm(ndb.Model):
    name = ndb.StringProperty()
    semantics = ndb.StringProperty()
    source_code = ndb.StringProperty()
    version = ndb.StringProperty()
    supplier = ndb.KeyProperty(kind=Supplier, name="algorithms")
    input_format = ndb.KeyProperty(kind=DataFormat, name="algorithms_input")
    output_format = ndb.KeyProperty(kind=DataFormat, name="algorithms_output")

class AlgorithmExecution(ndb.Model):
    consumer = ndb.KeyProperty(kind=Consumer, name="algorithm_executions")
    algorithm = ndb.KeyProperty(kind=Algorithm, name="algorithm_executions")
    result_set = ndb.KeyProperty(kind=ResultSet, name="algorithm_executions")
    data_set = ndb.KeyProperty(kind=DataSet, name="algorithm_executions")
    resource = ndb.KeyProperty(kind=Resource, name="algorithm_executions")

class BillingRecord(ndb.Model):
    billing = ndb.KeyProperty(kind=Billing, name="billing_records")
    resource = ndb.KeyProperty(kind=Resource, name="billing_records")
    algorithm_execution = ndb.KeyProperty(kind=AlgorithmExecution, name="billing_records")
    amount = ndb.FloatProperty()