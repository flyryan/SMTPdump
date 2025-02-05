#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

# Create test email with attachment
msg = MIMEMultipart()
msg['Subject'] = 'Test Email'
msg['From'] = 'sender@example.com'
msg['To'] = 'recipient@example.com'

# Add text body
msg.attach(MIMEText('Test email body'))

# Add file attachment
with open('test.txt', 'rb') as f:
    attachment = MIMEApplication(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename='test.txt')
    msg.attach(attachment)

# Send email
with smtplib.SMTP('localhost', 8025) as smtp:
    smtp.send_message(msg)
    print("Test email sent successfully!")