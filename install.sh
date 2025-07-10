#!/bin/bash

# Script d'installation automatique pour le projet de veille technologique
# Analyse de Sentiments avec Hugging Face

echo "🎯 Installation du projet de veille technologique"
echo "=================================================="

# Vérification de Python
echo "🔍 Vérification de Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python $PYTHON_VERSION détecté"
else
    echo "❌ Python 3 n'est pas installé"
    echo "📥 Installation de Python 3..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update
        sudo apt install -y python3 python3-pip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python3
    else
        echo "❌ Système d'exploitation non supporté"
        exit 1
    fi
fi

# Vérification de pip
echo "🔍 Vérification de pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 détecté"
else
    echo "❌ pip3 n'est pas installé"
    echo "📥 Installation de pip3..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt install -y python3-pip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python3
    fi
fi

# Création d'un environnement virtuel (optionnel)
echo "🔍 Vérification de l'environnement virtuel..."
if command -v python3 -m venv &> /dev/null; then
    echo "📁 Création d'un environnement virtuel..."
    python3 -m venv venv
    echo "✅ Environnement virtuel créé"
    echo "🔧 Activation de l'environnement virtuel..."
    source venv/bin/activate
    echo "✅ Environnement virtuel activé"
else
    echo "⚠️  Impossible de créer un environnement virtuel"
    echo "   Installation en mode global"
fi

# Installation des dépendances
echo "📦 Installation des dépendances..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dépendances installées avec succès"
else
    echo "❌ Erreur lors de l'installation des dépendances"
    echo "🔧 Tentative d'installation manuelle..."
    pip3 install transformers torch requests pandas matplotlib seaborn numpy
fi

# Test rapide
echo "🧪 Test rapide de l'installation..."
python3 test_simple.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Installation terminée avec succès!"
    echo ""
    echo "📋 Prochaines étapes:"
    echo "1. Lancer le benchmark complet: python3 sentiment_analysis_benchmark.py"
    echo "2. Consulter la documentation: cat README.md"
    echo "3. Voir la synthèse: cat synthese_veille.md"
    echo ""
    echo "💡 Pour désactiver l'environnement virtuel: deactivate"
else
    echo "❌ Erreur lors du test"
    echo "🔧 Vérifiez votre connexion internet et réessayez"
fi

echo ""
echo "📚 Documentation disponible:"
echo "- README.md : Guide complet d'utilisation"
echo "- synthese_veille.md : Synthèse de veille technologique"
echo "- tableau_comparatif.md : Comparaison détaillée des modèles" 