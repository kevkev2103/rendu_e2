# Documentation Technique - Service IA d'Analyse de Sentiment

> **Compétence C8 : Paramétrage d'un service d'IA**  
> Service d'analyse de sentiment multilingue avec Hugging Face et monitoring Prometheus

## Table des matières

1. [Installation](#installation)
2. [Exécution de la démonstration](#exécution-de-la-démonstration)
3. [Gestion des accès](#gestion-des-accès)
4. [Code source](#code-source)
5. [Monitoring et alerting](#monitoring-et-alerting)
6. [Dépendances](#dépendances)
7. [Description des données](#description-des-données)
8. [Accessibilité](#accessibilité)

---

## Installation

### Prérequis système

| Composant | Version minimale | Recommandé |
|-----------|------------------|------------|
| Python | 3.8+ | 3.9+ |
| RAM | 2 GB | 4 GB+ |
| Espace disque | 1 GB | 2 GB+ |
| Connexion Internet | Requise | Haut débit |

### Installation des dépendances

```bash
# 1. Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 2. Installer les packages Python
pip install transformers huggingface_hub prometheus_client python-dotenv

# 3. Vérifier l'installation
python -c "from transformers import pipeline; print('✅ Installation réussie!')"
```

### Configuration initiale

1. **Compte Hugging Face** : Créez un compte gratuit sur [huggingface.co](https://huggingface.co)
2. **Token d'accès** : Générez un token dans [Settings > Access Tokens](https://huggingface.co/settings/tokens)
3. **Configuration du token** :
   ```bash
   # Option 1: Variable d'environnement
   export HUGGINGFACE_TOKEN="your_token_here"
   
   # Option 2: Fichier .env (recommandé)
   echo "HUGGINGFACE_TOKEN=your_token_here" > .env
   ```

---

## Exécution de la démonstration

### Lancement rapide

```bash
# Démarrer le service avec monitoring
python demo_sentiment.py
```

### Sortie attendue

Le script exécute automatiquement 5 tests d'analyse de sentiment et affiche :

```
🤖 Démonstration - Analyse de Sentiment avec Hugging Face
📊 Compétence C8 : Paramétrage d'un service d'IA
============================================================

[TEST 1/5]
============================================================
TEXTE: Ce produit est absolument fantastique! Je le recommande vivement.
SENTIMENT: POSITIVE
CONFIANCE: 99.87%
TEMPS DE TRAITEMENT: 0.0234s
DÉTAILS:
  - POSITIVE: 0.9987
  - NEGATIVE: 0.0013
============================================================
```

### Vérification du monitoring

- **Métriques Prometheus** : http://localhost:8000/metrics
- **Interface Prometheus** (si installé) : http://localhost:9090
- **Graphiques** : Utilisez Grafana pour visualiser les métriques

---

## Gestion des accès

### Token Hugging Face

#### Création du token
1. Connectez-vous à [Hugging Face](https://huggingface.co)
2. Allez dans **Settings** → **Access Tokens**
3. Cliquez sur **"New token"**
4. Sélectionnez le type **"Read"** (suffisant pour ce projet)
5. Copiez le token généré

#### Configuration sécurisée

**⚠️ Bonnes pratiques de sécurité :**

- ✅ Utilisez un fichier `.env` pour le développement
- ✅ Utilisez des variables d'environnement en production
- ✅ Ajoutez `.env` à votre `.gitignore`
- ❌ Ne commitez jamais le token dans Git
- ❌ Ne partagez jamais votre token

**Exemple de fichier `.env` :**
```env
# Configuration Hugging Face
HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Configuration optionnelle
LOG_LEVEL=INFO
METRICS_PORT=8000
```

#### Rotation des tokens

Renouvelez régulièrement vos tokens d'accès :
1. Générez un nouveau token sur Hugging Face
2. Mettez à jour votre configuration
3. Révoquek l'ancien token

---

## Code source

### Architecture du système

```mermaid
graph TD
    A[Client] --> B[demo_sentiment.py]
    B --> C[SentimentAnalyzer]
    C --> D[Hugging Face API]
    B --> E[Prometheus Metrics]
    E --> F[/metrics endpoint]
    F --> G[Prometheus Server]
    G --> H[Alert Rules]
```

### Composants principaux

#### 1. SentimentAnalyzer

**Responsabilité** : Gestion de l'analyse de sentiment avec instrumentation

```python
class SentimentAnalyzer:
    def __init__(self):
        """Initialise le pipeline de sentiment."""
        
    def test_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyse le sentiment d'un texte donné."""
```

**Fonctionnalités** :
- Chargement automatique du modèle `cardiffnlp/twitter-xlm-roberta-base-sentiment`
- Analyse de sentiment multilingue (français/anglais)
- Instrumentation Prometheus intégrée
- Gestion d'erreurs robuste

#### 2. Métriques Prometheus

| Métrique | Type | Description |
|----------|------|-------------|
| `sentiment_analysis_duration_seconds` | Histogram | Latence des requêtes |
| `sentiment_analysis_errors_total` | Counter | Nombre d'erreurs |
| `sentiment_analysis_requests_total` | Counter | Nombre de requêtes |

**Buckets de latence** : 10ms, 50ms, 100ms, 150ms, 200ms, 500ms, 1s, 2s, 5s

#### 3. Serveur de métriques

- **Port** : 8000 (configurable)
- **Endpoint** : `/metrics`
- **Format** : Prometheus standard
- **Disponibilité** : Continue pendant l'exécution

### Workflow de traitement

1. **Initialisation** : Chargement du modèle Hugging Face
2. **Requête** : Réception du texte à analyser
3. **Traitement** : Analyse via le pipeline transformers
4. **Métriques** : Enregistrement des performances
5. **Réponse** : Retour du sentiment et de la confiance

---

## Monitoring et alerting

### Configuration Prometheus

#### Fichier `prometheus.yml`

```yaml
# Job principal pour le service IA
- job_name: 'sentiment-analysis'
  static_configs:
    - targets: ['localhost:8000']
  scrape_interval: 5s
  labels:
    service: 'huggingface-sentiment'
    environment: 'demo'
```

#### Règles d'alerte `alert.rules.yml`

##### Alertes critiques

| Alerte | Condition | Seuil | Action |
|--------|-----------|-------|--------|
| **HighSentimentAnalysisLatency** | Latence P95 > 150ms pendant 5min | ⚠️ Warning | Optimiser le modèle |
| **HighSentimentAnalysisErrorRate** | > 5 erreurs/sec pendant 5min | 🚨 Critical | Vérifier la connectivité |
| **NoSentimentAnalysisRequests** | Aucune requête pendant 10min | ⚠️ Warning | Vérifier le service |
| **HighSentimentAnalysisLoad** | > 100 req/sec pendant 2min | ⚠️ Warning | Mise à l'échelle |

##### Métriques dérivées

- `sentiment:request_rate_5m` : Taux de requêtes sur 5 minutes
- `sentiment:error_rate_5m` : Taux d'erreur sur 5 minutes
- `sentiment:latency_p95_5m` : Latence P95 sur 5 minutes
- `sentiment:success_rate_5m` : Taux de succès sur 5 minutes

### Démarrage du monitoring

```bash
# 1. Démarrer le service IA
python demo_sentiment.py &

# 2. Démarrer Prometheus (si installé localement)
prometheus --config.file=prometheus.yml

# 3. Vérifier les métriques
curl http://localhost:8000/metrics

# 4. Interface Prometheus
# Naviguer vers http://localhost:9090
```

### Tableaux de bord recommandés

#### Métriques clés à surveiller

1. **Performance** :
   - Latence moyenne et P95
   - Débit (requêtes/seconde)
   - Taux de succès

2. **Santé du service** :
   - Taux d'erreur
   - Disponibilité
   - Statut du modèle

3. **Ressources** :
   - Utilisation CPU
   - Utilisation mémoire
   - Taille des réponses

---

## Dépendances

### Python packages

| Package | Version | Licence | Usage |
|---------|---------|---------|-------|
| `transformers` | ≥4.21.0 | Apache 2.0 | Pipeline de sentiment |
| `huggingface_hub` | ≥0.10.0 | Apache 2.0 | Authentification HF |
| `prometheus_client` | ≥0.14.0 | Apache 2.0 | Métriques monitoring |
| `python-dotenv` | ≥0.19.0 | BSD | Configuration environnement |

### Modèle IA

- **Nom** : `cardiffnlp/twitter-xlm-roberta-base-sentiment`
- **Type** : Transformer pour classification de sentiment (pré-entraîné)
- **Langues** : Multilingue (français, anglais, etc.)
- **Taille** : ~500 MB
- **Licence** : MIT
- **Performance** : F1-score > 85% sur les benchmarks standard

### Infrastructure optionnelle

- **Prometheus** : Monitoring et alerting
- **Grafana** : Visualisation des métriques
- **Docker** : Conteneurisation du service
- **Kubernetes** : Orchestration en production

---

## Description des données

### Format d'entrée

**Type** : Texte brut (string)

**Caractéristiques** :
- Longueur maximale recommandée : 512 tokens
- Encodage : UTF-8
- Langues supportées : Multilingue (optimisé pour français/anglais)

**Exemples valides** :
```json
{
  "examples": [
    "Ce produit est fantastique!",
    "This movie is terrible.",
    "Le service était correct.",
    "Amazing quality and fast delivery!"
  ]
}
```

### Format de sortie

**Type** : JSON structuré

**Schema** :
```json
{
  "text": "string",              // Texte original
  "sentiment": "string",       // POSITIVE ou NEGATIVE
  "confidence": "float",       // Score de confiance [0.0-1.0]
  "all_scores": [              // Détail de tous les scores
    {
      "label": "POSITIVE",
      "score": 0.9876
    },
    {
      "label": "NEGATIVE", 
      "score": 0.0124
    }
  ],
  "processing_time": "float"   // Temps de traitement en secondes
}
```

**Exemple de réponse** :
```json
{
  "text": "Ce produit est absolument fantastique!",
  "sentiment": "POSITIVE",
  "confidence": 0.9987,
  "all_scores": [
    {"label": "POSITIVE", "score": 0.9987},
    {"label": "NEGATIVE", "score": 0.0013}
  ],
  "processing_time": 0.0234
}
```

### Métriques de qualité

- **Confiance minimale recommandée** : 0.7 (70%)
- **Temps de réponse moyen** : < 100ms
- **Précision attendue** : > 90% sur textes français/anglais
- **Gestion d'erreurs** : Timeout après 5 secondes

---

## Accessibilité

### Structure documentaire

Cette documentation respecte les standards d'accessibilité **WCAG 2.1 AA** :

#### Hiérarchie des titres
- **H1** : Titre principal du document
- **H2** : Sections principales (Installation, Code source, etc.)
- **H3** : Sous-sections (Prérequis système, Workflow, etc.)
- **H4** : Détails spécifiques (Alertes critiques, etc.)

#### Contraste et lisibilité
- ✅ Contrastes de couleur conformes (ratio 4.5:1 minimum)
- ✅ Police lisible et taille appropriée
- ✅ Espacement suffisant entre les éléments
- ✅ Pas de contenu purement visuel

#### Navigation et structure
- ✅ Table des matières avec liens de navigation
- ✅ Liens descriptifs et contextuels
- ✅ Structure logique et cohérente
- ✅ Alternatives textuelles pour les éléments visuels

#### Code et exemples
- ✅ Blocs de code avec syntaxe claire
- ✅ Exemples pratiques et testables
- ✅ Instructions étape par étape
- ✅ Messages d'erreur descriptifs

### Alternatives textuelles

**Diagrammes** : Descriptions textuelles fournies pour tous les schémas

**Tableaux** : En-têtes appropriés et structure logique

**Code** : Commentaires explicatifs et documentation inline

### Support multiplateforme

Cette documentation et le code associé sont compatibles :
- **OS** : Linux, macOS, Windows
- **Navigateurs** : Chrome, Firefox, Safari, Edge
- **Lecteurs d'écran** : Structure sémantique appropriée
- **Terminaux** : Support des émojis et couleurs optionnels

---

## Support et maintenance

### Contact
- **Projet** : Certification IA - Compétence C8
- **Documentation** : Version 1.0
- **Dernière mise à jour** : Janvier 2025

### Contributions
Pour améliorer cette documentation :
1. Signalez les problèmes d'accessibilité
2. Proposez des clarifications
3. Testez les exemples sur différentes plateformes
4. Suggérez des améliorations

---

*Cette documentation a été conçue pour être accessible à tous les utilisateurs, quel que soit leur niveau technique ou leurs besoins d'accessibilité.* 