import imaplib
import email
import os
import shutil
import re
from datetime import datetime
from imap_tools import MailBox
from email.header import decode_header

now = datetime.now()
current_time = now.strftime("%D - %H.%M.%S")

#fill with your imap credentials
IMAP_SERVER = 'your.imap.server'
EMAIL = 'your.email@your.imap.server.com'
PASSWORD = 'your_password'

id_email = 0
#First log-in to count how many emails have to import
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('define/imap/folder')  #Select the folder that where you want do donwload your emails

result, data = mail.search(None, '(HEADER Content-Type "application/pdf")')

#Effectivaly count your emails
email_count = len(data[0].split())
mail_ids = data[0].split()

#log out for now
mail.close()
mail.logout()

#while have emails it will still repeating
while id_email <= email_count +10 :

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('define/imap/folder')  #Select the folder that you have counted earlier

    result, data = mail.search(None, 'ALL')
    email_count = len(data[0].split())
    email_id = data[0].split()[0]
    result, data = mail.fetch(email_id, '(RFC822)')
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    #Define the target local folder that you want to Download your emails
    output_folder = r"define\your\destination\network\folder"
    filename = f"{msg['From']} - ({msg['Subject']}) - {current_time}" #It defines your email name as: sender - (subject) - date/time
    filename = re.sub('[^a-zA-Z0-9@.() -]',' ', filename) #Excludes characters that can't be used in windows 
    filename = f"{filename}.eml" #define the extension of the file to ".eml"
    output_path = os.path.join(output_folder, filename)
    with open(output_path, 'wb') as f:
        f.write(raw_email)

    #Last log-in to move already dowloaded files to another folder in your imap
    with MailBox('your.imap.server.com').login('your.email@your.imap.server.com', 'your_password', 'mail/source/folder') as mailbox:
        mailbox.move(mailbox.uids()[0], 'mail/destination/folder') # Move all messages from the current folder to read/files/folder
    print (id_email) #print which email is being read
    id_email += 1 #select the next email
mail.close()
mail.logout()