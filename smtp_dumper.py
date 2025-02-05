#!/usr/bin/env python3

# Configuration
CONFIG = {
    'host': 'localhost',      # Host to listen on
    'port': 8025,            # Port to listen on
    'attachment_dir': '/var/smtp-dumper/attachments',  # Directory to save attachments
    'log_dir': '/var/smtp-dumper/logs'                # Directory to save logs
}

import asyncio
import logging
import os
import sys
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP
from email import message_from_bytes
from datetime import datetime

class AttachmentHandler:
    def __init__(self):
        self.save_dir = CONFIG['attachment_dir']
        
        # Ensure directories exist
        os.makedirs(self.save_dir, exist_ok=True)
        os.makedirs(CONFIG['log_dir'], exist_ok=True)
        
        # Setup logging
        log_file = os.path.join(CONFIG['log_dir'], 'smtp_dumper.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('smtp_dumper')
        
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        try:
            message = message_from_bytes(envelope.content)
            
            # Process each attachment
            for part in message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                    
                filename = part.get_filename()
                if filename:
                    # Generate unique filename with timestamp
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    unique_filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(self.save_dir, unique_filename)
                    
                    # Save attachment
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    
                    self.logger.info(f"Saved attachment: {unique_filename}")
            
            return '250 Message accepted for delivery'
            
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            return '500 Error processing message'

def main():
    # Create handler and controller
    handler = AttachmentHandler()
    controller = Controller(handler, hostname=CONFIG['host'], port=CONFIG['port'])
    
    try:
        # Start the SMTP server
        controller.start()
        logging.info(f"SMTP server running on {CONFIG['host']}:{CONFIG['port']}")
        logging.info(f"Saving attachments to {os.path.abspath(CONFIG['attachment_dir'])}")
        logging.info(f"Logs available at {os.path.abspath(CONFIG['log_dir'])}")
        
        # Keep the server running
        asyncio.get_event_loop().run_forever()
        
    except KeyboardInterrupt:
        controller.stop()
        logging.info("Server stopped")
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
        controller.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()