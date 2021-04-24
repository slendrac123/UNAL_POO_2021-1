import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mensajeObj = MIMEMultipart()
mensaje = 'Hola\nEste es un mensaje de prueba para mi app'


mensajeObj['From'] = 'pruebas.vacunacion@gmail.com'
mensajeObj['To'] = 'jugarciale@unal.edu.co'
mensajeObj['Subject'] = 'Email de prueba'
password = 'TEST_123*'

mensajeObj.attach(MIMEText(mensaje, 'plain'))

try:
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(mensajeObj['From'], password)

    server.sendmail(mensajeObj['From'], mensajeObj['To'], mensajeObj.as_string())
    print('correo enviado')
    server.quit()
except:
    print('error')