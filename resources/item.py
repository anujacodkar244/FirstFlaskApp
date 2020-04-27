from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):
    parser= reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank!"
        )
    parser.add_argument('store_id',
            type=int,
            required=True,
            help="Every Item needs a store id"
    )
    @jwt_required()
    def get(self, name):
        # # for item in items:
        #     # if item['name'] == name:
        #     #     return item
        # item=next(filter(lambda x: x['name']==name, items),None)
        # return {'item': item},200 if item else 404

        #Keeping the Items dictionary in database
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return  {'message': 'item not found'}, 404

    


    def post(self, name):
        #Writing items to the database (data.db)
        if ItemModel.find_by_name(name):
            return {'message':"item with name '{}' already exists".format(name)}, 400
        
        data=Item.parser.parse_args()
        item = ItemModel(name, **data)
        #items.append(item)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting item"}, 500
        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item is deleted'}
        

    def put(self, name):
        data=Item.parser.parse_args()
        #data = request.get_json()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price'] 
        
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items':list(map(lambda x: x.json(), ItemModel.query.all()))}
