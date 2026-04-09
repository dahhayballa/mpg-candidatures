from __future__ import annotations
import imaplib
import email
from email.utils import parseaddr, parsedate_to_datetime
from datetime import datetime
from typing import List, Dict, Any, Optional, cast, Union
import os
import re

# Root absolute imports
from core.interfaces.gateways import IEmailService, IAttachmentProvider

class ImapEmailAdapter(IEmailService):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.mail: Optional[imaplib.IMAP4] = None
        self._connect()

    def _connect(self) -> None:
        server = str(self.config['IMAP_SERVER'])
        port = int(self.config['IMAP_PORT'])
        if self.config.get('USE_SSL', True):
            self.mail = imaplib.IMAP4_SSL(server, port)
        else:
            self.mail = imaplib.IMAP4(server, port)
        
        if self.mail:
            self.mail.login(str(self.config['EMAIL_ADDRESS']), str(self.config['PASSWORD']))

    def fetch_emails(self, batch_size: int = 10) -> List[Dict[str, Any]]:
        if not self.mail: return []
        
        self.mail.select("INBOX")
        _, search_data = self.mail.search(None, "ALL")
        if not search_data or not search_data[0]: return []
        
        all_ids = search_data[0].split()
        batch = all_ids[-batch_size:]
        if not batch: return []
        
        # Convert bytes IDs to comma-separated string
        ids_str = ",".join([i.decode('utf-8', errors='ignore') for i in batch])
        
        _, msgs = self.mail.fetch(ids_str, "(RFC822)")
        results: List[Dict[str, Any]] = []
        
        for response_part in msgs:
            if not isinstance(response_part, tuple): continue
            
            # response_part[1] is the raw message bytes
            raw_msg = response_part[1]
            if not isinstance(raw_msg, bytes): continue
            
            msg = email.message_from_bytes(raw_msg)
            
            raw_from = str(msg.get("From", ""))
            name_raw, addr_raw = parseaddr(self._decode_str(raw_from))
            
            date_raw = str(msg.get("Date", ""))
            try:
                date_obj = parsedate_to_datetime(date_raw)
                date_str = date_obj.strftime("%Y-%m-%d %H:%M")
            except:
                date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

            results.append({
                "email_addr": addr_raw.lower().strip(),
                "name": name_raw or addr_raw.split("@")[0],
                "subject": self._decode_str(str(msg.get("Subject", ""))),
                "date": date_str,
                "body": self._get_body(msg),
                "parts": [p for p in msg.walk() if p.get_content_disposition() == "attachment"]
            })
        return results

    def _decode_str(self, s: str) -> str:
        from email.header import decode_header
        if not s: return ""
        try:
            parts = decode_header(s)
            res = ""
            for p, enc in parts:
                if isinstance(p, bytes): res += p.decode(enc or "utf-8", errors="replace")
                else: res += str(p)
            return res.strip()
        except: return str(s).strip()

    def _get_body(self, msg: email.message.EmailMessage) -> str:
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition", "")):
                    try:
                        payload = part.get_payload(decode=True)
                        if isinstance(payload, bytes):
                            body = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
                            break
                    except: pass
        else:
            try:
                payload = msg.get_payload(decode=True)
                if isinstance(payload, bytes):
                    body = payload.decode(msg.get_content_charset() or "utf-8", errors="replace")
            except: pass
        return body

    def logout(self) -> None:
        if self.mail:
            try: self.mail.logout()
            except: pass
        self.mail = None

class FileStorageAdapter(IAttachmentProvider):
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def get_candidate_folder(self, email_addr: str) -> str:
        safe_email = re.sub(r'[^\w@.-]', '_', email_addr)
        return os.path.join(self.base_dir, safe_email)

    def save_attachment(self, part: Any, folder: str) -> str:
        filename = part.get_filename()
        if not filename: return ""
        filename = re.sub(r'[<>:"/\\|?*]', '_', str(filename))
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)
        try:
            payload = part.get_payload(decode=True)
            if isinstance(payload, bytes):
                with open(filepath, "wb") as f:
                    f.write(payload)
                return filename
        except: pass
        return ""
