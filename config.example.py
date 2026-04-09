IMAP_SERVER       = "mail.votredomaine.mr"
IMAP_PORT         = 993
USE_SSL           = True
EMAIL_ADDRESS     = "votre@email.mr"
PASSWORD          = "VOTRE_MOT_DE_PASSE"
DB_PATH           = "candidates.db"
ATTACHMENTS_DIR   = "pieces_jointes"
BATCH_SIZE        = 10
FLASK_PORT        = 5000
FLASK_DEBUG       = False
QUOTAS = {
    "Maintenance industrielle":           20,
    "Électricité industrielle":           30,
    "Tuyauterie industrielle":            30,
    "Construction métallique et soudure": 40,
    "HSE":                                40,
    "Opérations pétrolières et gazières": 20,
    "Techniques minières":                20,
}
QUOTA_TOTAL       = 200
DIVERGENCE_SEUIL  = 15
ANTHROPIC_API_KEY = "sk-ant-VOTRE_CLE_ICI"