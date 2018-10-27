import smtplib, os, sys, getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#Timer
#Multiple Attachments


#os.environ['PASSWD']
#sys.argv[1:]

#Credentials
username = input("Email id: ")
passwd = getpass.getpass("password: ")

#Sender and Receiver information
email_sender = username
email_recipients = ["shravandheep4@gmail.com"]
Subject = "Testing script"

# filling the text part
message = MIMEMultipart()
message['From'] = email_sender
message['To'] = ", ".join(email_recipients)
message['Subject'] = Subject

while True:
    body = str(input("Body : "))
    if(str(input("\nIs this the message you want to send Y/[N]?  "))[0].lower()=='y'):
        break

message.attach(MIMEText(body,'plain'))


#Attachments
bool_attach = str(input("Do you want to make attachments? Y/[N] :  "))[0].lower()
num_attach = 0

while(bool_attach=='y'):
    filename = str(input("File-path: "))

    if not os.path.exists(filename):
        print("Incorrect Path, Try again")
        continue

    attachment = open(filename, "rb")

    part = MIMEBase('application','octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename="+ filename)

    message.attach(part)
    attachment.close()

    num_attach+=1
    print(f"{num_attach} attachment(s) made.")
    bool_attach = str(input("Do you want to make one more attachment Y/[N]?  :  "))[0].lower()

#Final Message
text = message.as_string()

#Connecting to the server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
try:
    server.login(username, passwd)
except Exception as err:
    print(str(err).split("'")[1])
else:
    print('Sending ...')
    server.sendmail(email_sender, email_recipients, text)
    print('Sent to the recipient(s)')
finally:
    server.quit()
