# Système de Veille Technologique - Analyse de Sentiments

## 📋 Description du Projet

Ce projet implémente un **système complet de veille technologique** spécialisé dans l'analyse de sentiments et les technologies d'intelligence artificielle. Il permet de surveiller automatiquement les innovations, collecter des informations pertinentes, générer des alertes et produire des rapports d'analyse.

## 🎯 Objectifs Pédagogiques

Ce projet valide les **3 compétences du bloc E2 "Veille service IA"** :

### C6 : Organiser et réaliser une veille technique et réglementaire
- ✅ Organisation d'une veille systématique sur les modèles d'IA
- ✅ Collecte et traitement automatisé d'informations
- ✅ Partage des résultats via rapports et tableaux de bord
- ✅ Recommandations basées sur l'état de l'art

### C7 : Identifier des services d'IA et réaliser un benchmark
- ✅ Identification de services d'IA préexistants (Hugging Face, APIs)
- ✅ Benchmark comparatif détaillé des modèles
- ✅ Analyse des caractéristiques et performances
- ✅ Recommandations adaptées selon les contextes d'usage

### C8 : Paramétrer un service d'IA selon sa documentation
- ✅ Installation et configuration des modèles d'IA
- ✅ Tests de fonctionnement et validation
- ✅ Documentation complète de l'intégration
- ✅ Gestion des dépendances et accès

## 🔧 Architecture du Système

```
├── veille_sentiment_analysis.py    # Script principal de veille
├── dashboard_veille.py              # Tableau de bord interactif
├── sentiment_analysis_benchmark.py  # Benchmark des modèles
├── test_simple.py                   # Tests de validation
├── requirements_veille.txt          # Dépendances
└── README_veille.md                # Documentation
```

## 🚀 Installation et Configuration

### 1. Prérequis
```bash
# Python 3.8 ou supérieur
python --version

# Environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 2. Installation des dépendances
```bash
pip install -r requirements_veille.txt

# Pour le tableau de bord interactif
pip install streamlit plotly
```

### 3. Configuration initiale
```bash
# Test de l'installation
python test_simple.py

# Lancement de la première veille
python veille_sentiment_analysis.py
```

## 📊 Utilisation

### 1. Collecte de Veille Automatisée
```bash
python veille_sentiment_analysis.py
```

**Options disponibles :**
- **Option 1** : Veille complète (collecte + analyse + rapport)
- **Option 2** : Génération de rapport uniquement
- **Option 3** : Collecte RSS uniquement
- **Option 4** : Surveillance des modèles

### 2. Tableau de Bord Interactif
```bash
streamlit run dashboard_veille.py
```

**Fonctionnalités :**
- 📈 Visualisation en temps réel des données
- 🔍 Filtres par source, période, type
- 📊 Métriques et graphiques interactifs
- 📥 Export des données (CSV/JSON)

### 3. Benchmark des Modèles
```bash
python sentiment_analysis_benchmark.py
```

**Modes disponibles :**
- **Mode Local** : Test des modèles en local (recommandé)
- **Mode API** : Test via API Hugging Face (nécessite clé)

## 📋 Sources de Veille Surveillées

### 1. **Hugging Face Models**
- Nouveaux modèles d'analyse de sentiments
- Mises à jour et optimisations
- Métriques de performance

### 2. **Articles de Recherche (ArXiv)**
- Publications scientifiques récentes
- Innovations en NLP
- Nouvelles approches algorithmiques

### 3. **Dépôts GitHub**
- Projets open source populaires
- Implémentations de référence
- Outils et librairies

### 4. **Articles Medium/Blog**
- Tutoriels et guides pratiques
- Retours d'expérience
- Analyses de cas d'usage

## 🔔 Système d'Alertes

### Types d'alertes automatiques :
- **Volume élevé** : Plus de 5 nouvelles ressources en 24h
- **Contenu critique** : Mots-clés "breakthrough", "state-of-the-art"
- **Nouveaux modèles** : Détection de nouveaux modèles populaires
- **Mises à jour** : Changements dans les modèles surveillés

## 📊 Rapports Générés

### 1. Rapport Visuel
- `rapport_veille_sentiment.png` : Graphiques et métriques
- Évolution temporelle des collectes
- Répartition par sources et types
- Analyse des alertes

### 2. Rapport Textuel
- `rapport_veille_sentiment.txt` : Analyse détaillée
- Résumé exécutif
- Tendances observées
- Recommandations stratégiques

### 3. Données Brutes
- `detailed_results.json` : Résultats détaillés des tests
- `veille_sentiment.db` : Base de données SQLite complète

## 🎯 Exemples de Résultats

### Métriques de Performance
```
Modèle DistilBERT (anglais) :
- Temps de réponse : 0.045s
- Précision : 91.3%
- Taille : 268 MB

Modèle BERT Multilingue :
- Langues supportées : 5
- Précision : 85.2%
- Taille : 438 MB
```

### Recommandations Générées
- **Pour l'anglais uniquement** : DistilBERT (optimal)
- **Pour le multilingue** : BERT multilingue
- **Pour les réseaux sociaux** : RoBERTa Twitter
- **Pour la production** : Test local puis API

## 📈 Validation des Compétences

### C6 - Veille Technique
- [x] **Organisation** : Système automatisé de surveillance
- [x] **Collecte** : Multiples sources (RSS, API, web scraping)
- [x] **Traitement** : Filtrage et catégorisation automatique
- [x] **Partage** : Rapports et dashboard interactif

### C7 - Benchmark IA
- [x] **Identification** : 5+ modèles d'IA comparés
- [x] **Comparaison** : Métriques détaillées (temps, précision, taille)
- [x] **Analyse** : Avantages/inconvénients documentés
- [x] **Recommandations** : Contextes d'usage spécifiés

### C8 - Paramétrage IA
- [x] **Installation** : Scripts automatisés avec gestion d'erreurs
- [x] **Configuration** : Tests de validation inclus
- [x] **Documentation** : Guide complet d'utilisation
- [x] **Contraintes** : Gestion des dépendances et performances

## 🔍 Dépannage

### Problèmes Courants

**1. Erreur "ModuleNotFoundError"**
```bash
pip install -r requirements_veille.txt
```

**2. Erreur API 401 (Hugging Face)**
- Utiliser le mode local (option 1)
- Ou obtenir une clé API gratuite sur huggingface.co

**3. Base de données vide**
```bash
# Lancer d'abord la collecte
python veille_sentiment_analysis.py
# Puis le dashboard
streamlit run dashboard_veille.py
```

## 📚 Ressources Complémentaires

- [Hugging Face Documentation](https://huggingface.co/docs)
- [Transformers Library](https://huggingface.co/docs/transformers/)
- [ArXiv NLP Papers](https://arxiv.org/list/cs.CL/recent)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🤝 Contribution

Ce projet est conçu pour la validation des compétences E2. Pour des améliorations :

1. Fork du projet
2. Créer une branche feature
3. Commit des changements
4. Pull request avec description détaillée

---

**Auteur** : [Votre nom]  
**Date** : [Date]  
**Contexte** : Projet de validation des compétences du bloc E2 "Veille service IA" 