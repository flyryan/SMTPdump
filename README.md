# SMTP Attachment Dumper

A simple SMTP server that saves email attachments to a specified directory.

## Configuration

Edit the CONFIG section at the top of `smtp_dumper.py`:
```python
CONFIG = {
    'host': '0.0.0.0',       # Listen on all interfaces
    'port': 2525,            # Port to listen on
    'attachment_dir': '/var/smtp-dumper/attachments',  # Directory to save attachments
    'log_dir': '/var/smtp-dumper/logs'                # Directory to save logs
}
```

## Installation

1. Install Python dependencies:
```bash
sudo python3 -m pip install aiosmtpd>=1.4.2
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

# Verify Python module is available to the service user
sudo -u smtp-dumper python3 -c "from aiosmtpd.controller import Controller"

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable smtp-dumper
sudo systemctl start smtp-dumper
```

## Local Testing

1. Create local directories:
```bash
mkdir -p attachments logs
```

2. Start the server:
```bash
python3 smtp_dumper.py
```

3. In another terminal, run the test script:
```bash
python3 test_send.py
```

The test script will send an email with test.txt as an attachment. You should see a success message and the attachment will be saved in the attachments directory with a timestamp prefix.

## Monitoring

- Check service status: `sudo systemctl status smtp-dumper`
- View logs: `sudo tail -f /var/smtp-dumper/logs/smtp_dumper.log`
- Check saved files: `ls -l /var/smtp-dumper/attachments/`

## Troubleshooting

1. If service fails to start:
   - Check logs: `journalctl -u smtp-dumper`
   - Verify permissions on directories
   - Ensure port 2525 is available and not blocked by firewall
   - Verify Python dependencies are installed

2. If attachments aren't saving:
   - Check directory permissions
   - Verify enough disk space
   - Review logs for specific errors
   - Ensure email contains proper attachments

3. Common Issues:
   - Port already in use: Check if another service is using port 2525
   - Permission denied: Check directory and file ownership