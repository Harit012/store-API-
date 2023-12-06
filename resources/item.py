import sys
import uuid
import traceback
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema,ItemUpdateSchema

blp = Blueprint("items", __name__ ,description="operations on items")

@blp.route("/item")
class ItemList(MethodView):
    
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        item = ItemModel(**item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            etype, value, tb = sys.exc_info()
            print(traceback.print_exception(etype, value, tb))
            abort(500,message="An error occurred while inserting the item\n {}".format(SQLAlchemyError))
        
        return item


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    def delete(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"Message":"Item Deleted"}
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id,**item_data)
        
        db.session.add(item)
        db.session.commit()
        return item

    