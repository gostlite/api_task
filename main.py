import json
import os
import secrets
from functools import wraps
from time import sleep
from flask_pymongo import PyMongo
from flask import Flask,jsonify, request, make_response, Response, redirect
import jwt
from bson.objectid import ObjectId

app = Flask(__name__)
JWTManager(app)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["MONGO_URI"] = f"mongodb+srv://gost:{os.environ.get("pass")}@cluster0.drav2vj.mongodb.net/flask_data?retryWrites=true&w=majority"

client = PyMongo(app)
db = client.db



  
# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header

        """new lines again """
        if 'x-access-token' in token1:
            token = token1['x-access-token']
            # token['exp'] = int(token["exp"])
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            # data = 
            data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
            # current_user = db.user.find_one(data["public_id"])
            # User.query\
            #     .filter_by(public_id = data['public_id'])\
            #     .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!',"token": jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
            }), 401
        # returns the current logged in users contex to the routes
        return  f(*args, **kwargs)
  
    return decorated
"""Set a decorator function to check user auth"""
def auth_req(f, **kwargs):
    @wraps(f, **kwargs)
    def deco(*args, **kwargs):
        temp = json.dumps(db.template.find_one({"_id":ObjectId(kwargs["template_id"])}), default=str)
        temp = json.loads(temp)
        # temp_owner = temp.get("template_owner")
        # temp_owner = temp.get("template_owner")
        if jwt.decode(token1["x-access-token"],key=app.config["SECRET_KEY"], algorithms='HS256')["public_id"] != temp["template_owner"]:
            return jsonify({"message": "Sorry you cannot edit or delete this file","ERROR":"NOT OWNER"})
        return f(*args, **kwargs)
    return deco

@app.route("/")
def home():
      return jsonify(response=json.dumps({"message": "Welcome here!!! Pls use postman and body should be json"
      "kindly register with /register, and login with /login, you cannot access"
      "the templates without login in."}), status=200, 
      mimetype="application/json")

@app.post("/register")
def register():
    try:
        body = {
        "first_name" : request.json.get("first_name"),
        "last_name" : request.json.get("last_name"),
        "email" :request.json.get("email"),
        "password" : request.json.get("password")
        }
    except:
        return json({"ERROR": "Pls use all key:{first_name, last_name, email and passwor}"})
    # try:
    new_user = db.user.insert_one(dict(body)) 
    
    return Response(
      response=json.dumps({"message": "new user created ","id":f"{new_user.inserted_id}",
      "body": body }),
      status=200,
      mimetype="application/json"
    )

@app.post("/login")
def login():
  # user = request.authorization


    try:
        req_user = request.json.get("email")
        req_pass = request.json.get("password")
    except:
        return jsonify({"ERROR":"Kindly use the keys {email and password to login}"})
    reg_user =db.user.find_one({"email":req_user})
    if reg_user:
        if reg_user.get("password") == req_pass:
            token = jwt.encode({
            'public_id': str(reg_user['_id']),
        }, app.config['SECRET_KEY'], algorithm='HS256')

            """added new line"""
            global token1
            token1 = dict(request.headers)
            token1["x-access-token"] = token

           
  
            return make_response(jsonify({ "message": "You have successfully logged in, use /template for all," 
            "/newtemplate to add new template and /delete/<key>", "how to add template": "when adding a new template,"
            "kindly use the key:{template_name, subject and body}using json" ,"header": token1, 
            "id": str(reg_user['_id'])}), 201)
        
            #   return jsonify({"Success": f"Successfully signed in {str(reg_user['_id'])} ",
            #   })

        else :
              return jsonify({"error": "Wrong credentials"})

    else:
        return jsonify({"error": "No matching email"})


@app.post("/newtemplate")
@token_required
def new_temp():
    # jwt.decode(token1["x-access-token"],key=app.config["SECRET_KEY"], algorithms='HS256')["public_id"],
    template = {"template_name":request.json.get("template_name"),
    "template_owner": jwt.decode(token1["x-access-token"],key=app.config["SECRET_KEY"], algorithms='HS256')["public_id"],
    "subject": request.json.get("subject"),
    "body":request.json.get("body")}
    tempy = db.template.insert_one(template)
    return jsonify({"Owner id":template.get("template_owner")," body":f"successfully created a new template with id {tempy.inserted_id}"})
    

@app.route("/template")
@token_required
def alltemplates():
      try:
        templates = list(db.template.find())
        for template in templates:
              template["_id"] = str(template["_id"])
        print(templates)
      except Exception:
        pass
       
      # return jsonify({template for template in templates})
      return Response(response=json.dumps(templates),
      status=500,
      mimetype="application/json"
      )


@app.put("/template/<template_id>")
@token_required
@auth_req
def get_template(template_id):
      # template_update = request.args.get("template_id")
      try:
            db.template.find_one_and_replace({"_id":ObjectId(template_id),#serialize object id
            "template_name":request.json.get("template_name"),
            "subject": request.json.get("subject"),
            "body":request.json.get("body")})
      except Exception:
            pass
      finally:
            return Response(
                  response=json.dumps({"message": "details updated for ","id":f"{template_id}",
      "body": "updated" }),
      status=200,
      mimetype="application/json"
            )


@app.delete("/delete/<template_id>")
@token_required
@auth_req
def delete_template(template_id):
      db.template.find_one_and_delete({"_id":ObjectId(template_id)})
      try:
        templates = list(db.template.find())
        for template in templates:
              template["_id"] = str(template["_id"])
        print(templates)
      except Exception:
        pass
       
      # return jsonify({template for template in templates})
      Response(response=json.dumps({"Message":f"content of id {template_id} deleted successfully",
            "body":templates}),
      status=500,
      mimetype="application/json"
      )
      import time
      time.sleep(3)
      return redirect("/template")
      # return jsonify({"deleted succcessfully"})


print(__name__)
if __name__ == "__main__":
    app.run()
