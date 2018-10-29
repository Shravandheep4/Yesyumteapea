import smtplib, os, sys, getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

### You can specify your mail-id as the default id if you're the only one who's going to use this script

### Default way to get the password is through a prompt message, Feel free to change
#   os.environ['ENVIRONMENT_VARIABLE_NAME_GOES_HERE']   Set up an environment variable
#   sys.argv[1:]   Get the password from the argument list



### TO BE ADDED IN THE FUTURE
# 1. Timer
# 2. SMTP Server compatibility
# 3. HTML as the body   (This can be changed by simply changing the MIMEText parameter to html from plain)
# 4. Auto-generated message


#Connect to the server
retries = 0
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()

#Credential
while retries<5:
    username = input("Email id: ")
    passwd = getpass.getpass("password: ")

#Authentication
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
    server.quit()
    quit()


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
    try:
        confirm = str(input("\nConfirm Y/[N]?  "))[0].lower()
    except IndexError:
        confirm = 'N'
    if(confirm=='y'):
        break

message.attach(MIMEText(body,'plain'))


#Attachments
try:
    bool_attach = str(input("Do you want to attach files Y/[N] ? :  "))[0].lower()
except IndexError as err:
    bool_attach='N'

num_attach = 0

while(bool_attach=='y'):
    filename = str(input("File-path: "))

    if filename.strip()=="" or filename.strip()=='\n':
        bool_attach = 'N'

        if num_attach==0:
            print("No file has been attached.")
        break

    if not os.path.exists(filename):
        print("Incorrect Path, Try again\n")
        continue

    try:
        attachment = open(filename, "rb")
    except Exception as error:
        print(str(error))
        continue

    #Works on linux. For windows, split the path by using back-slash '\'
    filename = filename.split('/')[-1]

    part = MIMEBase('application','octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename="+ filename)

    message.attach(part)
    attachment.close()

    num_attach+=1
    print(f"{num_attach} attachment(s) made.")

print(f"\n{num_attach} attachment(s) in total.")

#Final mail transfer
print('Sending ...')
server.sendmail(email_sender, email_recipients, message.as_string())
print('Sent to the recipient(s)')
server.quit()
