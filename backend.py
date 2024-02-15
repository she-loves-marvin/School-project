from flask import Flask,request
import requests
import psycopg2
import json
import os

connection_string = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(connection_string)
cursor= conn.cursor()

app=Flask(__name__)
def apicall(number):
  try: 
      url="https://tinypesa.com/api/v1/express/initialize"
      details={
          "amount": "1",
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
@app.route(['/'],methods=['GET','POST'])
def login():
    try:
        data=request.get_json()
        email=data.get('email')
        password=data.get('password')
        query="SELECT * FROM Project WHERE email = %s AND password = %s LIMIT 1"
        cursor.execute(query,(email,password))
        feedback =cursor.fetchone()
        if feedback is not None:
            pass
            #return statement
        else:
            pass
            #return statement
    except Exception as e:
        print(f"An error occurred: {e}")

app.route(['/signup'],methods=-['GET','POST'])
def signup ():
    try:
        data=request.get_json()
        email=data.get('email')
        password=data.get('password')
        query="INSERT INTO Project (email,password) VALUES (%s, %s)"
        cursor.execute(query,(email,password))
        conn.commit()
        cursor.close()
        conn.close()
        return 
    except  Exception as e:
        print(f"An exception occurred: {e}")
@app.route(['/homepage'],methods=['GET','POST'])
def homepage ():
    try:
        data=request.get_json
        phone=data.get('phone')
        apicall(phone)
        #rest of logic
    except Exception as e:
        print (f"An exception occurred: {e}")
def b2ccall():
    tobecontinued=5