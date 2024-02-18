import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
class exbo(object):
  # constructor
  def __init__(self):
    pass


def abhinav():
    print("Abhinav Jain")

def adrija():
    print("Adrija Sengupta")

def akarsh():
    print("Akarsh Shrivastava")

def armaan():
    print("Armaan Mittal")

def dev():
    print("Dev Goyal")

def dinesh():
    print("Dinesh Agrawal")

def gopal():
    print("Gopal Agarwal")

def gurman():
    print("Gurman Kaur")

def hushraj():
    print("Hushraj Singh")

def jahanvi():
    print("Jahanvi Srivastava")

def jasdeep():
    print("Jasdeep Singh")

def kanishk():
    print("Kanishk Jagya")

def pancham():
    print("Pancham Agarwal")

def pariansh():
    print("Pariansh Mahajan")

def reyan():
    print("Reyan Singh")

def saaransh():
    print("Saaransh Gupta")

def sharath():
    print("Sharath Chandra Chinnarigari")

def shaurya():
    print("Shaurya Verma")

def sparsh():
    print("Sparsh Rastogi")

def swapnil():
    print("Swapnil Chhibber")

def test():
    print("This is a test")
    
    

def sendEmail(email,password,recp_email,Subject, messageBody):
    try:
        sender_email = email
        sender_password = password
        recipient_email =recp_email
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = Subject
        body = messageBody
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:   
            server.starttls()
            server.login(sender_email, sender_password)     
            server.send_message(message)

        print(f"Email sent successfully to {recipient_email}")
    except:
        print(f"Error occurred. Email not sent for {recipient_email}")

if __name__ == '__main__':
  pass