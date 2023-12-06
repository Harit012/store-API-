from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema, StoreUpdateSchema

blp = Blueprint("Tags","tags",description="Operations on tags")

