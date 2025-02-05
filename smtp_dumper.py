#!/usr/bin/env python3

# Configuration
CONFIG = {
    'host': 'localhost',      # Host to listen on
    'port': 8025,            # Port to listen on
    'attachment_dir': './attachments',  # Directory to save attachments (local testing)
    'log_dir': './logs'                # Directory to save logs (local testing)
}

import asyncio
import logging
import os
import sys
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP
from email import message_from_bytes
from datetime import datetime

# Configure logging before anything else
os.makedirs(CONFIG['log_dir'], exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(CONFIG['log_dir'], 'smtp_dumper.log')),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('smtp_dumper')

# Suppress aiosmtpd debug logs
logging.getLogger('mail.log').setLevel(logging.WARNING)
logging.getLogger('aiosmtpd').setLevel(logging.WARNING)

class AttachmentHandler:
    def __init__(self):
        self.save_dir = CONFIG['attachment_dir']
        os.makedirs(self.save_dir, exist_ok=True)
        
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        try:
            message = message_from_bytes(envelope.content)
            
            # Process each attachment
            attachments_found = False
            for part in message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                    
                filename = part.get_filename()
                if filename:
                    attachments_found = True
                    # Generate unique filename with timestamp
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    unique_filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(self.save_dir, unique_filename)
                    
                    # Save attachment
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    
                    logger.info(f"Saved attachment: {unique_filename}")
            
            if not attachments_found:
                logger.info("Email received but no attachments found")
                
            return '250 Message accepted for delivery'
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return '500 Error processing message'

async def main():
    # Create handler and controller
    handler = AttachmentHandler()
    controller = Controller(handler, hostname=CONFIG['host'], port=CONFIG['port'])
    
    try:
        # Start the SMTP server
        controller.start()
        logger.info(f"Started SMTP server on {CONFIG['host']}:{CONFIG['port']}")
        logger.info(f"Saving attachments to {os.path.abspath(CONFIG['attachment_dir'])}")
        logger.info(f"Logs available at {os.path.abspath(CONFIG['log_dir'])}")
        
        # Keep the server running
        while True:
            await asyncio.sleep(3600)  # Sleep for an hour, then check again
            
    except KeyboardInterrupt:
        controller.stop()
        logger.info("Server stopped")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        controller.stop()
        sys.exit(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
        sys.exit(0)