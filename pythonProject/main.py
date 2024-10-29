import cgi
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

form = cgi.FieldStorage()
user_email = form.getvalue("email")
user_message = form.getvalue("message")

email_sender = 'sofja.mf@gmail.com'
email_password = 'kisi eljh ywkv uahc'
email_receiver = 'sofja.mf@gmail.com'


subject = 'something'
body = """
hope that it will work
"""

message = MIMEMultipart()
message["From"] = email_sender
message["To"] = email_receiver
message["Subject"] = f"New message from {user_email}"

body = f"Message from {user_email}:\n\n{user_message}"
message.attach(MIMEText(body, "plain"))


try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, message.as_string())
    print("Content-Type: text/html\n")
    print("<html><body><h1>Email sent successfully!</h1></body></html>")
except Exception as e:
    print("Content-Type: text/html\n")
    print(f"<html><body><h1>Failed to send email. Error: {e}</h1></body></html>")