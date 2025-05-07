@echo off
:: ========================================================
:: Fichier : RefreshEnv.cmd
:: Description : Recharge les variables d’environnement Windows
:: Auteur : David PONDA
:: Contact : david.ponda@gmail.com
:: Copyright 2024 | David PONDA - Je suis votre Maquette
:: ========================================================

:: Sauvegarde de l'encodage actuel
for /f "tokens=2 delims=:" %%a in ('chcp') do set OldCodePage=%%a

:: Forcer UTF-8 pour un affichage correct
chcp 65001 >nul
echo | set /p dummy="🔄 Rafraîchissement des variables d'environnement. Veuillez patienter..."

goto main

:: ========================================================
:: Définir une variable d’environnement depuis le registre
:: ========================================================
:SetFromReg
    "%WinDir%\System32\Reg" QUERY "%~1" /v "%~2" > "%TEMP%\_envset.tmp" 2>NUL
    for /f "usebackq skip=2 tokens=2,*" %%A IN ("%TEMP%\_envset.tmp") do (
        echo/set "%~3=%%B"
    )
    goto :EOF

:: ========================================================
:: Récupérer toutes les variables d’environnement du registre
:: ========================================================
:GetRegEnv
    "%WinDir%\System32\Reg" QUERY "%~1" > "%TEMP%\_envget.tmp"
    for /f "usebackq skip=2" %%A IN ("%TEMP%\_envget.tmp") do (
        if /I not "%%~A"=="Path" (
            call :SetFromReg "%~1" "%%~A" "%%~A"
        )
    )
    goto :EOF

:main
    echo/@echo off >"%TEMP%\_env.cmd"

    :: Chargement des variables système et utilisateur
    call :GetRegEnv "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" >> "%TEMP%\_env.cmd"
    call :GetRegEnv "HKCU\Environment">>"%TEMP%\_env.cmd" >> "%TEMP%\_env.cmd"

    :: Gestion spéciale du PATH (concaténation système + utilisateur)
    call :SetFromReg "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" Path Path_HKLM >> "%TEMP%\_env.cmd"
    call :SetFromReg "HKCU\Environment" Path Path_HKCU >> "%TEMP%\_env.cmd"
    echo/set "Path=%%Path_HKLM%%;%%Path_HKCU%%" >> "%TEMP%\_env.cmd"

    :: Nettoyage des fichiers temporaires
    del /f /q "%TEMP%\_envset.tmp" 2>nul
    del /f /q "%TEMP%\_envget.tmp" 2>nul

    :: Capture de l'utilisateur et de l'architecture du système
    SET "OriginalUserName=%USERNAME%"
    SET "OriginalArchitecture=%PROCESSOR_ARCHITECTURE%"

    :: Application des nouvelles variables
    call "%TEMP%\_env.cmd"

    :: Nettoyage du fichier temporaire
    del /f /q "%TEMP%\_env.cmd" 2>nul

    :: Restauration des valeurs originales
    SET "USERNAME=%OriginalUserName%"
    SET "PROCESSOR_ARCHITECTURE=%OriginalArchitecture%"

    :: Restauration de l'encodage initial
    chcp %OldCodePage% >nul

    echo | set /p dummy="✅ Rafraîchissement terminé !"
    echo.