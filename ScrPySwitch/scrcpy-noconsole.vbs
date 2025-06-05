' =============================================================================
' Script de gestion des appareils Android via ADB et Scrcpy
' Author : David PONDA E.
' * Dave | th2 k0D3
' * GitHub : https://github.com/xroot
'
' Description :
' Ce script détecte les appareils Android connectés via ADB et permet 
' à l'utilisateur de choisir un périphérique pour lancer Scrcpy en mirroring.
' =============================================================================

Option Explicit

' **Gestion des accents pour les boîtes de dialogue**
SetLocale(1036) ' 1036 = Français

Dim objShell, strCommand, strDeviceList, arrDevices, i, userChoice

' **Initialisation**
Set objShell = CreateObject("WScript.Shell")
strDeviceList = ""
userChoice = ""

' =============================================================================
' Étape 1 : Récupération des appareils connectés via ADB
' =============================================================================
strCommand = "cmd /c adb devices > temp_devices.txt 2>&1"
objShell.Run strCommand, 0, True

' =============================================================================
' Étape 2 : Lecture du fichier contenant la liste des appareils
' =============================================================================
Dim fso, file, line
Set fso = CreateObject("Scripting.FileSystemObject")

If Not fso.FileExists("temp_devices.txt") Then
    MsgBox "Erreur : fichier temp_devices.txt introuvable.", vbCritical, "ScrPySwitch"
    WScript.Quit
End If

Set file = fso.OpenTextFile("temp_devices.txt", 1)
While Not file.AtEndOfStream
    line = file.ReadLine
    ' Vérifie que la ligne contient un périphérique sans l'entête
    If InStr(line, "device") > 0 And InStr(line, "List of") = 0 Then
        strDeviceList = strDeviceList & line & vbCrLf
    End If
Wend
file.Close

' =============================================================================
' Étape 3 : Vérification des appareils détectés
' =============================================================================
If strDeviceList = "" Then
    MsgBox "Aucun appareil d" & Chr(233) & "tect" & Chr(233) & ".", vbExclamation, "ScrPySwitch"
    WScript.Quit
End If

' =============================================================================
' Étape 4 : Affichage des appareils et sélection utilisateur
' =============================================================================
arrDevices = Split(strDeviceList, vbCrLf)
Dim deviceDict
Set deviceDict = CreateObject("Scripting.Dictionary")

For i = 0 To UBound(arrDevices)
    If arrDevices(i) <> "" Then
        deviceDict.Add i+1, arrDevices(i)
    End If
Next

' Si un seul appareil est détecté, démarrage automatique
If deviceDict.Count = 1 Then
    Dim singleSerial
    singleSerial = Split(deviceDict(1), vbTab)(0) ' Extraction du numéro de série
    MsgBox "Un seul appareil d" & Chr(233) & "tect" & Chr(233) & " : " & singleSerial, vbInformation, "ScrPySwitch"
    strCommand = "cmd /c scrcpy.exe -s " & Trim(singleSerial) & " --always-on-top --pause-on-exit=if-error"
    objShell.Run strCommand, 1, False
    WScript.Quit
End If

' =============================================================================
' Étape 5 : Sélection de l'appareil par l'utilisateur
' =============================================================================
Dim menu
menu = "Appareils d" & Chr(233) & "tect" & Chr(233) & "s : " & vbCrLf & vbCrLf
For Each i In deviceDict.Keys
    menu = menu & "[" & i & "] " & deviceDict(i) & vbCrLf 
Next

userChoice = InputBox(menu & vbCrLf & "Entrez le num" & Chr(233) & "ro du p" & Chr(233) & "riph" & Chr(233) & "rique :", "ScrPySwitch")

' Vérifie si le choix est valide
If Not deviceDict.Exists(CInt(userChoice)) Then
    MsgBox "Choix invalide.", vbCritical, "ScrPySwitch"
    WScript.Quit
End If

' **Extraction du numéro de série**
Dim serial
serial = Split(deviceDict(CInt(userChoice)), vbTab)(0) ' Numéro de série extrait

' =============================================================================
' Étape 6 : Lancement de scrcpy avec l'appareil sélectionné
' =============================================================================
strCommand = "cmd /c scrcpy.exe -s " & Trim(serial) & " --always-on-top --pause-on-exit=if-error"
objShell.Run strCommand, 1, False

' **Nettoyage du fichier temporaire**
fso.DeleteFile "temp_devices.txt"

' **Confirmation**
MsgBox "Le mirroring de l" & Chr(233) & "appareil " & serial & " a d" & Chr(233) & "marr" & Chr(233) & " !", vbInformation, "ScrPySwitch"