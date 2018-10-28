import smtplib, os, sys, getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

### Default way to get the password is through a prompt message, Feel free to change
#os.environ['PASSWD']   Set up an environment variable
#sys.argv[1:]   Get the password from the argument list



### TO BE ADDED IN THE FUTURE
# 1. Timer
# 2. Multiple SMTP Servers
# 3. HTML as the body   (This can be changed by simply changing the MIMEText parameter to html from plain)


#Connecting to the server
retries = 0
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()

#Credentials
while retries<5:
    username = input("Email id: ")
    passwd = getpass.getpass("password: ")

    try:
        server.login(username, passwd)
    except Exception as err:
        print(str(err).split("'")[1])
        retries+=1
        continue
    else:
        print("Logged in Successfully\n")
        break
else:
    print("Too many retries. Make sure you are entering the right set of credentials ")

#Sender and Receiver information
email_sender = username
email_recipients = []
Subject = str(input("Subject : "))

print("Enter the recipient(s) mail address: ")

while True:
    recipient = str(input())

    if(recipient.strip()=="" or recipient.strip()=='\n'):
        if len(email_recipients)==0:
            print("You have to add at least one recipient!")
            continue
        break

    if "," in recipient:
        recipient = recipient.split(",")
        recipient = [removeSpaces.strip() for removeSpaces in recipient]
        email_recipients.append(recipient)
    else:
        email_recipients.append(recipient.strip())

    print(str(len(email_recipients)) + " recipient(s) added.")

print(str(len(email_recipients)) + " recipient(s) in total")


# Message transfer detail
message = MIMEMultipart()
message['From'] = email_sender
message['To'] = ", ".join(email_recipients)
message['Subject'] = Subject

while True:
    body = str(input("\nBody : "))
    if(str(input("\nConfirm Y/[N]?  "))[0].lower()=='y'):
        break

message.attach(MIMEText(body,'plain'))


#Attachments
bool_attach = str(input("Do you want to attach a file Y/[N] ? :  "))[0].lower()
num_attach = 0

while(bool_attach=='y'):
    filename = str(input("File-path: "))

    if not os.path.exists(filename):
        print("Incorrect Path, Try again")
        continue

    attachment = open(filename, "rb")
    filename = filename.split('/')[-1]

    part = MIMEBase('application','octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename="+ filename)

    message.attach(part)
    attachment.close()

    num_attach+=1
    print(f"{num_attach} attachment(s) made.")
    bool_attach = str(input("Do you want to attach one more file Y/[N]?  :  "))[0].lower()

#Final Message
text = message.as_string()

print('Sending ...')
server.sendmail(email_sender, email_recipients, text)
print('Sent to the recipient(s)')
server.quit()
