# RefreshEnv.cmd

**Auteur** : David PONDA  
**Contact** : david.ponda@gmail.com  
**Copyright** : 2024 | David PONDA - Je suis votre Maquette

## 🌟 Description
`RefreshEnv.cmd` est un script batch permettant de **rafraîchir les variables d’environnement Windows** sans nécessiter un redémarrage du PC. Il recharge dynamiquement les paramètres système et utilisateur depuis le registre et les applique à la session en cours.

## 🚀 Fonctionnalités
✅ Recharge les **variables système** et **utilisateur**  
✅ Combine les valeurs **HKLM** et **HKCU** pour une mise à jour complète  
✅ Met à jour le **PATH** sans redémarrer Windows  
✅ Supprime les **fichiers temporaires** après exécution  
✅ **Affichage amélioré** pour une meilleure lisibilité  

## 📌 Emplacement recommandé
Pour **une exécution accessible partout dans Windows**, placez `RefreshEnv.cmd` dans **`C:\Windows\System32`**.  
Cela permet de l'exécuter depuis **n'importe quel terminal**, sans spécifier son chemin complet.

## 🔧 Utilisation
### 1️⃣ **Exécution depuis `cmd.exe`**
Ouvrez une **invite de commande** et exécutez :
```bash
RefreshEnv.cmd