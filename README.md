🚀 Service d'Analyse de Sentiment avec IA
> Projet de certification IA - Compétence C8
> Service simple qui analyse le sentiment (positif/négatif) de textes en français et anglais
📋 C'est quoi ce projet ?
Ce projet utilise l'intelligence artificielle pour comprendre si un texte exprime quelque chose de positif, négatif ou neutre. Parfait pour analyser des commentaires, avis clients, ou posts sur les réseaux sociaux !
Exemple :
"Ce film est génial !" → POSITIF (95% de confiance)
"Très décevant" → NÉGATIF (87% de confiance)
�� Installation rapide
1. Vérifier Python
python3 --version  # Doit être 3.8 ou plus récent
2. Cloner le projet
git clone <votre-repo>
cd rendu_e2
3. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows


4. Installer les dépendances
pip install -r requirements.txt

⚙️ Configuration
Créer votre token Hugging Face
Allez sur huggingface.co et créez un compte
Dans Settings → Access Tokens, créez un nouveau token
Copiez le token (commence par hf_...)
Configurer le token
echo "HUGGINGFACE_TOKEN=votre_token_ici" > .env
⚠️ Important : Remplacez votre_token_ici par votre vrai token !
🧪 Tester le service
Lancer la démo
python demo_sentiment.py

Ce qui va se passer :
📥 Téléchargement du modèle IA (première fois seulement, ~500 MB)
🤖 Analyse de 5 exemples de textes
📊 Affichage des résultats
�� Démarrage du serveur de métriques sur le port 8000
Exemple de sortie
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

📊 Monitoring et métriques
Voir les métriques en temps réel
curl http://localhost:8000/metrics

Interface web Prometheus (optionnel)
# Installer Prometheus
sudo apt install prometheus  # Ubuntu/Debian

# Lancer avec votre config
prometheus --config.file=prometheus.yml

# Ouvrir http://localhost:9090 dans votre navigateur

🏗️ Structure du projet
<img width="577" height="163" alt="image" src="https://github.com/user-attachments/assets/8288abba-3e40-4ddd-88f0-bb049fe48385" />

�� Fichiers principaux expliqués
demo_sentiment.py
Classe SentimentAnalyzer : Charge le modèle IA et analyse les textes
Métriques Prometheus : Mesure les performances et erreurs
Tests automatiques : 5 exemples en français et anglais
Serveur de métriques : Port 8000 pour le monitoring
requirements.txt
transformers : Modèles IA Hugging Face
prometheus_client : Métriques et monitoring
python-dotenv : Lecture du fichier .env
prometheus.yml
Configuration du monitoring
Collecte des métriques toutes les 5 secondes
Cible : localhost:8000 (votre service)
alert.rules.yml
Alertes automatiques en cas de problème
Latence élevée, erreurs, charge importante

�� Dépannage rapide
"ModuleNotFoundError: No module named 'transformers'"
pip install --upgrade pip
pip install transformers huggingface_hub

"Erreur d'authentification Hugging Face"
# Vérifier votre fichier .env
cat .env
# Doit contenir : HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

"Port 8000 déjà utilisé"
# Changer le port dans demo_sentiment.py ligne 120
def start_metrics_server(port: int = 8001):  # Changer 8000 en 8001

"Modèle trop lent"
✅ Normal au premier lancement (téléchargement)
✅ Les lancements suivants seront plus rapides
✅ Le modèle est stocké localement
📚 Comment ça marche ?
1. Modèle IA utilisé
Nom : nlptown/bert-base-multilingual-uncased-sentiment
Type : Analyse de sentiment multilingue
Langues : Français, anglais, et plus
Taille : ~500 MB
2. Processus d'analyse
Apply to demo_sentime...
3. Métriques collectées
⏱️ Temps de traitement : Performance du modèle
❌ Erreurs : Problèmes détectés
�� Requêtes : Nombre d'analyses effectuées
🎯 Compétences validées
✅ C8 : Paramétrage d'un service d'IA
✅ C9 : Monitoring et observabilité
✅ C10 : Métriques et alertes
✅ C11 : Gestion des erreurs
✅ C12 : Logging structuré
✅ C13 : Configuration externalisée
🚀 Prochaines étapes
Tester avec vos propres textes : Modifiez test_texts dans le code
Intégrer dans une application : Utilisez la classe SentimentAnalyzer
Déployer en production : Serveur web, API REST
Ajouter plus de métriques : Temps de réponse, taux de succès
📞 Besoin d'aide ?
📖 Documentation complète : documentation.md
🐛 Problèmes : Vérifiez les logs dans le terminal
🔍 Monitoring : http://localhost:8000/metrics
�� Ressources : Hugging Face






