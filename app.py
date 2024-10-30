from flask import Flask, render_template, request, redirect, url_for
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

RECAPTCHA_SECRET_KEY= '6LeCmXAqAAAAAIX0m9NMiy6TsnGfQkclrzqWDDcZ'


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT= 587
USERNAME= 'sofja.mf@gmail.com'
PASSWORD = 'kisi eljh ywkv uahc'

app = Flask(__name__)

@app.route("/")
def contact():
    return render_template("index.html")

@app.route("/send_email", methods=['POST'])
def send_email():
    if request.method =='POST':
        email= request.form['email']
        message = request.form['message']

        recaptcha_response = request.form['g-recaptcha-response']

        recaptcha_url= 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_data = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        recaptcha_request = requests.post(recaptcha_url, data=recaptcha_data)
        recaptcha_result= recaptcha_request.json()

        print(recaptcha_result)
        #print(recaptcha_result['score'])

        if recaptcha_result['success'] == True and recaptcha_result['score'] >= 0.5:

            msg = MIMEMultipart()
            msg['From'] = email
            msg['To']= USERNAME
            
            body = f"Email:{email}\n\nMessage:\n{message}"
            msg.attach(MIMEText(body, 'plain'))

            try:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(USERNAME, PASSWORD)
                text =msg.as_string()
                server.sendmail(email, USERNAME, text)
                server.quit()
            except Exception as e:
                print (f"Error: {e}")

            return redirect(url_for('contact'))
        else:
            print('ROBOT')
            return redirect(url_for('contact'))




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)