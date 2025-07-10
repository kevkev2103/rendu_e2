# 🎯 Veille Technologique : Analyse de Sentiments avec Hugging Face

## 📋 Description du Projet

Ce projet réalise une veille technologique et un benchmark de services d'analyse de sentiments proposés par Hugging Face. Il s'inscrit dans le cadre d'une certification en intelligence artificielle (Bloc de compétence 2 - E2).

### Objectifs
- **Fonctionnel :** Proposer un service d'IA capable de détecter le sentiment d'un texte court
- **Technique :** Comparer 3 modèles d'analyse de sentiments sur Hugging Face
- **Pédagogique :** Démontrer les compétences C6, C7 et C8 de la certification

## 🚀 Installation et Utilisation

### Prérequis
- Python 3.8 ou supérieur
- 4 GB de RAM minimum (pour les modèles locaux)
- Connexion internet (pour télécharger les modèles)

### Installation

1. **Cloner le projet :**
```bash
git clone [url-du-repo]
cd rendu_e2
```

2. **Installer les dépendances :**
```bash
pip install -r requirements.txt
```

3. **Lancer le benchmark :**
```bash
python sentiment_analysis_benchmark.py
```

### Modes d'Exécution

Le script propose deux modes de test :

1. **Mode Local (Recommandé)**
   - Télécharge et utilise les modèles en local
   - Pas de limite de requêtes
   - Premier lancement plus long (téléchargement des modèles)

2. **Mode API (Gratuit)**
   - Utilise l'API Hugging Face
   - Limite de 30 requêtes/jour
   - Plus rapide pour les tests ponctuels

## 📊 Modèles Testés

### 1. DistilBERT English
- **Modèle :** `distilbert-base-uncased-finetuned-sst-2-english`
- **Langues :** Anglais uniquement
- **Classification :** Binaire (positif/négatif)
- **Avantages :** Rapide, précis, léger
- **Taille :** 268 MB

### 2. BERT Multilingue
- **Modèle :** `nlptown/bert-base-multilingual-uncased-sentiment`
- **Langues :** EN, FR, DE, ES, IT
- **Classification :** 5 étoiles (converti en positif/neutre/négatif)
- **Avantages :** Multilingue, granulaire
- **Taille :** 438 MB

### 3. RoBERTa Twitter
- **Modèle :** `cardiffnlp/twitter-roberta-base-sentiment`
- **Langues :** Anglais uniquement
- **Classification :** Ternaire (positif/neutre/négatif)
- **Avantages :** Optimisé réseaux sociaux
- **Taille :** 499 MB

## 📈 Résultats Attendus

Le script génère :

1. **Tableau comparatif** en console
2. **Graphiques** sauvegardés dans `benchmark_results.png`
3. **Résultats détaillés** dans `detailed_results.json`
4. **Recommandations** d'usage

### Exemple de Sortie
```
🎯 BENCHMARK D'ANALYSE DE SENTIMENTS - HUGGING FACE
============================================================

📊 Test du modèle: distilbert-english
----------------------------------------
✅ Temps de réponse moyen: 0.152s
✅ Nombre de tests réussis: 10
   Exemple 1: 'This product is absolutely amazing! I love it!' → POSITIVE (0.99)
   Exemple 2: 'The service was terrible and the staff was rude.' → NEGATIVE (0.98)
   Exemple 3: 'It's okay, nothing special but works fine.' → POSITIVE (0.67)
```

## 📁 Structure du Projet

```
rendu_e2/
├── sentiment_analysis_benchmark.py  # Script principal
├── requirements.txt                  # Dépendances Python
├── README.md                        # Documentation
├── synthese_veille.md              # Synthèse de veille
├── contexte.txt                     # Contexte du projet
├── benchmark_results.png            # Graphiques (généré)
└── detailed_results.json            # Résultats détaillés (généré)
```

## 🔧 Personnalisation

### Ajouter de Nouveaux Modèles

Modifiez la section `self.models` dans `sentiment_analysis_benchmark.py` :

```python
'nouveau-modele': {
    'name': 'nom/du-modele-huggingface',
    'languages': ['en', 'fr'],
    'description': 'Description du modèle',
    'expected_accuracy': 'XX.X%',
    'model_size_mb': 300,
    'api_endpoint': 'https://api-inference.huggingface.co/models/nom/du-modele'
}
```

### Modifier les Exemples de Test

Éditez `self.test_samples` pour ajouter vos propres phrases de test :

```python
self.test_samples = {
    'en': [
        "Votre phrase en anglais",
        # ...
    ],
    'fr': [
        "Votre phrase en français",
        # ...
    ]
}
```

## 📚 Compétences Démontrées

### C6 : Organisation d'une veille technologique
- ✅ Sélection ciblée de modèles pertinents
- ✅ Documentation structurée des résultats
- ✅ Synthèse comparative

### C7 : Benchmark de services IA
- ✅ Comparaison quantitative (temps, précision)
- ✅ Évaluation qualitative (accessibilité, documentation)
- ✅ Recommandations d'usage

### C8 : Paramétrage via API
- ✅ Intégration avec l'API Hugging Face
- ✅ Utilisation des pipelines Transformers
- ✅ Gestion des erreurs et limites

## 🚨 Dépannage

### Erreurs Courantes

1. **"CUDA out of memory"**
   - Solution : Utilisez le mode CPU ou réduisez la taille des modèles

2. **"Model not found"**
   - Solution : Vérifiez la connexion internet et le nom du modèle

3. **"API rate limit exceeded"**
   - Solution : Passez en mode local ou attendez le lendemain

### Optimisations

- **Premier lancement :** Les modèles sont téléchargés (~1.5 GB)
- **Lancements suivants :** Utilisation des modèles en cache
- **Mode API :** Plus rapide mais limité à 30 requêtes/jour

## 📄 Licence

Ce projet est réalisé dans le cadre d'une certification en intelligence artificielle.

## 👨‍💻 Auteur

Kevin Packianathan - Certification IA - Bloc de compétence 2 - E2

