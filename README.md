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

## Testing

### Local Development Testing

1. Update CONFIG in smtp_dumper.py to use local directories:
```python
CONFIG = {
    'host': 'localhost',
    'port': 8025,
    'attachment_dir': './attachments',
    'log_dir': './logs'
}
```

2. Start the server:
```bash
python3 smtp_dumper.py
```

You should see:
```
Started SMTP server on localhost:8025
Saving attachments to /path/to/attachments
Logs available at /path/to/logs
```

3. In another terminal, create a test file:
```bash
echo "Test content" > test.txt
```

4. Send a test email with the test.txt attachment:
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
with open('test.txt', 'rb') as f:
    attachment = MIMEApplication(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename='test.txt')
    msg.attach(attachment)

# Send email
with smtplib.SMTP('localhost', 8025) as smtp:
    smtp.send_message(msg)
    print("Test email sent successfully!")
```

5. Verify the attachment was saved:
```bash
ls -l attachments/
```

You should see your test.txt file saved with a timestamp prefix, e.g.:
`20250205_151118_test.txt`

### Production Testing

1. After deploying to RedHat server, verify the service is running:
```bash
sudo systemctl status smtp-dumper
```

2. Check logs for successful startup:
```bash
sudo tail -f /var/smtp-dumper/logs/smtp_dumper.log
```

3. Send a test email to the server's IP address on port 25 (or configured port)

4. Verify attachment was saved:
```bash
ls -l /var/smtp-dumper/attachments/
```

5. Monitor logs for any errors:
```bash
sudo tail -f /var/smtp-dumper/logs/smtp_dumper.log
```

## Monitoring

- Check service status: `sudo systemctl status smtp-dumper`
- View logs: `sudo tail -f /var/smtp-dumper/logs/smtp_dumper.log`
- Check saved files: `ls -l /var/smtp-dumper/attachments/`

## Troubleshooting

1. If service fails to start:
   - Check logs: `journalctl -u smtp-dumper`
   - Verify permissions on directories
   - Ensure port is available
   - Check Python dependencies are installed

2. If attachments aren't saving:
   - Check directory permissions
   - Verify enough disk space
   - Review logs for specific errors
   - Ensure email contains proper attachments

3. Common Issues:
   - Port already in use: Change port in CONFIG or stop conflicting service
   - Permission denied: Check directory and file ownership
   - Missing attachments: Verify email is properly formatted with attachments
   - Connection refused: Check firewall settings and port availability