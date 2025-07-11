#!/usr/bin/env python3
"""
Script de test simple pour vérifier le fonctionnement des modèles
Utile pour un test rapide avant le benchmark complet
"""

from transformers import pipeline
import time

def test_simple():
    """Test simple avec un modèle pour vérifier l'installation"""
    
    print("🧪 TEST SIMPLE - Vérification de l'installation")
    print("=" * 50)
    
    # Test avec DistilBERT (le plus léger)
    print("📥 Téléchargement du modèle DistilBERT...")
    
    try:
        # Création du pipeline
        classifier = pipeline('sentiment-analysis', 
                            model='distilbert-base-uncased-finetuned-sst-2-english')
        
        print("✅ Modèle chargé avec succès!")
        
        # Test avec quelques phrases
        test_phrases = [
            "I love this product!",
            "This is terrible.",
            "It's okay, nothing special."
        ]
        
        print("\n🔍 Test d'analyse de sentiments:")
        print("-" * 30)
        
        for phrase in test_phrases:
            start_time = time.time()
            result = classifier(phrase)
            response_time = time.time() - start_time
            
            sentiment = result[0]['label'].upper()
            confidence = result[0]['score']
            
            print(f"📝 '{phrase}'")
            print(f"   → {sentiment} ({confidence:.2f}) en {response_time:.3f}s")
            print()
        
        print("🎉 Test réussi! L'installation fonctionne correctement.")
        print("\n💡 Vous pouvez maintenant lancer le benchmark complet:")
        print("   python sentiment_analysis_benchmark.py")
        
    except Exception as e:
        print(f" Erreur lors du test: {str(e)}")
        print("\n Solutions possibles:")
        print("1. Vérifiez votre connexion internet")
        print("2. Installez les dépendances: pip install -r requirements.txt")
        print("3. Vérifiez que vous avez suffisamment d'espace disque")

if __name__ == "__main__":
    test_simple() 