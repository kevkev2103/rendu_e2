# Guide d'Installation - Service IA Hugging Face

## Prérequis

- **Python** ≥ 3.8
- **Compte Hugging Face** 
- **Token d'accès Hugging Face** 
- **Environnement virtuel** 

## Installation des dépendances

### 1. Activer l'environnement virtuel
```bash

python3 -m venv venv
source venv/bin/activate
```

### 2. Installer les bibliothèques requises
```bash
pip install transformers huggingface_hub prometheus_client
```

### 3. Configuration du token Hugging Face

**Option 1 : Connexion interactive**
```bash
huggingface-cli login
```

**Option 2 : Variable d'environnement**
```bash
export HUGGINGFACE_TOKEN="your_token_here"
```

**Option 3 : Fichier .env (recommandé pour le développement)**
```bash
echo "HUGGINGFACE_TOKEN=your_token_here" > .env
pip install python-dotenv
```

## Vérification de l'installation

Pour vérifier que tout est correctement installé :

```bash
python -c "from transformers import pipeline; print('Installation réussie!')"
```

## Installation de Prometheus (optionnel pour monitoring local)

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install prometheus
```

### macOS
```bash
brew install prometheus
```

### Docker (toutes plateformes)
```bash
docker run -d --name prometheus -p 9090:9090 prom/prometheus
```

## Prochaines étapes

1. Exécuter le script de démonstration : `python demo_sentiment.py`
2. Consulter la documentation complète dans `DOCS.md`
3. Configurer le monitoring avec les fichiers Prometheus fournis

## Dépannage

### Erreur de token
Si vous obtenez une erreur d'authentification :
- Vérifiez que votre token est valide sur https://huggingface.co/settings/tokens
- Assurez-vous que le token a les permissions appropriées

### Erreur de connexion
- Vérifiez votre connexion internet
- Certains réseaux d'entreprise peuvent bloquer l'accès à Hugging Face

### Problèmes de dépendances
```bash
pip install --upgrade pip
pip install --force-reinstall transformers huggingface_hub prometheus_client
``` 