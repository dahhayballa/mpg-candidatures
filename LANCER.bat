@echo off
chcp 65001 > nul
echo.
echo  ===============================================
echo   EETFP-MPG — Installation et démarrage
echo  ===============================================
echo.

REM ── Vérification Python ──
python --version > nul 2>&1
if errorlevel 1 (
    echo  [ERREUR] Python n'est pas installé.
    echo  Téléchargez-le sur : https://www.python.org/downloads/
    pause
    exit /b 1
)

REM ── Installation des dépendances ──
echo  [1/3] Installation des dépendances...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo  [ERREUR] Impossible d'installer les dépendances.
    pause
    exit /b 1
)
echo  OK

REM ── Vérification de la config ──
findstr /C:"CHANGE_ME" config.py > nul
if not errorlevel 1 (
    echo.
    echo  [ATTENTION] Vous n'avez pas encore modifié le mot de passe
    echo  dans config.py !  Ouvrez ce fichier et remplacez CHANGE_ME.
    echo.
    pause
)

REM ── Traitement des e-mails ──
echo.
echo  [2/3] Traitement des e-mails (cela peut prendre plusieurs minutes)...
python process_emails.py
if errorlevel 1 (
    echo.
    echo  [ERREUR] Échec du traitement des e-mails.
    echo  Vérifiez config.py (serveur, mot de passe).
    pause
    exit /b 1
)

REM ── Lancement du serveur ──
echo.
echo  [3/3] Démarrage du dashboard...
echo.
echo  ► Ouvrez votre navigateur sur : http://localhost:5000
echo.
start "" http://localhost:5000
python app.py

pause
