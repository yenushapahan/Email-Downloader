import imaplib
import email
import JSPYLib

mydbfile = JSPYLib.DATABASE()

imap_server = "imap.gmail.com"
email_address = input("Email: ")
password = input("Google Server Password: ")

try:
    imap = imaplib.IMAP4_SSL(imap_server)

    imap.login(email_address,password)
except Exception as e:
    print("There is an Error with login {}".format(e))

#Select the folder where the data need to be collect
try:
    email_folder= input("Email Folder Name: ")
    imap.select(email_folder)
except Exception as e:
    print("There is an Error with folder Selection. ",e)

email_filter_words = input("Enter the Filter for email: ")

if not email_filter_words:
    email_filter_words = "ALL"

try:
    _,msgnums = imap.search(None,email_filter_words)

except:
    print("This Filter isn't valid. ",e)

email_range = int(input(f"Select the Range {len(msgnums[0].split())}: "))

if email_range > len(msgnums[0].split()):
    email_range = len(msgnums[0].split())

for msgnum in msgnums[0].split()[:email_range]:
    _,data = imap.fetch(msgnum,"RFC822")

    message = email.message_from_bytes(data[0][1])

    body = ""
    for part in message.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode(errors="ignore")
            break  # stop at first plain-text part

    # Then create your dataset dictionary
    dataset = {
        "Msg Number": str(msgnum)[2:-1],
        "From": str(message.get('From')),
        "Subject": str(message.get('Subject')),
        "Content": f"""str(body)"""
    }

    mydbfile.insertData2("emaildata",dataset)

imap.logout()


