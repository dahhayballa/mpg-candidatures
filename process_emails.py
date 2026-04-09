import sys
import os
from datetime import datetime

# Add current dir to path for imports to work regardless of execution location
sys.path.append(os.path.dirname(__file__))

import config
from infrastructure.persistence.sqlite_repository import SqliteCandidateRepository, SqliteAuditLogRepository
from infrastructure.external.imap_service import ImapEmailAdapter, FileStorageAdapter
from core.use_cases.ingest_emails import IngestEmailsUseCase

def main():
    print("=" * 56)
    print("  MPG — Expert-Grade Email Processing (Clean Arch)")
    print("=" * 56)
    
    start_time = datetime.now()
    
    # --- Dependencies ---
    email_config = {
        'IMAP_SERVER': config.IMAP_SERVER,
        'IMAP_PORT': config.IMAP_PORT,
        'USE_SSL': config.USE_SSL,
        'EMAIL_ADDRESS': config.EMAIL_ADDRESS,
        'PASSWORD': config.PASSWORD,
        'DEADLINE': config.DEADLINE if hasattr(config, 'DEADLINE') else "2026-03-31 14:00",
        'SPECIALTIES': config.SPECIALTIES,
        'CV_KEYWORDS': config.CV_KEYWORDS,
        'MOTIVATION_KEYWORDS': config.MOTIVATION_KEYWORDS,
        'ID_KEYWORDS': config.ID_KEYWORDS,
        'DIPLOMA_KEYWORDS': config.DIPLOMA_KEYWORDS
    }
    
    # Check if DB exists
    if not os.path.exists(config.DB_PATH):
        print(f"⚠ Warning: {config.DB_PATH} not found. Ensure tables are created.")
        
    email_service = ImapEmailAdapter(email_config)
    candidate_repo = SqliteCandidateRepository(config.DB_PATH)
    attachment_provider = FileStorageAdapter(config.ATTACHMENTS_DIR)
    
    ingest_uc = IngestEmailsUseCase(
        email_service, 
        candidate_repo, 
        attachment_provider, 
        email_config
    )
    
    # --- Execute ---
    print(f"📡 Fetching emails from {config.EMAIL_ADDRESS} ...")
    try:
        processed = ingest_uc.execute(batch_size=config.BATCH_SIZE)
        print(f"✅ Processed {processed} emails.")
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
    finally:
        email_service.logout()

    duration = (datetime.now() - start_time).total_seconds()
    print(f"\n📊 Total duration: {duration:.1f}s")
    print("=" * 56)

if __name__ == "__main__":
    main()
