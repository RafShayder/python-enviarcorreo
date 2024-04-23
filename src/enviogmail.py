# Author: Raf Shayder Leon Gutierrez, Telco Asociado : https://www.linkedin.com/in/raf-shayder-leon
 #2024-04-12 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
import smtplib
msg = MIMEMultipart()
class Email:
    __host='smtp.gmail.com'
    __port=465
    __automensaje='* No responda este correo, fue autogenerado el Envio, @Raf Shayder *' 
    __firma='Bot Automatico \n Telco'
    def __init__(self,from_email,from_pass,to_email,body='Saludos Cordiales, Se te envia este correo de forma automática',subject='Envio automatico de Correo',cc=None,attachment=None):
        self.from_email=from_email
        self.from_pass=from_pass
        self.to_email=to_email
        self.subject=subject
        self.cc=cc
        self.body=body
        self.attachment=attachment

    @property
    def firma(self):
        return self.__firma
    @firma.setter
    def firma(self,firma):
        self.__firma=firma
    @property
    def automensaje(self):
        return self.__automensaje
    @automensaje.setter
    def automensaje(self,automensaje):
        self.__automensaje=automensaje    
    @property
    def host(self):
        return self.__host
    @host.setter
    def host(self,host):
        self.__host=host
    @property
    def port(self):
        return self.__port
    @port.setter
    def port(self,port):
        self.__port=port

    def verificarcorreo(self,mail):
        #Verificamos el correo
        mensaje='correo invalido falta: '
        error_mail=False
        for char in ['@','.']:
            if(char not in mail):
                mensaje+= char+'|'
                error_mail=True
        if(error_mail):
            print(mensaje,mail)
        #veliricar
        return error_mail
    def adjuntararchivo(self,nombrearchivo):
        self.__attachfile(nombrearchivo)
    def __attachfile(self,attachment):
        try:
            with open(attachment, "rb") as archivo:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(archivo.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={attachment}')
                # Attach the file
                msg.attach(part)
        except Exception as e:
            print(f"Could not attach {attachment} due to {e}")
    def adjuntardata(self, data, filename):
        try:
            if('DataFrame' in str(type(data))):
                buffer = BytesIO()
                if filename.endswith('.xlsx'):
                    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    data.to_excel(buffer, index=False)
                    data = buffer.getvalue()

                elif filename.endswith('.csv'):
                    content_type = 'text/csv'
                    data.to_csv(buffer, index=False)
                    data = buffer.getvalue()
                elif filename.endswith('.txt'):
                    
                    content_type = 'text/plain'
                    data.to_csv(buffer, index=False, sep='\t')
                    data = buffer.getvalue()
                else:
                    content_type = 'application/octet-stream'
                    data = None
            else:
                content_type = 'application/octet-stream'
            # Crear objeto MIMEBase para el adjunto
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(data)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            part.add_header('Content-Type', content_type)
            msg.attach(part)
            
        except Exception as e:
            print(f"Could not attach {filename} due to {e}")
    
    def enviarMail(self):
        if not  (self.verificarcorreo(self.from_email) and self.verificarcorreo(self.to_email)):
            msg['From'] = self.from_email
            msg['To'] = self.to_email 
            msg['Subject'] = self.subject
            msg.attach(MIMEText(self.body,'plain'))
            #attachment file
            if(self.attachment):
                self.__attachfile(self.attachment)
            # Send the email and login
            with smtplib.SMTP_SSL(self.host, self.port) as smtp:
                try:
                    smtp.login(self.from_email, self.from_pass)  
                    smtp.send_message(msg)
                    print("mensaje enviado")
                except Exception as e:
                    print("Login wrong",e)
        else:
            print("datos incorrectos")





