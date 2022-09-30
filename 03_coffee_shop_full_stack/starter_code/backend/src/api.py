import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from flask import Flask, request

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError,requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''



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
#this endpoint give you all drinks
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
@requires_auth('get:drinks-detail')
#this endpoint give you all drinks with persmzssion get 
def aux(payload):
 
  drinks=Drink.query.all()

  
  return jsonify({
        'success': True,
        'drinks': [i.short() for i in drinks]}), 200 

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
#this endpoint help you post new drink
@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def adddrink(payload):
  try:
  
   drink=Drink()
   req = request.get_json()
   drink.title=req['title']
   
   drink.recipe=json.dumps(req['recipe'])
   print(type(req['recipe']))
   print(req['recipe'])
   
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
#this endpoint  =help you modify drinks
@app.route('/drinks/<drink_id>',methods=['PATCH'])
@requires_auth('patch:drinks')
def modifycoffe(payload,drink_id):

 req=request.get_json()
 try:
  drink_id=int(drink_id)
 
  alle=Drink.query.all()
  aux=0
  for i in alle:
   if int(i.id)==int(drink_id):
     break
   
  r=i 
  
 
  
  if not r:
   abort(404)

  if(req['title']): 
   r.title=req['title']
  
 
  if req['recipe'] is None:
  
   r.update()
  else:
    r.recipe=json.dumps(req['recipe'])
    print(json.dumps(req['recipe']))
 
 
  print("final")
  r.update()

 except Exception:
        abort(400)
 
 return jsonify({'success': True, 'drinks': [r.long()]}), 200

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
@requires_auth('delete:drinks')
def delete(payload,idt):
 
  drink = Drink.query.filter(Drink.id ==idt).one_or_none()
  if not drink:
   abort(404)
  try:
   drink.delete()
  except Exception:
   abort(404)
  return  jsonify({"success": True, "delete": idt})
 
  
   
   
  
 
 




# Error Handling
'''
Example error handling for unprocessable entity
'''

#handel the 422 error
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
#handel the 404 error
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

#handel authintication error
@app.errorhandler(AuthError)
def auth_error(error):
    print(error)
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

#handel the 401  error
@app.errorhandler(401)
def unauthorized(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


