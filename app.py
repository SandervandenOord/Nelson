# create first version of REST API for ziengs data
# most important: 
# with /product_details/<string:url_join> you can get the positions of products on their site
# url is in the form: signatura-veterschoen_cognac_11399.html

from flask import Flask 
from flask_restful import Resource, Api
from sqlalchemy import create_engine

e = create_engine('sqlite:///ziengs.db')

app = Flask(__name__)
api = Api(app)

class Categories(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute("select distinct product_category from product_pages4")
        return {'categories': [i[0] for i in query.cursor.fetchall()]}

class Category_Details(Resource):
    def get(self, product_category):
        conn = e.connect()
        query = conn.execute("select * from product_pages4 where product_category='%s'" %product_category)
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
 
class Product_Details(Resource):
    def get(self, url_join):
        conn = e.connect()
        query = conn.execute("select * from product_positions4_result where url_join='%s' order by product_category" %url_join)
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result 
 
api.add_resource(Category_Details, '/prod_cat/<string:product_category>')
 
api.add_resource(Categories, '/categories')

api.add_resource(Product_Details, '/product_details/<string:url_join>')

if __name__ == '__main__':
     app.run()


