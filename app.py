from flask import Flask, request
from textblob import TextBlob
import sendgrid

app = Flask(__name__)
sg = sendgrid.SendGridClient('jprakash', 'prakash')

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/incoming',methods=['POST'])
def besmart():

   email = request.form['from']
   subject = request.form['subject']
   incoming_body = request.form['text']
   send_from =  request.form['to']

   #Get the sentiment of the body
   blob = TextBlob(incoming_body)
   sentiment = blob.sentiment

   #Based on Sentiment send back a different email
   #polarity > 0 is positive and less is negative

   if sentiment.polarity > 0:
        body = "Thats good! We appreciate the feedback. Expect another response from a support rep soon"
   elif sentiment.polarity < 0:
        body = "We're sorry to hear that!. We just forwarded your request to the appropriate person in support, expect a response shortly"
   else:
        body = "We are forwarding your question to the appropriate person in support, Will get back to you shortly"


   new_sub = "Re: "+subject


   #Send back that return email

   message = sendgrid.Mail()
   message.add_to(email)
   message.set_subject(new_sub)
   message.set_html(body)
   message.set_text(body)
   message.set_from(send_from)
   status, msg = sg.send(message)

   return "OK"

if __name__ == '__main__':
   app.run()