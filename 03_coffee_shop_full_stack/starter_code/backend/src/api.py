import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from flask import Flask, request

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError,requires_auth
from collections.abc import Mapping
app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()


'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/')
def index():
  return '<h1>hello, you are succesfully connected </h1>'
@app.route('/drinks')
def drink():
 drinks=Drink.query.all()

 
 return jsonify({
        'success': True,
        'drinks': [d.short() for d in drinks]
        }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])

def aux():
  requires_auth('get:drinks-detail')
  drinks=Drink.query.all()

  
  return jsonify({
        'success': True,
        'drinks': [d.short() for d in drinks]
    }), 200 

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',methods=['POST'])
def adddrink():
  try:
   requires_auth('post:drinks')
   drink=Drink()
   req = request.get_json()
   drink.title=req['title']
   drink.recipe=json.dumps(req['recipe'])
   drink.insert()
  except:
   abort(400) 
  
  return jsonify({'success': True,'drinks':[drink.long()]})
 


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>',methods=['PATCH'])
def modifycoffe(drink_id):
 requires_auth('patch:drinks')
 req=request.get_json()
 try:
  drink_id=int(drink_id)
  drink = Drink.query.filter(Drink.id ==drink_id).one_or_none()
  if not drink:
   abort(404)
  if(req['title']): 
   drink.title=req['title']
  print(",kkkk")
  if req.dumps(req['recipe']):
   drink.recipe=req.dumps(req['recipe'])
  db.session.commit()
  drink.update()
  print(",kkkk")
 except Exception:
        abort(400)
 
 return jsonify({'success': True, 'drinks': [drink.long()]}), 200

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<idt>',methods=['DELETE'])
def delete(idt):
  requires_auth('delete:drinks')
  drink = Drink.query.filter(Drink.id ==idt).one_or_none()
  if not drink:
   abort(404)
  try:
   drink.delete()
  except Exception:
   abort(404)
  return   {"success": True, "delete": idt}
  
   
   
  
 
 




# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(401)
def unauthorized(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


