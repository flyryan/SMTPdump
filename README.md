# SMTP Attachment Dumper

A simple SMTP server that saves email attachments to a specified directory.

## Configuration

Edit the CONFIG section at the top of `smtp_dumper.py`:
```python
CONFIG = {
    'host': 'localhost',      # Host to listen on
    'port': 8025,            # Port to listen on
    'attachment_dir': '/var/smtp-dumper/attachments',  # Directory to save attachments
    'log_dir': '/var/smtp-dumper/logs'                # Directory to save logs
}
```

## Installation

1. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

2. Setup service (on RedHat):
```bash
# Create service user
sudo useradd -r -s /sbin/nologin smtp-dumper

# Create directories
sudo mkdir -p /opt/smtp-dumper
sudo mkdir -p /var/smtp-dumper/attachments
sudo mkdir -p /var/smtp-dumper/logs

# Copy files
sudo cp smtp_dumper.py /opt/smtp-dumper/
sudo cp smtp-dumper.service /etc/systemd/system/

# Set permissions
sudo chown -R smtp-dumper:smtp-dumper /opt/smtp-dumper
sudo chown -R smtp-dumper:smtp-dumper /var/smtp-dumper

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable smtp-dumper
sudo systemctl start smtp-dumper
```

## Usage

The server will:
- Listen for incoming SMTP connections
- Save any email attachments to the specified directory
- Add timestamps to filenames to prevent conflicts
- Log all activity and errors

### Manual Testing

You can test locally using Python's built-in SMTP client:

```python
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
with open('test.pdf', 'rb') as f:
    attachment = MIMEApplication(f.read(), _subtype='pdf')
    attachment.add_header('Content-Disposition', 'attachment', filename='test.pdf')
    msg.attach(attachment)

# Send email
with smtplib.SMTP('localhost', 8025) as smtp:
    smtp.send_message(msg)
```

## Monitoring

- Check service status: `sudo systemctl status smtp-dumper`
- View logs: `sudo tail -f /var/smtp-dumper/logs/smtp_dumper.log`
- Check saved files: `ls -l /var/smtp-dumper/attachments/`

## Troubleshooting

1. If service fails to start:
   - Check logs: `journalctl -u smtp-dumper`
   - Verify permissions
   - Ensure port is available

2. If attachments aren't saving:
   - Check directory permissions
   - Verify enough disk space
   - Review logs for errors