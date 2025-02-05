# Simplified SMTP Attachment Dumper

## Overview
A single Python script that runs as an SMTP server, saves email attachments to a specified folder, and logs errors.

## Core Components
1. SMTP Server (using aiosmtpd)
2. File saving logic
3. Error logging
4. Daemon setup

## Implementation Plan

### Script Structure
```python
# smtp_dumper.py
import logging
from aiosmtpd.controller import Controller
from email import message_from_bytes
import os

# Setup logging
# Handle SMTP messages
# Save attachments
# Run server
```

### Configuration
Simple command line arguments for:
- Port number
- Save directory
- Log file location

### Systemd Service
Basic service file to run as daemon:
```ini
[Unit]
Description=SMTP Attachment Dumper

[Service]
ExecStart=/usr/bin/python3 /path/to/smtp_dumper.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Testing
- Send test email with attachment
- Verify file saves correctly
- Check error logging works

## Deployment
1. Copy script to server
2. Install Python dependencies
3. Setup systemd service
4. Start service

That's it - keeping it simple and focused on the core task.