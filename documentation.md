# 📚 Guide Complet - Service IA d'Analyse de Sentiment

> **Pour les développeurs débutants**  
> Service d'analyse de sentiment multilingue avec Hugging Face

## 🎯 **C'est quoi ce projet ?**

Imaginez que vous voulez savoir si les gens aiment ou détestent un film en analysant leurs commentaires. Ce projet fait exactement ça ! Il utilise l'intelligence artificielle pour comprendre le sentiment (positif/négatif) dans un texte.

**Exemple concret :**
- Texte : "Ce film est génial !" → Sentiment : POSITIF (95% de confiance)
- Texte : "Très décevant" → Sentiment : NÉGATIF (87% de confiance)

---

## 📋 **Table des matières**

1. [🚀 Installation rapide](#installation-rapide)
2. [🔧 Configuration](#configuration)
3. [🧪 Tester le service](#tester-le-service)
4. [📊 Comprendre le code](#comprendre-le-code)
5. [🔍 Monitoring simple](#monitoring-simple)
6. [📦 Dépendances](#dépendances)
7. [📝 Formats de données](#formats-de-données)
8. [♿ Accessibilité](#accessibilité)

---

## 🚀 **Installation rapide**

### **Étape 1 : Vérifier Python**
Vous devez avoir Python 3.8 ou plus récent. Vérifiez avec :
```bash
python3 --version
```

### **Étape 2 : Créer un environnement propre**
```bash
# Créer un dossier pour le projet
mkdir mon-projet-sentiment
cd mon-projet-sentiment

# Créer un environnement virtuel (comme une boîte isolée)
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate     # Sur Windows
```

### **Étape 3 : Installer les outils**
```bash
# Installer toutes les bibliothèques nécessaires
pip install transformers huggingface_hub prometheus_client python-dotenv tabulate tiktoken
```

### **Étape 4 : Vérifier que ça marche**
```bash
python -c "from transformers import pipeline; print('✅ Tout est installé !')"
```

---

## 🔧 **Configuration**

### **Créer un compte Hugging Face**
1. Allez sur [huggingface.co](https://huggingface.co)
2. Cliquez sur "Sign Up" (c'est gratuit)
3. Confirmez votre email

### **Obtenir votre clé d'accès (token)**
1. Connectez-vous sur Hugging Face
2. Cliquez sur votre photo → "Settings"
3. Dans le menu de gauche, cliquez "Access Tokens"
4. Cliquez "New token"
5. Donnez un nom (ex: "mon-projet")
6. Sélectionnez "Read"
7. **COPIEZ** le token (il commence par `hf_...`)

### **Configurer le token**
```bash
# Créer un fichier .env avec votre token
echo "HUGGINGFACE_TOKEN=votre_token_ici" > .env
```

**⚠️ Important :** Remplacez `votre_token_ici` par le vrai token que vous avez copié !

---

## 🧪 **Tester le service**

### **Lancer le test**
```bash
python demo_sentiment.py
```

### **Ce qui va se passer**
Le script va :
1. 📥 Télécharger le modèle IA (première fois seulement, ~500 MB)
2. 🤖 Analyser 5 exemples de textes
3. 📊 Afficher les résultats
4. 🌐 Démarrer un serveur de métriques sur le port 8000

### **Exemple de sortie**
```
🤖 Démonstration - Analyse de Sentiment avec Hugging Face
📊 Compétence C8 : Paramétrage d'un service d'IA
============================================================

[TEST 1/5]
============================================================
TEXTE: Ce produit est absolument fantastique! Je le recommande vivement.
SENTIMENT: 5 stars
CONFIANCE: 90.57%
TEMPS DE TRAITEMENT: 0.6546s
============================================================
```


## 📊 **Comprendre le code**

### **Structure du projet**
```
mon-projet-sentiment/
├── demo_sentiment.py      # Script principal
├── INSTALL.md            # Guide d'installation
├── DOCS.md               # Documentation technique
├── requirements.txt      # Dépendances
├── prometheus.yml        # Configuration monitoring
├── alert.rules.yml       # Règles d'alerte
└── .env                  # Votre token (à créer)
```

### **Le fichier principal : demo_sentiment.py**

#### **1. Import des bibliothèques**
```python
from transformers import pipeline  # Pour l'IA
from prometheus_client import Histogram, Counter  # Pour les métriques
from dotenv import load_dotenv  # Pour lire le fichier .env
```

#### **2. Configuration des métriques**
```python
# Mesurer le temps de traitement
SENTIMENT_LATENCY = Histogram(
    'sentiment_analysis_duration_seconds',
    'Temps de traitement',
    buckets=[0.01, 0.05, 0.1, 0.15, 0.2, 0.5, 1.0, 2.0, 5.0]
)

# Compter les requêtes
SENTIMENT_REQUESTS = Counter(
    'sentiment_analysis_requests_total',
    'Nombre de requêtes',
    ['sentiment_label']
)
```

#### **3. Classe principale**
```python
class SentimentAnalyzer:
    def __init__(self):
        # Charge le modèle IA
        self.pipeline = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment",
            top_k=None
        )
    
    def test_sentiment(self, text):
        # Analyse le sentiment d'un texte
        results = self.pipeline(text)
        return results
```

#### **4. Tests automatiques**
```python
test_texts = [
    "Ce produit est absolument fantastique!",  # Positif
    "Service client décevant, très lent.",     # Négatif
    "Le film était correct, sans plus.",       # Neutre
    "This product is amazing!",                # Anglais positif
    "Terrible experience!",                    # Anglais négatif
]
```

---

## 🔍 **Monitoring simple**

### **Qu'est-ce que le monitoring ?**
C'est comme un "thermomètre" qui surveille votre service :
- ⏱️ **Temps de réponse** : Est-ce que c'est rapide ?
- ❌ **Erreurs** : Est-ce que ça plante ?
- 📈 **Nombre de requêtes** : Combien de personnes utilisent le service ?

### **Voir les métriques**
```bash
# Dans un terminal
curl http://localhost:8000/metrics
```

Vous verrez quelque chose comme :
```
# HELP sentiment_analysis_duration_seconds Temps de traitement
# TYPE sentiment_analysis_duration_seconds histogram
sentiment_analysis_duration_seconds_bucket{le="0.01"} 0
sentiment_analysis_duration_seconds_bucket{le="0.05"} 2
sentiment_analysis_duration_seconds_bucket{le="0.1"} 3
```

### **Interface web (optionnel)**
Si vous installez Prometheus :
```bash
# Installer Prometheus
sudo apt install prometheus  # Ubuntu/Debian
# ou
brew install prometheus      # macOS

# Lancer Prometheus
prometheus --config.file=prometheus.yml

# Ouvrir dans le navigateur
# http://localhost:9090
```

---

## 📦 **Dépendances**

### **Bibliothèques Python utilisées**

| Bibliothèque | À quoi ça sert | Version |
|--------------|----------------|---------|
| `transformers` | Modèles IA Hugging Face | ≥4.21.0 |
| `huggingface_hub` | Connexion à Hugging Face | ≥0.10.0 |
| `torch` | Moteur IA (PyTorch) | ≥1.11.0 |
| `prometheus_client` | Métriques et monitoring | ≥0.14.0 |
| `python-dotenv` | Lecture du fichier .env | ≥0.19.0 |
| `tabulate` | Affichage de tableaux | ≥0.8.9 |
| `tiktoken` | Tokenisation avancée | ≥0.5.0 |

### **Modèle IA utilisé**
- **Nom** : `nlptown/bert-base-multilingual-uncased-sentiment`
- **Type** : Analyse de sentiment multilingue
- **Langues** : Français, anglais, et plus
- **Taille** : ~500 MB
- **Performance** : Très bonne sur le français

---

## 📝 **Formats de données**

### **Ce que vous envoyez au service**
```python
# Un simple texte
texte = "Ce film est génial !"
```

### **Ce que le service vous répond**
```python
{
    "text": "Ce film est génial !",
    "sentiment": "5 stars",
    "confidence": 0.9057,
    "all_scores": [
        {"label": "5 stars", "score": 0.9057},
        {"label": "4 stars", "score": 0.0786},
        {"label": "3 stars", "score": 0.0128},
        {"label": "2 stars", "score": 0.0011},
        {"label": "1 star", "score": 0.0018}
    ],
    "processing_time": 0.6546
}
```

### **Explication des résultats**
- **sentiment** : Le sentiment détecté (1-5 stars)
- **confidence** : Niveau de confiance (0.0 à 1.0)
- **all_scores** : Scores pour tous les sentiments possibles
- **processing_time** : Temps de traitement en secondes

---

## ♿ **Accessibilité**

### **Qu'est-ce que l'accessibilité ?**
C'est rendre votre code et votre documentation utilisables par **tout le monde**, y compris :
- 👨‍🦯 Personnes malvoyantes
- 🦻 Personnes malentendantes
- 🖱️ Personnes qui utilisent uniquement le clavier
- 📱 Personnes sur mobile

### **Ce que nous avons fait pour l'accessibilité**

#### **1. Structure claire**
- ✅ **Titres hiérarchisés** : H1, H2, H3 (facilite la navigation)
- ✅ **Table des matières** : Navigation rapide
- ✅ **Liens descriptifs** : Pas de "cliquez ici"

#### **2. Contraste et lisibilité**
- ✅ **Couleurs contrastées** : Texte lisible sur fond
- ✅ **Taille de police** : Suffisamment grande
- ✅ **Espacement** : Pas de texte collé

#### **3. Alternatives textuelles**
- ✅ **Émojis avec texte** : 🚀 + "Installation rapide"
- ✅ **Code commenté** : Explications dans le code
- ✅ **Exemples concrets** : "Ce film est génial !"

#### **4. Support multiplateforme**
- ✅ **Linux, macOS, Windows** : Fonctionne partout
- ✅ **Navigateurs modernes** : Chrome, Firefox, Safari, Edge
- ✅ **Lecteurs d'écran** : Structure sémantique

### **Comment tester l'accessibilité**

#### **Test manuel**
1. **Navigation clavier** : Utilisez Tab pour naviguer
2. **Zoom** : Agrandissez à 200% (reste lisible ?)
3. **Contraste** : Imprimez en noir et blanc

#### **Outils automatiques**
```bash
# Extension navigateur
axe DevTools (Chrome/Firefox)

# En ligne
https://wave.webaim.org/
```

### **Bonnes pratiques pour votre code**

#### **1. Commentaires clairs**
```python
# ❌ Mauvais
def f(x):
    return x * 2

# ✅ Bon
def double_valeur(nombre):
    """Double la valeur d'un nombre."""
    return nombre * 2
```

#### **2. Messages d'erreur utiles**
```python
# ❌ Mauvais
raise Exception("Erreur")

# ✅ Bon
raise ValueError("Le token Hugging Face est manquant. Vérifiez votre fichier .env")
```

#### **3. Variables explicites**
```python
# ❌ Mauvais
x = 0.95

# ✅ Bon
seuil_confiance_minimum = 0.95
```

---

## 🛠️ **Dépannage**

### **Problèmes courants**

#### **1. "ModuleNotFoundError: No module named 'transformers'**
```bash
# Solution : Réinstaller
pip install --upgrade pip
pip install transformers huggingface_hub
```

#### **2. "Erreur d'authentification Hugging Face"**
```bash
# Vérifier votre token
cat .env
# Doit contenir : HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### **3. "Port 8000 déjà utilisé"**
```bash
# Changer le port dans le code
# Ligne 120 dans demo_sentiment.py
def start_metrics_server(port: int = 8001):  # Changer 8000 en 8001
```

#### **4. "Modèle trop lent"**
- ✅ Normal au premier lancement (téléchargement)
- ✅ Les lancements suivants seront plus rapides
- ✅ Le modèle est stocké localement

---

## 📚 **Ressources pour aller plus loin**

### **Documentation officielle**
- [Hugging Face](https://huggingface.co/docs) - Documentation complète
- [Transformers](https://huggingface.co/docs/transformers) - Bibliothèque IA
- [Prometheus](https://prometheus.io/docs/) - Monitoring

### **Tutoriels**
- [Analyse de sentiment avec Python](https://huggingface.co/tasks/text-classification)
- [Monitoring avec Prometheus](https://prometheus.io/docs/guides/)

### **Communauté**
- [Forum Hugging Face](https://discuss.huggingface.co/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/huggingface)

---

## 📞 **Support**

### **En cas de problème**
1. **Vérifiez les logs** : Messages d'erreur dans le terminal
2. **Testez étape par étape** : Installation → Configuration → Test
3. **Consultez la documentation** : Ce guide et les liens ci-dessus
4. **Demandez de l'aide** : Communautés mentionnées

### **Améliorer cette documentation**
Si vous trouvez des erreurs ou des améliorations :
1. Signalez les problèmes d'accessibilité
2. Proposez des clarifications
3. Testez sur votre machine
4. Partagez vos retours

---

## 🎉 **Félicitations !**

Vous avez maintenant un service d'analyse de sentiment fonctionnel ! 

**Ce que vous savez faire :**
- ✅ Installer et configurer un service IA
- ✅ Analyser le sentiment de textes en français/anglais
- ✅ Surveiller les performances
- ✅ Documenter de manière accessible

**Prochaines étapes :**
- 🔄 Intégrer dans votre application
- 📊 Ajouter plus de métriques
- 🌐 Déployer en production
- 🧪 Tester avec vos propres données

**Bon développement !** 🚀

---

