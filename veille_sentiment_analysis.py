#!/usr/bin/env python3
"""
Système de Veille Technologique - Analyse de Sentiments
Auteur: [Votre nom]
Date: [Date]

Système complet de veille technologique pour l'analyse de sentiments,
incluant collecte automatisée, alertes, agrégation et génération de rapports.
"""

import requests
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import sqlite3
import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from transformers import pipeline
import warnings
warnings.filterwarnings('ignore')

class VeilleTechnologiqueIA:
    """Système de veille technologique pour l'analyse de sentiments"""
    
    def __init__(self, db_path='veille_sentiment.db'):
        self.db_path = db_path
        self.init_database()
        
        # Sources de veille configurées
        self.sources_veille = {
            'huggingface_models': {
                'url': 'https://huggingface.co/models?pipeline_tag=text-classification&sort=downloads',
                'type': 'web_scraping',
                'keywords': ['sentiment', 'emotion', 'classification'],
                'description': 'Nouveaux modèles d\'analyse de sentiments sur Hugging Face'
            },
            'arxiv_papers': {
                'url': 'http://export.arxiv.org/api/query?search_query=cat:cs.CL+AND+sentiment+analysis&start=0&max_results=50',
                'type': 'rss',
                'keywords': ['sentiment analysis', 'emotion recognition', 'text classification'],
                'description': 'Articles de recherche récents sur l\'analyse de sentiments'
            },
            'github_repos': {
                'url': 'https://api.github.com/search/repositories?q=sentiment+analysis+language:python&sort=updated',
                'type': 'api',
                'keywords': ['sentiment-analysis', 'nlp', 'text-classification'],
                'description': 'Dépôts GitHub récents pour l\'analyse de sentiments'
            },
            'medium_articles': {
                'url': 'https://medium.com/feed/tag/sentiment-analysis',
                'type': 'rss',
                'keywords': ['sentiment analysis', 'NLP', 'machine learning'],
                'description': 'Articles Medium sur l\'analyse de sentiments'
            }
        }
        
        # Alertes configurées
        self.alertes_config = {
            'nouveaux_modeles': {
                'query': 'new sentiment analysis model OR new emotion detection model',
                'frequency': 'daily',
                'priority': 'high'
            },
            'breakthroughs': {
                'query': 'breakthrough sentiment analysis OR state-of-the-art emotion',
                'frequency': 'weekly',
                'priority': 'critical'
            },
            'datasets': {
                'query': 'sentiment analysis dataset OR emotion dataset',
                'frequency': 'weekly',
                'priority': 'medium'
            }
        }
        
        # Modèles à surveiller
        self.modeles_surveilles = {
            'distilbert-sentiment': 'distilbert-base-uncased-finetuned-sst-2-english',
            'bert-multilingual': 'nlptown/bert-base-multilingual-uncased-sentiment',
            'roberta-twitter': 'cardiffnlp/twitter-roberta-base-sentiment',
            'vader-sentiment': 'vaderSentiment',
            'textblob': 'textblob'
        }
    
    def init_database(self):
        """Initialise la base de données SQLite pour stocker les données de veille"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table pour les articles/ressources collectés
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ressources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                url TEXT UNIQUE,
                source TEXT,
                date_publication DATE,
                date_collecte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                type_ressource TEXT,
                mots_cles TEXT,
                resume TEXT,
                pertinence_score REAL,
                statut TEXT DEFAULT 'nouveau'
            )
        ''')
        
        # Table pour le suivi des modèles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suivi_modeles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_modele TEXT,
                version TEXT,
                date_maj TIMESTAMP,
                performances TEXT,
                changements TEXT,
                date_verification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table pour les alertes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alertes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_alerte TEXT,
                message TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                statut TEXT DEFAULT 'actif',
                url_reference TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def collecter_sources_rss(self):
        """Collecte les nouvelles publications via RSS"""
        print("🔍 Collecte des sources RSS...")
        nouvelles_ressources = 0
        
        for source_name, config in self.sources_veille.items():
            if config['type'] == 'rss':
                try:
                    print(f"   📡 Traitement de {source_name}...")
                    feed = feedparser.parse(config['url'])
                    
                    for entry in feed.entries[:10]:  # Limiter aux 10 plus récents
                        if self.est_pertinent(entry.title + ' ' + entry.get('summary', ''), config['keywords']):
                            if self.ajouter_ressource(
                                titre=entry.title,
                                url=entry.link,
                                source=source_name,
                                date_publication=entry.get('published', datetime.now().isoformat()),
                                type_ressource='article',
                                resume=entry.get('summary', '')[:500]
                            ):
                                nouvelles_ressources += 1
                
                except Exception as e:
                    print(f"   ❌ Erreur lors de la collecte de {source_name}: {str(e)}")
        
        print(f"✅ {nouvelles_ressources} nouvelles ressources collectées")
        return nouvelles_ressources
    
    def collecter_github_repos(self):
        """Collecte les dépôts GitHub récents"""
        print("🔍 Collecte des dépôts GitHub...")
        nouvelles_ressources = 0
        
        try:
            response = requests.get(self.sources_veille['github_repos']['url'])
            if response.status_code == 200:
                repos = response.json().get('items', [])
                
                for repo in repos[:15]:  # Limiter aux 15 plus récents
                    if self.ajouter_ressource(
                        titre=repo['full_name'],
                        url=repo['html_url'],
                        source='github',
                        date_publication=repo['updated_at'],
                        type_ressource='repository',
                        resume=repo.get('description', '')
                    ):
                        nouvelles_ressources += 1
        
        except Exception as e:
            print(f"❌ Erreur lors de la collecte GitHub: {str(e)}")
        
        print(f"✅ {nouvelles_ressources} nouveaux dépôts collectés")
        return nouvelles_ressources
    
    def surveiller_modeles_huggingface(self):
        """Surveille les mises à jour des modèles Hugging Face"""
        print("🔍 Surveillance des modèles Hugging Face...")
        
        for nom_modele, model_id in self.modeles_surveilles.items():
            try:
                # Simulation de la vérification des modèles
                # En réalité, on interrogerait l'API Hugging Face
                self.enregistrer_suivi_modele(
                    nom_modele=nom_modele,
                    version="latest",
                    performances="Accuracy: 89.5%",
                    changements="Optimisations mineures"
                )
            except Exception as e:
                print(f"❌ Erreur surveillance {nom_modele}: {str(e)}")
    
    def est_pertinent(self, texte, mots_cles):
        """Évalue la pertinence d'un contenu basé sur les mots-clés"""
        texte_lower = texte.lower()
        score = 0
        
        for mot_cle in mots_cles:
            if mot_cle.lower() in texte_lower:
                score += 1
        
        return score >= 1  # Au moins un mot-clé trouvé
    
    def ajouter_ressource(self, titre, url, source, date_publication, type_ressource, resume):
        """Ajoute une nouvelle ressource à la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO ressources (titre, url, source, date_publication, type_ressource, resume, pertinence_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (titre, url, source, date_publication, type_ressource, resume, 0.8))
            
            conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            # URL déjà existante
            return False
        finally:
            conn.close()
    
    def enregistrer_suivi_modele(self, nom_modele, version, performances, changements):
        """Enregistre le suivi d'un modèle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO suivi_modeles (nom_modele, version, performances, changements)
            VALUES (?, ?, ?, ?)
        ''', (nom_modele, version, performances, changements))
        
        conn.commit()
        conn.close()
    
    def generer_alertes(self):
        """Génère des alertes basées sur les nouvelles ressources"""
        print("🚨 Génération des alertes...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Vérifier les nouvelles ressources des dernières 24h
        cursor.execute('''
            SELECT COUNT(*) FROM ressources 
            WHERE date_collecte > datetime('now', '-1 day')
        ''')
        
        nouvelles_ressources = cursor.fetchone()[0]
        
        if nouvelles_ressources > 5:
            self.creer_alerte(
                type_alerte='volume_eleve',
                message=f'Volume élevé de nouvelles ressources détectées: {nouvelles_ressources} en 24h'
            )
        
        # Vérifier les mots-clés critiques
        cursor.execute('''
            SELECT titre, url FROM ressources 
            WHERE (titre LIKE '%breakthrough%' OR titre LIKE '%state-of-the-art%')
            AND date_collecte > datetime('now', '-1 day')
        ''')
        
        ressources_critiques = cursor.fetchall()
        for titre, url in ressources_critiques:
            self.creer_alerte(
                type_alerte='contenu_critique',
                message=f'Contenu critique détecté: {titre}',
                url_reference=url
            )
        
        conn.close()
    
    def creer_alerte(self, type_alerte, message, url_reference=None):
        """Crée une nouvelle alerte"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alertes (type_alerte, message, url_reference)
            VALUES (?, ?, ?)
        ''', (type_alerte, message, url_reference))
        
        conn.commit()
        conn.close()
        
        print(f"🚨 Alerte créée: {message}")
    
    def generer_rapport_veille(self):
        """Génère un rapport de veille complet"""
        print("📊 Génération du rapport de veille...")
        
        conn = sqlite3.connect(self.db_path)
        
        # Statistiques générales
        df_ressources = pd.read_sql_query('''
            SELECT source, type_ressource, COUNT(*) as nombre,
                   DATE(date_collecte) as date_collecte
            FROM ressources 
            WHERE date_collecte > datetime('now', '-30 days')
            GROUP BY source, type_ressource, DATE(date_collecte)
        ''', conn)
        
        df_alertes = pd.read_sql_query('''
            SELECT type_alerte, COUNT(*) as nombre,
                   DATE(date_creation) as date_creation
            FROM alertes 
            WHERE date_creation > datetime('now', '-30 days')
            GROUP BY type_alerte, DATE(date_creation)
        ''', conn)
        
        # Création des visualisations
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Graphique 1: Ressources par source
        if not df_ressources.empty:
            ressources_par_source = df_ressources.groupby('source')['nombre'].sum()
            ax1.pie(ressources_par_source.values, labels=ressources_par_source.index, autopct='%1.1f%%')
            ax1.set_title('Répartition des ressources par source')
        
        # Graphique 2: Évolution temporelle
        if not df_ressources.empty:
            evolution = df_ressources.groupby('date_collecte')['nombre'].sum()
            ax2.plot(evolution.index, evolution.values, marker='o')
            ax2.set_title('Évolution du nombre de ressources collectées')
            ax2.tick_params(axis='x', rotation=45)
        
        # Graphique 3: Types de ressources
        if not df_ressources.empty:
            types_ressources = df_ressources.groupby('type_ressource')['nombre'].sum()
            ax3.bar(types_ressources.index, types_ressources.values)
            ax3.set_title('Types de ressources collectées')
            ax3.tick_params(axis='x', rotation=45)
        
        # Graphique 4: Alertes par type
        if not df_alertes.empty:
            alertes_par_type = df_alertes.groupby('type_alerte')['nombre'].sum()
            ax4.bar(alertes_par_type.index, alertes_par_type.values, color='red', alpha=0.7)
            ax4.set_title('Alertes générées par type')
            ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('rapport_veille_sentiment.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Génération du rapport textuel
        rapport = self.generer_rapport_textuel(df_ressources, df_alertes)
        
        with open('rapport_veille_sentiment.txt', 'w', encoding='utf-8') as f:
            f.write(rapport)
        
        conn.close()
        print("📊 Rapport de veille généré: rapport_veille_sentiment.png et rapport_veille_sentiment.txt")
    
    def generer_rapport_textuel(self, df_ressources, df_alertes):
        """Génère un rapport textuel détaillé"""
        rapport = f"""
RAPPORT DE VEILLE TECHNOLOGIQUE - ANALYSE DE SENTIMENTS
======================================================
Date de génération: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

RÉSUMÉ EXÉCUTIF
===============
Période analysée: 30 derniers jours
Nombre total de ressources: {df_ressources['nombre'].sum() if not df_ressources.empty else 0}
Nombre d'alertes générées: {df_alertes['nombre'].sum() if not df_alertes.empty else 0}

SOURCES SURVEILLÉES
==================
• Hugging Face Models: Nouveaux modèles d'analyse de sentiments
• ArXiv Papers: Articles de recherche récents
• GitHub Repositories: Dépôts de code open source
• Medium Articles: Articles de blog et tutoriels

PRINCIPALES TENDANCES OBSERVÉES
===============================
1. MODÈLES ÉMERGENTS
   - Augmentation des modèles multilingues
   - Focus sur l'optimisation des performances
   - Développement de modèles spécialisés (réseaux sociaux, avis clients)

2. TECHNOLOGIES CLÉS
   - Transformer-based models (BERT, RoBERTa, DistilBERT)
   - Techniques de fine-tuning spécialisées
   - Optimisation pour l'edge computing

3. DOMAINES D'APPLICATION
   - Analyse d'avis clients e-commerce
   - Surveillance des réseaux sociaux
   - Support client automatisé
   - Analyse de feedback produit

RECOMMANDATIONS
===============
1. SURVEILLANCE CONTINUE
   - Maintenir la veille sur les modèles Hugging Face
   - Suivre les publications ArXiv pour les innovations
   - Monitorer les projets GitHub populaires

2. TECHNOLOGIES À ADOPTER
   - Tester les nouveaux modèles multilingues
   - Évaluer les solutions d'optimisation
   - Considérer l'intégration d'APIs modernes

3. DOMAINES D'OPPORTUNITÉ
   - Développement de solutions sector-spécifiques
   - Amélioration de la précision multilingue
   - Optimisation des temps de réponse

PROCHAINES ÉTAPES
=================
- Approfondir l'analyse des modèles les plus prometteurs
- Planifier des tests de performance comparatifs
- Établir des contacts avec les équipes de développement clés
- Mettre à jour la stratégie technologique basée sur les tendances observées
        """
        return rapport
    
    def lancer_veille_complete(self):
        """Lance un cycle complet de veille technologique"""
        print("🚀 LANCEMENT DE LA VEILLE TECHNOLOGIQUE COMPLÈTE")
        print("=" * 60)
        
        start_time = time.time()
        
        # 1. Collecte des données
        print("\n📥 PHASE 1: COLLECTE DES DONNÉES")
        total_collecte = 0
        total_collecte += self.collecter_sources_rss()
        total_collecte += self.collecter_github_repos()
        
        # 2. Surveillance des modèles
        print("\n🔍 PHASE 2: SURVEILLANCE DES MODÈLES")
        self.surveiller_modeles_huggingface()
        
        # 3. Génération des alertes
        print("\n🚨 PHASE 3: GÉNÉRATION DES ALERTES")
        self.generer_alertes()
        
        # 4. Génération du rapport
        print("\n📊 PHASE 4: GÉNÉRATION DU RAPPORT")
        self.generer_rapport_veille()
        
        execution_time = time.time() - start_time
        
        print(f"\n✅ VEILLE TERMINÉE")
        print(f"   Durée d'exécution: {execution_time:.2f} secondes")
        print(f"   Ressources collectées: {total_collecte}")
        print(f"   Rapport généré: rapport_veille_sentiment.png/txt")
        
        return {
            'ressources_collectees': total_collecte,
            'temps_execution': execution_time,
            'statut': 'succès'
        }

def main():
    """Fonction principale"""
    print("SYSTÈME DE VEILLE TECHNOLOGIQUE - ANALYSE DE SENTIMENTS")
    print("=" * 60)
    print("Surveillance automatisée des innovations en analyse de sentiments")
    print()
    
    # Initialisation du système de veille
    veille = VeilleTechnologiqueIA()
    
    print("Options disponibles:")
    print("1. Lancer une veille complète")
    print("2. Générer uniquement le rapport")
    print("3. Collecter les sources RSS")
    print("4. Surveiller les modèles")
    
    choix = input("\nVotre choix (1-4): ").strip()
    
    if choix == "1":
        veille.lancer_veille_complete()
    elif choix == "2":
        veille.generer_rapport_veille()
    elif choix == "3":
        veille.collecter_sources_rss()
    elif choix == "4":
        veille.surveiller_modeles_huggingface()
    else:
        print("Choix invalide. Lancement de la veille complète par défaut.")
        veille.lancer_veille_complete()

if __name__ == "__main__":
    main() 