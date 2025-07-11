#!/usr/bin/env python3
"""
Benchmark d'analyse de sentiments - Veille technologique Hugging Face
Auteur: [Votre nom]
Date: [Date]

Ce script compare 3 modèles d'analyse de sentiments disponibles sur Hugging Face
pour l'analyse automatique d'avis clients et commentaires.
"""

import time
import requests
import json
from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class SentimentAnalyzer:
    """Classe pour analyser les sentiments avec différents modèles Hugging Face"""
    
    def __init__(self):
        self.models = {
            'distilbert-english': {
                'name': 'distilbert-base-uncased-finetuned-sst-2-english',
                'languages': ['en'],
                'description': 'Modèle DistilBERT optimisé pour l\'anglais',
                'expected_accuracy': '91.3%',
                'model_size_mb': 268,
                'api_endpoint': 'https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english'
            },
            'bert-multilingual': {
                'name': 'nlptown/bert-base-multilingual-uncased-sentiment',
                'languages': ['en', 'fr', 'de', 'es', 'it'],
                'description': 'Modèle BERT multilingue (5 étoiles)',
                'expected_accuracy': '85.2%',
                'model_size_mb': 438,
                'api_endpoint': 'https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment'
            },
            'roberta-twitter': {
                'name': 'cardiffnlp/twitter-roberta-base-sentiment',
                'languages': ['en'],
                'description': 'RoBERTa optimisé pour Twitter',
                'expected_accuracy': '89.1%',
                'model_size_mb': 499,
                'api_endpoint': 'https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment'
            }
        }
        
        self.test_samples = {
            'en': [
                "This product is absolutely amazing! I love it!",
                "The service was terrible and the staff was rude.",
                "It's okay, nothing special but works fine.",
                "Best purchase I've ever made, highly recommended!",
                "Disappointed with the quality, waste of money."
            ],
            'fr': [
                "Ce produit est absolument génial ! Je l'adore !",
                "Le service était terrible et le personnel était impoli.",
                "C'est correct, rien de spécial mais ça fonctionne bien.",
                "Meilleur achat que j'ai jamais fait, fortement recommandé !",
                "Déçu de la qualité, gaspillage d'argent."
            ]
        }
        
        self.results = {}
    
    def test_local_model(self, model_key: str) -> Dict:
        """Teste un modèle en local avec Transformers"""
        print(f"🔧 Test du modèle local: {model_key}")
        
        model_info = self.models[model_key]
        results = {
            'model': model_key,
            'type': 'local',
            'responses': [],
            'response_times': [],
            'errors': []
        }
        
        try:
            # Chargement du modèle
            start_time = time.time()
            
            if model_key == 'bert-multilingual':
                # Modèle 5 étoiles - conversion spéciale
                classifier = pipeline('text-classification', model=model_info['name'])
                
                for lang, samples in self.test_samples.items():
                    if lang in model_info['languages']:
                        for sample in samples:
                            start = time.time()
                            try:
                                result = classifier(sample)
                                response_time = time.time() - start
                                
                                # Conversion du format 5 étoiles vers sentiment
                                label = result[0]['label']
                                score = result[0]['score']
                                
                                # Conversion: 1-2 étoiles = négatif, 3 = neutre, 4-5 = positif
                                if '1 star' in label or '2 stars' in label:
                                    sentiment = 'NEGATIVE'
                                elif '3 stars' in label:
                                    sentiment = 'NEUTRAL'
                                else:
                                    sentiment = 'POSITIVE'
                                
                                results['responses'].append({
                                    'text': sample,
                                    'language': lang,
                                    'sentiment': sentiment,
                                    'confidence': score,
                                    'original_label': label
                                })
                                results['response_times'].append(response_time)
                                
                            except Exception as e:
                                results['errors'].append(f"Erreur sur '{sample}': {str(e)}")
                                
            else:
                # Modèles binaires (positif/négatif)
                classifier = pipeline('sentiment-analysis', model=model_info['name'])
                
                for lang, samples in self.test_samples.items():
                    if lang in model_info['languages']:
                        for sample in samples:
                            start = time.time()
                            try:
                                result = classifier(sample)
                                response_time = time.time() - start
                                
                                results['responses'].append({
                                    'text': sample,
                                    'language': lang,
                                    'sentiment': result[0]['label'].upper(),
                                    'confidence': result[0]['score'],
                                    'original_label': result[0]['label']
                                })
                                results['response_times'].append(response_time)
                                
                            except Exception as e:
                                results['errors'].append(f"Erreur sur '{sample}': {str(e)}")
            
            load_time = time.time() - start_time
            results['load_time'] = load_time
            
        except Exception as e:
            results['errors'].append(f"Erreur de chargement: {str(e)}")
        
        return results
    
    def test_api_model(self, model_key: str) -> Dict:
        """Teste un modèle via l'API Hugging Face"""
        print(f"Test de l'API: {model_key}")
        
        model_info = self.models[model_key]
        results = {
            'model': model_key,
            'type': 'api',
            'responses': [],
            'response_times': [],
            'errors': []
        }
        
        for lang, samples in self.test_samples.items():
            if lang in model_info['languages']:
                for sample in samples:
                    start = time.time()
                    try:
                        response = requests.post(
                            model_info['api_endpoint'],
                            headers={"Content-Type": "application/json"},
                            json={"inputs": sample}
                        )
                        response_time = time.time() - start
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            if model_key == 'bert-multilingual':
                                # Traitement spécial pour le modèle 5 étoiles
                                label = result[0][0]['label']
                                score = result[0][0]['score']
                                
                                if '1 star' in label or '2 stars' in label:
                                    sentiment = 'NEGATIVE'
                                elif '3 stars' in label:
                                    sentiment = 'NEUTRAL'
                                else:
                                    sentiment = 'POSITIVE'
                            else:
                                label = result[0]['label']
                                score = result[0]['score']
                                sentiment = label.upper()
                            
                            results['responses'].append({
                                'text': sample,
                                'language': lang,
                                'sentiment': sentiment,
                                'confidence': score,
                                'original_label': label
                            })
                            results['response_times'].append(response_time)
                        else:
                            results['errors'].append(f"Erreur API {response.status_code}: {response.text}")
                            
                    except Exception as e:
                        results['errors'].append(f"Erreur sur '{sample}': {str(e)}")
        
        return results
    
    def run_benchmark(self, use_api: bool = False) -> Dict:
        """Lance le benchmark complet"""
        print("🚀 Démarrage du benchmark d'analyse de sentiments")
        print("=" * 60)
        
        all_results = {}
        
        for model_key in self.models.keys():
            print(f"\n📊 Test du modèle: {model_key}")
            print("-" * 40)
            
            if use_api:
                result = self.test_api_model(model_key)
            else:
                result = self.test_local_model(model_key)
            
            all_results[model_key] = result
            
            # Affichage des résultats
            if result['responses']:
                avg_time = sum(result['response_times']) / len(result['response_times'])
                print(f" Temps de réponse moyen: {avg_time:.3f}s")
                print(f"Nombre de tests réussis: {len(result['responses'])}")
                
                # Afficher quelques exemples
                for i, resp in enumerate(result['responses'][:3]):
                    print(f"   Exemple {i+1}: '{resp['text'][:50]}...' → {resp['sentiment']} ({resp['confidence']:.2f})")
            else:
                print("❌ Aucun test réussi")
            
            if result['errors']:
                print(f"Erreurs: {len(result['errors'])}")
                for error in result['errors'][:2]:  # Afficher seulement les 2 premières erreurs
                    print(f"   - {error}")
        
        self.results = all_results
        return all_results
    
    def generate_comparison_table(self) -> pd.DataFrame:
        """Génère un tableau comparatif des modèles"""
        comparison_data = []
        
        for model_key, model_info in self.models.items():
            result = self.results.get(model_key, {})
            
            avg_time = 0
            success_rate = 0
            if result.get('responses'):
                avg_time = sum(result['response_times']) / len(result['response_times'])
                success_rate = len(result['responses']) / (len(result['responses']) + len(result.get('errors', []))) * 100
            
            comparison_data.append({
                'Modèle': model_key,
                'Description': model_info['description'],
                'Langues': ', '.join(model_info['languages']),
                'Précision attendue': model_info['expected_accuracy'],
                'Taille (MB)': model_info['model_size_mb'],
                'Temps moyen (s)': f"{avg_time:.3f}",
                'Taux de succès (%)': f"{success_rate:.1f}",
                'Type de test': result.get('type', 'N/A'),
                'Erreurs': len(result.get('errors', []))
            })
        
        return pd.DataFrame(comparison_data)
    
    def plot_results(self):
        """Génère des graphiques de comparaison"""
        if not self.results:
            print("Aucun résultat à afficher")
            return
        
        # Préparation des données pour les graphiques
        models = []
        avg_times = []
        success_rates = []
        
        for model_key, result in self.results.items():
            if result.get('responses'):
                avg_time = sum(result['response_times']) / len(result['response_times'])
                success_rate = len(result['responses']) / (len(result['responses']) + len(result.get('errors', []))) * 100
                
                models.append(model_key)
                avg_times.append(avg_time)
                success_rates.append(success_rate)
        
        # Création des graphiques
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Graphique des temps de réponse
        bars1 = ax1.bar(models, avg_times, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        ax1.set_title('Temps de réponse moyen par modèle', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Temps (secondes)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Ajout des valeurs sur les barres
        for bar, time_val in zip(bars1, avg_times):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001, 
                    f'{time_val:.3f}s', ha='center', va='bottom')
        
        # Graphique des taux de succès
        bars2 = ax2.bar(models, success_rates, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        ax2.set_title('Taux de succès par modèle', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Taux de succès (%)')
        ax2.tick_params(axis='x', rotation=45)
        
        # Ajout des valeurs sur les barres
        for bar, rate in zip(bars2, success_rates):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{rate:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('benchmark_results.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("📊 Graphiques sauvegardés dans 'benchmark_results.png'")
    
    def save_detailed_results(self, filename: str = 'detailed_results.json'):
        """Sauvegarde les résultats détaillés en JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"Résultats détaillés sauvegardés dans '{filename}'")

def main():
    """Fonction principale"""
    print("BENCHMARK D'ANALYSE DE SENTIMENTS - HUGGING FACE")
    print("=" * 60)
    print("Ce script compare 3 modèles d'analyse de sentiments:")
    print("1. DistilBERT (anglais)")
    print("2. BERT multilingue (5 étoiles)")
    print("3. RoBERTa Twitter (anglais)")
    print()
    
    # Initialisation de l'analyseur
    analyzer = SentimentAnalyzer()
    
    # Choix du mode de test
    print("Choisissez le mode de test:")
    print("1. Test local (recommandé pour la première fois)")
    print("2. Test API (gratuit, 30 requêtes/jour)")
    
    choice = input("Votre choix (1 ou 2): ").strip()
    use_api = choice == "2"
    
    if use_api:
        print("\nMode API sélectionné - Limite de 30 requêtes/jour")
        print("   Les tests peuvent échouer si la limite est atteinte")
    
    # Lancement du benchmark
    results = analyzer.run_benchmark(use_api=use_api)
    
    # Génération du tableau comparatif
    print("\n" + "=" * 60)
    print("TABLEAU COMPARATIF")
    print("=" * 60)
    
    comparison_df = analyzer.generate_comparison_table()
    print(comparison_df.to_string(index=False))
    
    # Sauvegarde des résultats
    analyzer.save_detailed_results()
    
    # Génération des graphiques
    print("\n Génération des graphiques...")
    analyzer.plot_results()
    
    # Affichage des recommandations
    print("\n" + "=" * 60)
    print("💡 RECOMMANDATIONS")
    print("=" * 60)
    
    best_time = float('inf')
    best_model = None
    
    for model_key, result in results.items():
        if result.get('responses'):
            avg_time = sum(result['response_times']) / len(result['response_times'])
            if avg_time < best_time:
                best_time = avg_time
                best_model = model_key
    
    if best_model:
        print(f"🏆 Modèle le plus rapide: {best_model} ({best_time:.3f}s)")
    
    print("\nRecommandations d'usage:")
    print("- Pour l'anglais uniquement: DistilBERT (rapide et précis)")
    print("- Pour le multilingue: BERT multilingue (5 étoiles)")
    print("- Pour les réseaux sociaux: RoBERTa Twitter")
    print("- Pour la production: Testez d'abord en local, puis API")

if __name__ == "__main__":
    main() 