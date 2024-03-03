from flask import Flask,request,jsonify,render_template
from multiprocessing import Process
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
    print("Hash generator")
    salted_password = password + salt
    print("concatenation okay")
    hashedpassword=hashlib.sha256(salted_password.encode()).hexdigest()
    print("hash complete")
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
        print("home")
        price="20"
        print(f"price: {price}")
        phone="0112869586"
        print(f"phone: {phone}")
        b2ccall(price,phone)
        print("Succesful b2c call")
        response= jsonify({"Data":"call success"})
        return response
        """
        print("request received")
        data=request.get_json()
        print("data stripped")
        email=data.get('Email')
        print(f"email check {email}")
        password=data.get('Password')
        print(f"password check {password}")
        query="SELECT * FROM Project WHERE email = %s LIMIT 1"
        cursor.execute(query,(email,))
        print("query initiated")
        feedback =cursor.fetchone()
        print(f"feedback check {feedback}")
        if feedback is not None:
            hashpass=feedback[1]
            hashstr=bytes(hashpass).decode('utf-8')
            print(f"hashpass check {hashstr}")
            salt=feedback[2]
            print(f"salt here {salt}")
            salt_str = bytes(salt).decode('utf-8')
            print(f"decoded to string {salt_str}")
            passkey=hash_password(password,salt_str)
            print(f"pass regenartion success {passkey}")
            if hashstr==passkey:
               print("log in succesfull")
               return render_template('home.html')
            else:
                print("false password")
                response= jsonify({"Data":"The password you entered is not correct.Please try again!!!"})
                return response
        else:
            print("account does not exist")
            response = jsonify({"Data":"The account under this email does not exist.PLease got to the sign up page and create a new account"})
            return response
        """
    except Exception as e:
        print(f"An error occurred: {e}")
        
def hello():
    print("hello")
#signup page for new users
@app.route('/signup',methods=['GET'])
def rendersignuppage():
    try:
        print("request received rendering sign up page")
        return render_template('signup.html')
    except Exception as e:
        print(f"A n error occured : {e}")
@app.route('/signup',methods=['POST'])
def signup ():
    try:
        print("data received")
        data=request.get_json()
        print("data stripped")
        email=data.get('Email')
        print ("email check")
        password=data.get('Password')
        print(f"password check {password}")
        salt=generate_salt()
        print(f"salt done {salt}")
        passkey=hash_password(password,salt)
        print("hashed password ready")
        confirmation="SELECT * FROM project WHERE email = %s LIMIT 1"
        cursor.execute(confirmation,(email,))
        print("query exceuted")
        result=cursor.fetchone()
        print("result here")
        if result is None:
            print("result is none")
            query="INSERT INTO Project (email,passkey,salt) VALUES (%s, %s, %s )"
            cursor.execute(query,(email,passkey,salt))
            conn.commit()
            print("new email inserted into db success")
            cursor.close()
            conn.close()
            return render_template('login.html')
        else:
            print("email already exists")
            response=jsonify({"Data":"The account corresponding to the email address you entered already exists"})
            return response
    except  Exception as e:
        print(f"An exception occurred: {e}")


#homepage logic behind budgeting
def schedule_tasks(data:dict, phone):
    print(f"data:{data}")
    for timeinput, amount in data.items():
        schedule.every().day.at(timeinput).do(b2ccall, amount, phone)
    while True:
        schedule.run_pending()
        time.sleep(1)
@app.route('/homepage',methods=['GET'])
def home ():
    return render_template('home.html')
@app.route('/homepage',methods=['POST'])
def homepage ():
    try:

        """
        print("data here")
        data=request.get_json()
        print("json stripped...")
        print("order up")
        phone=data.pop('phonenumber',None)
        print(f"number here {phone}")
        price=data.pop('amount',None)
        print(f"price here{price}")
        apicall(phone,price)
        print(f"push initiated data remaining {data}")
        threadschedule=Process(target=schedule_tasks , args=(data,phone),daemon=False)
        threadschedule.start()
        """
        return jsonify({"Data":"Your schedule has been set up succesfully"})
    except Exception as e:
        print (f"An exception occurred: {e}")
        return jsonify({"Data":"An error occured"})

#api call to send the money to the customer at the schedule
def b2ccall(amount,phone):
    try:
        print("api call received ")
        token = os.environ.get("intasend_token")
        print(f"private token {token}")
        publishable_key = os.environ.get("intasend_key")
        print(f"public token {publishable_key}")
        service = APIService(token=token, publishable_key=publishable_key, test=False)
        print("service")
        transactions = [{'name': 'Customer 1', 'account': phone, 'amount': amount}]
        print("transactions")
        response = service.transfer.mpesa(currency='KES', transactions=transactions)
        print(response)
        approved_response = service.transfer.approve(response)
        print(approved_response)
        return ("okay")
    except Exception as e:
        print(f"An error occured: {e}")
if __name__== "__main__":
    app.run(debug=True,port=80)