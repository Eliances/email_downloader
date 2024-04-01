

## You can use this scipt to move to a specific folder messages that matches with your nessecities, like a word or a specific file in the email message ##


import imaplib
import email
from email.header import decode_header
import re

# Your email and password
email_user = "your.email@your.imap.server.com"
email_pass = "your_password"

# Connect to the email server
mail = imaplib.IMAP4_SSL("your.imap.server")
mail.login(email_user, email_pass)

# Select the mailbox
mail.select("source/folder")

# Search for emails with PDF attachments
result, data = mail.search(None, 'ALL')
mail_ids = data[0].split()
word = ".pdf" #Defines de variable to ".pdf", you can change the word to a word that matches with what you are looking for
for num in mail_ids:
    result, data = mail.fetch(num, "(RFC822)")
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)
    # Check if the email has a PDF attachment
    for part in email_message.walk():
        email_message = re.sub('[^a-zA-Z0-9@.() -]','', str(email_message)) #use this command to define the raw email as a extended string
        if word in email_message: #search the variable "word" in the raw email 
            # Move the email to the desired folder
            mail.copy(num, "destination/folder") # Use the name of the folder you want to move the emails to
            mail.store(num, "+FLAGS", "\\Deleted")
            break