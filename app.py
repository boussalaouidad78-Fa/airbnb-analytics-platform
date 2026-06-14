import streamlit as st
import duckdb
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Airbnb Analytics", layout="wide", initial_sidebar_state="expanded")

# 2. Injection de CSS avancé pour un rendu "Premium"
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    /* Style des cartes de KPI (Indicateurs) */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    /* Typographie et couleurs de la marque */
    h1 { color: #FF5A5F !important; font-weight: 700; }
    h2, h3 { color: #2D3748 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Barre latérale avec Logo
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_B%C3%A9lo.svg", width=120)
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Contexte**\n\nPlateforme d'analyse des données Airbnb (Pipeline de la couche Bronze ➔ Gold).")
    st.markdown("---")
    st.markdown("**Gouvernance des données :**")
    st.markdown("- **Data Engineering :** Ouidad")
    st.markdown("- **Front-end & BI :** Vous")

st.title("📊 Dashboard Airbnb Analytics")
st.markdown("Vision globale de l'activité du parc immobilier, des performances hôtes et des retours voyageurs.")
st.markdown("---")

# 4. Connexion sécurisée
@st.cache_resource
def get_connection():
    return duckdb.connect('airbnb_analytics/airbnb.duckdb', read_only=True)

con = get_connection()

# 5. Onglets avec icônes
tab_logements, tab_hotes, tab_avis, tab_lune = st.tabs(["🛏️ Logements", "👤 Hôtes", "⭐ Avis", "🌕 Impact Lunaire"])

# --- ONGLET 1 : LOGEMENTS ---
with tab_logements:
    st.subheader("Analyse du parc immobilier")
    
    # On gère les valeurs nulles (COALESCE) pour éviter les trous
    query_listings = """
        SELECT 
            COALESCE(CAST(room_type AS VARCHAR), 'Non spécifié') as "Type de logement", 
            COUNT(listing_id) as "Volume",
            ROUND(AVG(TRY_CAST(price AS NUMERIC)), 2) as "Prix moyen (€)"
        FROM main_gold.dim_listings 
        GROUP BY 1
        ORDER BY "Volume" DESC
    """
    df_listings = con.execute(query_listings).df()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Volume total de logements", f"{df_listings['Volume'].sum():,} ".replace(",", " "))
    col2.metric("Prix moyen du marché", f"{df_listings['Prix moyen (€)'].mean():.2f} €")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_chart, col_data = st.columns([2, 1])
    
    with col_chart:
        st.bar_chart(data=df_listings.set_index("Type de logement")["Volume"])
        
    with col_data:
        st.dataframe(df_listings, use_container_width=True, hide_index=True)

# --- ONGLET 2 : HÔTES ---
with tab_hotes:
    st.subheader("Performances et statuts des hôtes")
    
    # Résolution des trous : on gère tous les formats possibles (t, true, True, 1) et les vides
    query_hosts = """
        SELECT 
            CASE 
                WHEN CAST(is_superhost AS VARCHAR) IN ('t', 'true', 'True', '1') THEN 'Superhost' 
                WHEN CAST(is_superhost AS VARCHAR) IN ('f', 'false', 'False', '0') THEN 'Classique'
                ELSE 'Non renseigné' 
            END as "Statut",
            COUNT(host_id) as "Total"
        FROM main_gold.dim_hosts 
        GROUP BY 1
        ORDER BY "Total" DESC
    """
    df_hosts = con.execute(query_hosts).df()
    
    col1, col2 = st.columns(2)
    total_hotes = df_hosts["Total"].sum()
    
    # Sécurisation du calcul du pourcentage si la table est vide
    superhosts_df = df_hosts[df_hosts['Statut'] == 'Superhost']
    superhosts_count = superhosts_df['Total'].sum() if not superhosts_df.empty else 0
    pourcentage_super = (superhosts_count / total_hotes * 100) if total_hotes > 0 else 0
    
    col1.metric("Communauté d'hôtes", f"{total_hotes:,}".replace(",", " "))
    col2.metric("Taux de Superhosts", f"{pourcentage_super:.1f} %")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.bar_chart(data=df_hosts.set_index("Statut"))

# --- ONGLET 3 : AVIS ---
with tab_avis:
    st.subheader("Analyse textuelle des retours clients")
    
    col_filtre, _ = st.columns([1, 2])
    with col_filtre:
        sentiment_filter = st.selectbox("Filtrage sémantique :", ["Tous", "positive", "neutral", "negative"])
    
    where_clause = "" if sentiment_filter == "Tous" else f"WHERE LOWER(CAST(sentiment AS VARCHAR)) = '{sentiment_filter}'"
    
    # Nettoyage de la casse (UPPER) et gestion des noms vides
    query_reviews = f"""
        SELECT 
            review_date as "Date", 
            COALESCE(reviewer_name, 'Anonyme') as "Voyageur", 
            UPPER(CAST(sentiment AS VARCHAR)) as "Sentiment", 
            review_text as "Commentaire" 
        FROM main_gold.fact_reviews 
        {where_clause}
        ORDER BY review_date DESC 
        LIMIT 100
    """
    df_reviews = con.execute(query_reviews).df()
    st.dataframe(df_reviews, use_container_width=True, hide_index=True)

# --- ONGLET 4 : PLEINE LUNE ---
with tab_lune:
    st.subheader("Étude comportementale : Impact lunaire")
    
    query_moon = """
        SELECT 
            COALESCE(CAST(is_full_moon AS VARCHAR), 'Inconnu') as "Période",
            UPPER(CAST(sentiment AS VARCHAR)) as "Sentiment",
            COUNT(*) as "Volume"
        FROM main_gold.full_moon_reviews
        WHERE sentiment IS NOT NULL
        GROUP BY 1, 2
    """
    df_moon = con.execute(query_moon).df()
    
    # Transformation des données pour le graphique
    if not df_moon.empty:
        df_pivot = df_moon.pivot(index="Période", columns="Sentiment", values="Volume").fillna(0)
        st.bar_chart(df_pivot)
    else:
        st.info("Aucune donnée disponible pour cette analyse.")