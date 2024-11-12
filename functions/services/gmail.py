import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# import html2text
import fitz  # PyMuPDF
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import re

company_email = "alfa.vlueio@gmail.com"
# app_password = "ckkcwodclbvccvgf"  # Usa la contraseña de aplicación aquí


def send_email(destination_email, app_password):
    # Configuración del servidor SMTP de Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Información de inicio de sesión y destinatario
   
    receiver_email = destination_email
    
    # Crear el mensaje
    msg = MIMEMultipart()
    msg["From"] = company_email
    msg["To"] = receiver_email
    msg["Subject"] = "[Test Santino Ops] Test "
    
    # Cuerpo del correo
    body = "Este es el contenido del correo"
    msg.attach(MIMEText(body, "plain"))

    try:
        # Conexión al servidor SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Usar TLS para seguridad
            server.login(company_email, app_password)  # Iniciar sesión en el servidor
            server.sendmail(company_email, receiver_email, msg.as_string())  # Enviar el correo
        print("Correo enviado con éxito.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Llamada a la función
# send_email("rvin.rdgz@gmail.com")



def read_emails(app_password):
    # Configuración del servidor IMAP de Gmail
    imap_server = "imap.gmail.com"
    mails = []
    attachments = []

    try:
        # Conexión al servidor IMAP
        with imaplib.IMAP4_SSL(imap_server) as mail:
            mail.login(company_email, app_password)
            mail.select("Inbox")  # Seleccionar la bandeja de entrada
            
            # Buscar todos los correos electrónicos (cambiar "ALL" por "UNSEEN" para solo no leídos)
            status, messages = mail.search(None, "ALL")

            # Lista de correos
            mail_ids = messages[0].split()

            for i in mail_ids:

                try:
                    status, msg_data = mail.fetch( i , "(RFC822)")


                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            # Decodificar asunto
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else "utf-8")
                            mail_content = []
                            # Decodificar remitente
                            from_ = msg.get("From")
                            date_= msg.get("Date")

                            # print("Asunto:", subject)
                            # print("De:", from_)
                            
                            # Leer contenido del correo
                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    content_disposition = str(part.get("Content-Disposition"))
                                    # print("$$$$$",content_type,content_disposition)
                                        
                                    
                                    if content_type == "text/html" and "attachment" not in content_disposition:
                                        body = part.get_payload(decode=True).decode()
                                        soup = BeautifulSoup(body, 'html.parser')
                                        plain_text = soup.get_text(separator="\n", strip= True)
                                        # print(plain_text)
                                        split_text = re.split(r"(de:|De:|From:|from:)", plain_text) 
                                        second_filter_mails = [split_text[0]]
                                        for i in range(1, len(split_text) - 1, 2):
                                            second_filter_mails.append(split_text[i] + split_text[i + 1])

                                        mail_content.extend(second_filter_mails)
                                        # print( plain_text , '\n' + "#"*50 + '\n')
                                    
                                    if content_type == "application/pdf" :

                                        filename = part.get_filename()
                                        if filename:
                                            # Descargar el PDF
                                            pdf_data = part.get_payload(decode=True)
                                            with open(filename, "wb") as pdf_file:
                                                pdf_file.write(pdf_data)

                                            # Convertir el PDF a texto
                                            text = pdf_to_text(filename)
                                            attachments.append( {"filename" : filename, "text" : text})



                            else:
                                body = msg.get_payload(decode=True).decode()
                                soup = BeautifulSoup(body, 'html.parser')
                                plain_text = soup.get_text(separator="\n", strip= True)
                                mail_content.append(plain_text)




                            

                            mail_info = {
                                "subject" : subject,
                                "from" : from_,
                                "date" : date_,
                                "latest_mail" : mail_content[0],
                                "mails" : mail_content[1:],
                                "attachments" : attachments,
                            }
                            
                            # print(mail.subject)
                            mails.append(mail_info)

                except Exception as e:
                    print("Error " ,e)

            return mails
                        
    except Exception as e:
        print(f"Error al leer correos: {e}")

def pdf_to_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            text += page.get_text()
    return text
# read_emails()