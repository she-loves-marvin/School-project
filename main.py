from flask import Flask,request,jsonify,render_template
from intasend import APIService
import requests
import psycopg2
import schedule
import json
import os
import time
import hashlib
import secrets



#create flask app
app=Flask(__name__)



#establish database connection
connection_string = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(connection_string)
cursor= conn.cursor()
print("connection secured...")



def generate_salt():
    return secrets.token_hex(16)


def hash_password(password,salt):
    salted_password = password + salt
    hashedpassword=hashlib.sha256(salted_password.encode()).hexdigest()
    return hashedpassword

#STK push for the amount to be sent from clients mpesa number to our accounts
def apicall(number,amount):
  try: 
      url="https://tinypesa.com/api/v1/express/initialize"
      details={
          "amount": amount,
          "msisdn": number
      }
      payload =json.dumps(details)
      apikey=os.environ.get("apikey")
      header={
          "Content-Type":"application/json",
          "Apikey": apikey
      }
      response=requests.post(url,data=payload,headers=header)
      if response.status_code ==200:
          print("STK push sucess")
      else:
          print(response.json())
  except Exception as e:
      app.logger.error(f'An error occurred: {e}')

#root page directed to the user to authenticate themselves
@app.route('/',methods=['GET'])
def renderloginpage():
        try:
            return render_template('login.html')
        except Exception as e:
            print(f"an error occurred :{e}")
@app.route('/',methods=['POST'])
def login():
    try:
        data=request.get_json()
        email=data.get('email')
        password=data.get('password')
        query="SELECT * FROM Project WHERE email = %s LIMIT 1"
        cursor.execute(query,email)
        feedback =cursor.fetchone()
        hashpass=feedback[1]
        salt=feedback[2]
        passkey=hash_password(password,salt)
        if feedback is not None:
            if hashpass==passkey:
               return render_template('home.html')
            else:
                response= jsonify({"Data":"The password you entered is not correct.Please try again!!!"})
                return response
        else:
            response = jsonify({"Data":"The account under this email does not exist.PLease got to the sign up page and create a new account"})
            return response
    except Exception as e:
        print(f"An error occurred: {e}")

#signup page for new users
app.route('/signup',methods=['GET'])
def login():
    return render_template('signup.html')
app.route('/signup',methods=['POST'])
def signup ():
    try:
        data=request.get_json()
        email=data.get('email')
        password=data.get('password')
        salt=generate_salt()
        passkey=hash_password(password,salt)
        confirmation="SELECT * FROM project WHERE email = %s LIMIT 1"
        cursor.execute(confirmation,email)
        result=cursor.fetchone()
        if result is None:
            query="INSERT INTO Project (email,passkey,salt) VALUES (%s, %s, %s )"
            cursor.execute(query,(email,passkey,salt))
            conn.commit()
            cursor.close()
            conn.close()
            return render_template('login.html')
        else:
            response=jsonify({"Data":"The account corresponding to the email address you entered already exists"})
            return response
    except  Exception as e:
        print(f"An exception occurred: {e}")


#homepage logic behind budgeting

@app.route('/homepage',methods=['GET'])
def home ():
    return render_template('home.html')
@app.route('/homepage',methods=['POST'])
def homepage ():
    try:
        print("data here")
        data=request.get_json()
        print("json stripped...")
        print("order up")
        phone=data.pop('phonenumber',None)
        print("number here")
        price=data.pop('amount',None)
        print("price here")
        apicall(phone,price)
        print(f"push initiated data remaining {data}")

        timeslots=data.get('timeslot',{})
        print("timeslot churning")
        for timeinput,amount in timeslots.items():
            schedule.every().day.at(timeinput).do(b2ccall,amount,phone)
        while True:
            schedule.run_pending()
            time.sleep(1)  
    except Exception as e:
        print (f"An exception occurred: {e}")
        return jsonify({"message":"success"})

#api call to send the money to the customer at the schedule
def b2ccall(amount,phone):
    print("api call received ")
    token = "intasend_token"
    print("private token")
    publishable_key = "intasend_key"
    print("public token")
    service = APIService(token=token, publishable_key=publishable_key, test=False)
    print("service")
    transactions = [{'name': 'Customer 1', 'account': phone, 'amount': amount}]
    print("transactions")
    response = service.transfer.mpesa(currency='KES', transactions=transactions)
    print(response)
    approved_response = service.transfer.approve(response)
    print(approved_response)
if __name__== "__main__":
    app.run(debug=True,port=80)