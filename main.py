import json
import os
import secrets
from flask_pymongo import PyMongo
from flask import Flask,jsonify, request, make_response, Response
import pymongo
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_header, create_refresh_token
from bson.objectid import ObjectId


app = Flask(__name__)
JWTManager(app)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["MONGO_URI"] = "mongodb+srv://gost:ade12345@cluster0.drav2vj.mongodb.net/flask_data?retryWrites=true&w=majority"
# app.config["JWT_SECRET_KEY"] =

# mongo_cl = MongoClient("mongodb+srv://gost:PhMPHLprzK5edJu0@cluster0.drav2vj.mongodb.net/?retryWrites=true&w=majority")
# db = mongo_cl["flask_data"]
# collection = db["user"]

client = PyMongo(app)
db = client.db


@app.post("/register")
def register():
    body = {
    "first_name" : request.json.get("first_name"),
    "last_name" : request.json.get("last_name"),
    "email" :request.json.get("email"),
    "password" : request.json.get("password")
      }
    # try:
    new_user = db.user.insert_one(dict(body)) 
    
    # collection.insert_one(dict(body))
    # except Exception:
    #     pass
    # finally:
    # return jsonify({"Headers" : {
    #             'Accept': 'application/json',
    #             'Content-Type': 'application/json',
    #             # "user": get_jwt_header()          
    #           },
    #             "body": body,
              
    #           }), 200

    return Response(
      response=json.dumps({"message": "new user created ","id":f"n{new_user.inserted_id}",
      "body": body }),
      status=200,
      mimetype="application/json"
    )

@app.post("/login")
def login():
  # user = request.authorization


  req_user = request.json.get("email")
  req_pass = request.json.get("password")
  reg_user =db.user.find_one({"email":req_user})
  if reg_user:
        if reg_user.get("password") == req_pass:
              
              return jsonify({"Success": "Successfully signed in",
              })
        else :
              return jsonify({"error": "Wrong credentials"})

  else:
        return jsonify({"error": "No matching email"})
        
  

@app.get("/template")
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
                  response=json.dumps({"message": "details updated for ","id":f"n{template_id}",
      "body": "updated" }),
      status=200,
      mimetype="application/json"
            )
      # return jsonify({"Successfully replaced"})


@app.delete("/delete/<template_id>")
def delete_template(template_id):
      db.template.find_one_and_delete({"id":ObjectId(template_id)})
      try:
        templates = list(db.template.find())
        for template in templates:
              template["_id"] = str(template["_id"])
        print(templates)
      except Exception:
        pass
       
      # return jsonify({template for template in templates})
      return Response(response=json.dumps({"Message":f"content of id {template_id} deleted successfully",
            "body":templates}),
      status=500,
      mimetype="application/json"
      )
      # return jsonify({"deleted succcessfully"})


# @app.get("/chop-sticks")
# def chopstick(chopstick_id=None):
#     if not chopstick_id:
#         message = jsonify(message='"chopstick_id" missing')
#         return make_response(message, 400)

#     return jsonify(
#         id=chopstick_id,
#         color='bamboo',
#         left_handed=True,
#     )


print(__name__)
if __name__ == "__main__":
    app.run(debug=True)