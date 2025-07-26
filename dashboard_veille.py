#!/usr/bin/env python3
"""
Tableau de Bord de Veille - Analyse de Sentiments
Interface web interactive pour visualiser les données de veille
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

class DashboardVeille:
    """Tableau de bord interactif pour la veille technologique"""
    
    def __init__(self, db_path='veille_sentiment.db'):
        self.db_path = db_path
        
    def load_data(self):
        """Charge les données depuis la base de données"""
        conn = sqlite3.connect(self.db_path)
        
        # Chargement des ressources
        df_ressources = pd.read_sql_query('''
            SELECT * FROM ressources 
            ORDER BY date_collecte DESC
        ''', conn)
        
        # Chargement des alertes
        df_alertes = pd.read_sql_query('''
            SELECT * FROM alertes 
            ORDER BY date_creation DESC
        ''', conn)
        
        # Chargement du suivi des modèles
        df_modeles = pd.read_sql_query('''
            SELECT * FROM suivi_modeles 
            ORDER BY date_verification DESC
        ''', conn)
        
        conn.close()
        return df_ressources, df_alertes, df_modeles
    
    def afficher_metriques_principales(self, df_ressources, df_alertes):
        """Affiche les métriques principales"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_ressources = len(df_ressources)
            st.metric("Ressources totales", total_ressources)
        
        with col2:
            nouvelles_24h = len(df_ressources[
                pd.to_datetime(df_ressources['date_collecte']) > 
                datetime.now() - timedelta(days=1)
            ])
            st.metric("Nouvelles (24h)", nouvelles_24h)
        
        with col3:
            alertes_actives = len(df_alertes[df_alertes['statut'] == 'actif'])
            st.metric("Alertes actives", alertes_actives)
        
        with col4:
            sources_uniques = df_ressources['source'].nunique()
            st.metric("Sources surveillées", sources_uniques)
    
    def graphique_evolution_temporelle(self, df_ressources):
        """Graphique d'évolution temporelle des ressources"""
        df_ressources['date'] = pd.to_datetime(df_ressources['date_collecte']).dt.date
        evolution = df_ressources.groupby('date').size().reset_index(name='count')
        
        fig = px.line(evolution, x='date', y='count', 
                     title='Évolution du nombre de ressources collectées',
                     markers=True)
        fig.update_layout(xaxis_title='Date', yaxis_title='Nombre de ressources')
        st.plotly_chart(fig, use_container_width=True)
    
    def graphique_repartition_sources(self, df_ressources):
        """Graphique de répartition par sources"""
        repartition = df_ressources['source'].value_counts()
        
        fig = px.pie(values=repartition.values, names=repartition.index,
                    title='Répartition des ressources par source')
        st.plotly_chart(fig, use_container_width=True)
    
    def tableau_alertes_recentes(self, df_alertes):
        """Tableau des alertes récentes"""
        st.subheader("🚨 Alertes récentes")
        
        if not df_alertes.empty:
            alertes_recentes = df_alertes.head(10)[['type_alerte', 'message', 'date_creation', 'statut']]
            st.dataframe(alertes_recentes, use_container_width=True)
        else:
            st.info("Aucune alerte récente")
    
    def tableau_ressources_pertinentes(self, df_ressources):
        """Tableau des ressources les plus pertinentes"""
        st.subheader("📚 Ressources les plus pertinentes")
        
        if not df_ressources.empty:
            # Filtrer et trier par pertinence
            ressources_top = df_ressources.nlargest(15, 'pertinence_score')[
                ['titre', 'source', 'type_ressource', 'date_publication', 'pertinence_score']
            ]
            st.dataframe(ressources_top, use_container_width=True)
        else:
            st.info("Aucune ressource disponible")
    
    def graphique_types_ressources(self, df_ressources):
        """Graphique des types de ressources"""
        types = df_ressources['type_ressource'].value_counts()
        
        fig = px.bar(x=types.index, y=types.values,
                    title='Types de ressources collectées',
                    labels={'x': 'Type', 'y': 'Nombre'})
        st.plotly_chart(fig, use_container_width=True)
    
    def afficher_recommandations(self):
        """Affiche les recommandations basées sur l'analyse"""
        st.subheader("💡 Recommandations")
        
        recommendations = [
            "🎯 **Surveillance continue**: Maintenir la veille sur les modèles Hugging Face populaires",
            "📊 **Analyse comparative**: Effectuer des benchmarks réguliers des nouveaux modèles",
            "🔍 **Focus multilingue**: Surveiller particulièrement les développements en analyse multilingue",
            "⚡ **Optimisation**: Suivre les innovations en optimisation de performance",
            "🌐 **APIs modernes**: Évaluer les nouvelles solutions d'API d'analyse de sentiments"
        ]
        
        for rec in recommendations:
            st.markdown(rec)
    
    def filtres_sidebar(self, df_ressources):
        """Barre latérale avec filtres"""
        st.sidebar.header("🔧 Filtres")
        
        # Filtre par source
        sources = ['Toutes'] + list(df_ressources['source'].unique())
        source_selectionnee = st.sidebar.selectbox("Source", sources)
        
        # Filtre par période
        periode = st.sidebar.selectbox("Période", [
            "7 derniers jours",
            "30 derniers jours", 
            "90 derniers jours",
            "Toute la période"
        ])
        
        # Filtre par type
        types = ['Tous'] + list(df_ressources['type_ressource'].unique())
        type_selectionne = st.sidebar.selectbox("Type de ressource", types)
        
        return source_selectionnee, periode, type_selectionne
    
    def appliquer_filtres(self, df, source, periode, type_ressource):
        """Applique les filtres sélectionnés"""
        df_filtre = df.copy()
        
        # Filtre par source
        if source != 'Toutes':
            df_filtre = df_filtre[df_filtre['source'] == source]
        
        # Filtre par période
        if periode != "Toute la période":
            jours = {'7 derniers jours': 7, '30 derniers jours': 30, '90 derniers jours': 90}
            date_limite = datetime.now() - timedelta(days=jours[periode])
            df_filtre = df_filtre[pd.to_datetime(df_filtre['date_collecte']) > date_limite]
        
        # Filtre par type
        if type_ressource != 'Tous':
            df_filtre = df_filtre[df_filtre['type_ressource'] == type_ressource]
        
        return df_filtre
    
    def run_dashboard(self):
        """Lance le tableau de bord principal"""
        st.set_page_config(
            page_title="Veille Technologique - Analyse de Sentiments",
            page_icon="🔍",
            layout="wide"
        )
        
        st.title("🔍 Tableau de Bord - Veille Technologique")
        st.markdown("### Analyse de Sentiments et IA")
        
        # Chargement des données
        try:
            df_ressources, df_alertes, df_modeles = self.load_data()
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {str(e)}")
            st.info("Lancez d'abord le script de veille pour collecter des données.")
            return
        
        if df_ressources.empty:
            st.warning("Aucune donnée disponible. Lancez d'abord la collecte de veille.")
            return
        
        # Filtres
        source_selectionnee, periode, type_selectionne = self.filtres_sidebar(df_ressources)
        df_ressources_filtre = self.appliquer_filtres(df_ressources, source_selectionnee, periode, type_selectionne)
        
        # Métriques principales
        self.afficher_metriques_principales(df_ressources_filtre, df_alertes)
        
        # Graphiques principaux
        col1, col2 = st.columns(2)
        
        with col1:
            self.graphique_evolution_temporelle(df_ressources_filtre)
        
        with col2:
            self.graphique_repartition_sources(df_ressources_filtre)
        
        # Deuxième ligne de graphiques
        col3, col4 = st.columns(2)
        
        with col3:
            self.graphique_types_ressources(df_ressources_filtre)
        
        with col4:
            self.tableau_alertes_recentes(df_alertes)
        
        # Tableau des ressources
        self.tableau_ressources_pertinentes(df_ressources_filtre)
        
        # Recommandations
        self.afficher_recommandations()
        
        # Section de téléchargement
        st.subheader("📥 Export des données")
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            if st.button("Télécharger les ressources (CSV)"):
                csv = df_ressources_filtre.to_csv(index=False)
                st.download_button(
                    label="Télécharger CSV",
                    data=csv,
                    file_name=f"ressources_veille_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col_export2:
            if st.button("Télécharger les alertes (JSON)"):
                json_data = df_alertes.to_json(orient='records', indent=2)
                st.download_button(
                    label="Télécharger JSON",
                    data=json_data,
                    file_name=f"alertes_veille_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

def main():
    """Fonction principale pour lancer le dashboard"""
    dashboard = DashboardVeille()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main() 