import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import globalConstants



def sendEmail(to, subject, body, fileUrl):
    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = globalConstants.EMAIL
    msg['To'] = to
    msg.attach(MIMEText(body, 'html'))
    if fileUrl is not None:
        file = open(fileUrl, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename=ProductDetails.csv')
        msg.attach(part)
    print("sending mail to "+to)

    with smtplib.SMTP(globalConstants.MAIL_SERVER, globalConstants.PORT) as server:
        server.starttls()
        server.login(globalConstants.EMAIL, globalConstants.PASSWORD)
        server.sendmail(globalConstants.EMAIL, to, msg.as_string())