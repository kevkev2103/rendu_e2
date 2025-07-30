#!/usr/bin/env python3
"""
Script de démonstration - Analyse de sentiment avec Hugging Face
Compétence C8 : Paramétrage d'un service d'IA
"""

import os
import time
import logging
from typing import Dict, Any
from prometheus_client import Histogram, Counter, start_http_server, generate_latest
from transformers import pipeline
from dotenv import load_dotenv

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Chargement des variables d'environnement
load_dotenv()

# Métriques Prometheus
SENTIMENT_LATENCY = Histogram(
    'sentiment_analysis_duration_seconds',
    'Temps de traitement de l\'analyse de sentiment',
    buckets=[0.01, 0.05, 0.1, 0.15, 0.2, 0.5, 1.0, 2.0, 5.0]
)

SENTIMENT_ERRORS = Counter(
    'sentiment_analysis_errors_total',
    'Nombre total d\'erreurs dans l\'analyse de sentiment',
    ['error_type']
)

SENTIMENT_REQUESTS = Counter(
    'sentiment_analysis_requests_total',
    'Nombre total de requêtes d\'analyse de sentiment',
    ['sentiment_label']
)

class SentimentAnalyzer:
    """Classe pour l'analyse de sentiment avec instrumentation."""
    
    def __init__(self):
        """Initialise le pipeline de sentiment."""
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Charge le modèle d'analyse de sentiment multilingue."""
        try:
            logger.info("Chargement du modèle d'analyse de sentiment...")
            self.pipeline = pipeline(
                "sentiment-analysis",
                model="nlptown/bert-base-multilingual-uncased-sentiment",
                top_k=None
            )
            logger.info("Modèle chargé avec succès!")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {e}")
            SENTIMENT_ERRORS.labels(error_type="model_loading").inc()
            raise
    
    @SENTIMENT_LATENCY.time()
    def test_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyse le sentiment d'un texte donné.
        
        Args:
            text (str): Texte à analyser
            
        Returns:
            Dict[str, Any]: Résultats de l'analyse avec métriques
        """
        start_time = time.time()
        
        try:
            logger.info(f"Analyse du sentiment pour: '{text[:50]}...'")
            
            # Appel au pipeline
            results = self.pipeline(text)
            
            # Traitement des résultats
            best_result = max(results[0], key=lambda x: x['score'])
            
            # Métriques
            processing_time = time.time() - start_time
            SENTIMENT_REQUESTS.labels(sentiment_label=best_result['label']).inc()
            
            result = {
                'text': text,
                'sentiment': best_result['label'],
                'confidence': round(best_result['score'], 4),
                'all_scores': results[0],
                'processing_time': round(processing_time, 4)
            }
            
            # Affichage des résultats
            print(f"\n{'='*60}")
            print(f"TEXTE: {text}")
            print(f"SENTIMENT: {result['sentiment']}")
            print(f"CONFIANCE: {result['confidence']:.2%}")
            print(f"TEMPS DE TRAITEMENT: {result['processing_time']:.4f}s")
            print(f"DÉTAILS:")
            for score in result['all_scores']:
                print(f"  - {score['label']}: {score['score']:.4f}")
            print(f"{'='*60}")
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse: {e}")
            SENTIMENT_ERRORS.labels(error_type="analysis_error").inc()
            return {
                'text': text,
                'error': str(e),
                'processing_time': time.time() - start_time
            }

def start_metrics_server(port: int = 8000):
    """Démarre le serveur de métriques Prometheus."""
    try:
        start_http_server(port)
        logger.info(f"Serveur de métriques démarré sur le port {port}")
        logger.info(f"Métriques disponibles sur: http://localhost:{port}/metrics")
    except Exception as e:
        logger.error(f"Erreur lors du démarrage du serveur de métriques: {e}")
        SENTIMENT_ERRORS.labels(error_type="metrics_server").inc()

def main():
    """Fonction principale de démonstration."""
    print(" Démonstration - Analyse de Sentiment avec Hugging Face")
    print("Compétence C8 : Paramétrage d'un service d'IA")
    print("="*60)
    
    # Démarrage du serveur de métriques
    start_metrics_server()
    
    # Initialisation de l'analyseur
    analyzer = SentimentAnalyzer()
    
    # Exemples de tests
    test_texts = [
        "Ce produit est absolument fantastique! Je le recommande vivement.",  # Positif
        "Service client décevant, très lent et peu efficace.",  # Négatif
        "Le film était correct, sans plus.",  # Neutre
        "This product is amazing and works perfectly!",  # Anglais positif
        "Terrible experience, would not recommend.",  # Anglais négatif
    ]
    
    print(f"\n Exécution de {len(test_texts)} tests d'analyse de sentiment:")
    
    results = []
    for i, text in enumerate(test_texts, 1):
        print(f"\n[TEST {i}/{len(test_texts)}]")
        result = analyzer.test_sentiment(text)
        results.append(result)
        time.sleep(0.1)  # Pause pour éviter la surcharge
    
    # Résumé
    print(f"\n📈 RÉSUMÉ DES TESTS:")
    print(f"{'='*60}")
    successful_tests = [r for r in results if 'error' not in r]
    failed_tests = [r for r in results if 'error' in r]
    
    print(f"Tests réussis: {len(successful_tests)}/{len(results)}")
    print(f"Tests échoués: {len(failed_tests)}")
    
    if successful_tests:
        avg_time = sum(r['processing_time'] for r in successful_tests) / len(successful_tests)
        print(f"Temps moyen de traitement: {avg_time:.4f}s")
        
        sentiments = [r['sentiment'] for r in successful_tests]
        for sentiment in set(sentiments):
            count = sentiments.count(sentiment)
            print(f"Sentiment '{sentiment}': {count} occurence(s)")
    
    print(f"\n📊 Métriques Prometheus disponibles sur: http://localhost:8000/metrics")
    print("💡 Utilisez Ctrl+C pour arrêter le serveur de métriques")
    
    try:
        # Maintenir le serveur de métriques actif
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur de métriques")

if __name__ == "__main__":
    main() 