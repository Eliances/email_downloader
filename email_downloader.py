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

#credenciais de login
IMAP_SERVER = 'your.imap.server'
EMAIL = 'your.email@your.imap.server.com'
PASSWORD = 'your_pa$$word'

#define a variável de id do E-mail
id_email = 0

#Efetua login para captar numero de E-mails
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('define/imap/folder')  # Selecione a caixa de entrada

# Buscando os IDs dos e-mails na pasta
result, data = mail.search(None, '(HEADER Content-Type "application/pdf")')

# Count the emails
email_count = len(data[0].split())

mail_ids = data[0].split()


mail.close()
mail.logout()

#enquanto houver E-mails ele vai efetuar o processo
while id_email <= email_count +10 :

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('destination/folder')  # Selecione a caixa de entrada


    # Buscando os IDs dos e-mails na pasta
    result, data = mail.search(None, 'ALL')
    # Count the emails
    email_count = len(data[0].split())

    email_id = data[0].split()[0]
   
    result, data = mail.fetch(email_id, '(RFC822)')
    raw_email = data[0][1]

    msg = email.message_from_bytes(raw_email)

    #diretório destino Download
    output_folder = r"define\your\destination\network\folder"
    filename = f"{msg['From']} - ({msg['Subject']}) - {current_time}"  # Nome do arquivo
    filename = re.sub('[^a-zA-Z0-9@.() -]',' ', filename)
    filename = f"{filename}.eml"
    output_path = os.path.join(output_folder, filename)

    with open(output_path, 'wb') as f:
        f.write(raw_email)

    #move arquivos lidos para outra pasta

    with MailBox('your.imap.server.com').login('your.email@your.imap.server.com', 'your_pa$$word', 'mail/source/folder') as mailbox:
    # Move all messages from the current folder to INBOX/folder2
        mailbox.move(mailbox.uids()[0], 'mail/destination/solder') 

    print (id_email)
    id_email += 1
mail.close()
mail.logout()