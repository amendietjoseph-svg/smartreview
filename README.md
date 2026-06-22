# SmartReview - Journal de Trading Intelligent avec IA

SmartReview est une application web complète de journal de trading avec analyse de performance propulsée par l'IA. Elle permet aux traders de suivre leurs trades, d'analyser leurs statistiques, et d'obtenir des recommandations personnalisées pour améliorer leur performance.

## 🚀 Fonctionnalités

- **Dashboard complet** avec KPIs en temps réel (profit, win rate, drawdown, etc.)
- **Journal de trading détaillé** avec capture de setup, psychologie et gestion du risque
- **Calendrier de performance** pour visualiser les résultats jour par jour
- **Statistiques visuelles** avec graphiques interactifs (ApexCharts)
- **IA Coach** pour obtenir des insights et recommandations personnalisées
- **Gestion multi-comptes** (comptes personnels et prop firms)
- **Trading Score™** pour évaluer la discipline et le respect du plan
- **Design premium sombre** inspiré des fintech modernes

## 🛠 Stack Technique

### Backend
- **FastAPI** - Framework API Python moderne et rapide
- **SQLAlchemy** - ORM pour la base de données
- **SQLite** - Base de données légère et portable
- **Pydantic** - Validation des données
- **httpx** - Client HTTP asynchrone pour l'API Claude

### Frontend
- **HTML5, CSS3, JavaScript Vanilla** - Pas de framework pour l'instant
- **ApexCharts** - Bibliothèque de graphiques interactifs
- **Lucide Icons** - Icônes modernes et légères
- **Inter (Google Fonts)** - Typographie professionnelle

## 📁 Structure du Projet

```
smartreview/
├── backend/
│   ├── main.py                 # Point d'entrée FastAPI
│   ├── database.py             # Configuration de la base de données
│   ├── models.py               # Modèles SQLAlchemy
│   ├── schemas.py              # Schémas Pydantic
│   ├── requirements.txt        # Dépendances Python
│   ├── routers/
│   │   ├── trades.py          # Endpoints pour les trades
│   │   ├── stats.py           # Endpoints pour les statistiques
│   │   ├── accounts.py        # Endpoints pour les comptes
│   │   └── ai_coach.py        # Endpoints pour l'IA Coach
│   └── services/
│       ├── stats_calculator.py # Calculateur de statistiques
│       └── ai_service.py       # Service IA (Claude)
├── frontend/
│   ├── index.html              # Dashboard principal
│   ├── journal.html            # Journal de trading
│   ├── calendar.html           # Calendrier de performance
│   ├── stats.html              # Statistiques visuelles
│   ├── coach.html              # IA Coach
│   ├── accounts.html           # Gestion des comptes
│   ├── css/
│   │   ├── global.css          # Styles globaux
│   │   ├── dashboard.css       # Styles du dashboard
│   │   └── components.css      # Styles des composants
│   └── js/
│       ├── api.js              # Client API
│       ├── dashboard.js        # Logique du dashboard
│       ├── journal.js          # Logique du journal
│       ├── charts.js           # Utilitaires de graphiques
│       └── utils.js            # Fonctions utilitaires
└── README.md                   # Ce fichier
```

## 📦 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Un navigateur web moderne

### Étape 1 : Cloner le projet

```bash
cd "c:/Users/amend/OneDrive/Desktop/Smart REVIEW"
```

### Étape 2 : Installer les dépendances backend

```bash
cd backend
pip install -r requirements.txt
```

### Étape 3 : Lancer le serveur backend

```bash
uvicorn main:app --reload --port 8001
```

Le serveur démarrera sur `http://localhost:8001`

### Étape 4 : Ouvrir le frontend

Ouvrez simplement le fichier `frontend/index.html` dans votre navigateur web, ou utilisez un serveur HTTP local :

```bash
# Avec Python 3
cd ../frontend
python -m http.server 3000
```

Puis accédez à `http://localhost:3000`

## 🎯 Utilisation

### 1. Créer un compte

1. Allez dans la page **Comptes**
2. Cliquez sur **Nouveau Compte**
3. Remplissez les informations (nom, type, broker, solde initial)
4. Cliquez sur **Enregistrer**

### 2. Enregistrer un trade

1. Allez dans la page **Journal** ou cliquez sur **Nouveau Trade** dans le dashboard
2. Remplissez les informations du trade :
   - Informations de base (actif, direction, prix d'entrée)
   - Gestion du risque (stop loss, take profit, lot size)
   - Setup et contexte de marché
   - Psychologie et discipline
   - Détails temporels
3. Cliquez sur **Enregistrer**

### 3. Voir les statistiques

Le dashboard affiche automatiquement :
- **Performance** : Profit total, profit du jour/mois/année, solde actuel
- **Statistiques** : Win rate, profit factor, RR moyen, espérance, drawdown
- **Discipline** : Trading Score™, respect du plan, respect du risque
- **Courbe d'équité** : Évolution du capital dans le temps
- **Trades récents** : Les 10 derniers trades

### 4. Analyser avec l'IA Coach

1. Allez dans la page **IA Coach**
2. Sélectionnez un compte actif
3. Cliquez sur **Analyser**
4. L'IA vous fournira :
   - Insights sur votre performance
   - Forces à exploiter
   - Points à améliorer
   - Recommandations personnalisées
   - Edge tracker (meilleurs setups, sessions, actifs)

## 🎨 Design System

L'application utilise un thème sombre premium fintech avec les couleurs suivantes :

- **Background primaire** : `#0A0B0F`
- **Background secondaire** : `#111318`
- **Background carte** : `#161920`
- **Accent vert** : `#00D26A`
- **Accent rouge** : `#FF4757`
- **Accent bleu** : `#3B82F6`
- **Accent violet** : `#8B5CF6`
- **Accent or** : `#F59E0B`
- **Texte primaire** : `#F1F5F9`
- **Texte secondaire** : `#8B9AB1`

## 🔧 Configuration de l'IA (Optionnel)

Pour utiliser l'analyse IA complète avec Claude :

1. Créez un compte sur [Anthropic](https://www.anthropic.com/)
2. Obtenez votre clé API
3. Ajoutez la clé API dans `backend/services/ai_service.py` :

```python
self.api_key = "votre_clé_api_ici"
```

Sans clé API, l'application utilisera une analyse basée sur des règles qui fournit toujours des insights utiles.

## 📊 Modèle de Données

### Trade
- Informations de base (actif, direction, prix)
- Gestion du risque (SL, TP, lot size, RR)
- Setup et contexte de marché
- Psychologie (confiance, état émotionnel, discipline)
- Timing (session, dates)
- Screenshots et notes
- Trading Score™ calculé automatiquement

### Account
- Type (Personnel / Prop Firm)
- Informations broker
- Solde initial et actuel
- Limites de drawdown (pour prop firms)
- Objectifs de profit
- Phase du challenge

## 🔄 API Endpoints

### Trades
- `GET /api/trades/` - Liste des trades
- `POST /api/trades/` - Créer un trade
- `GET /api/trades/{id}` - Détails d'un trade
- `PUT /api/trades/{id}` - Modifier un trade
- `DELETE /api/trades/{id}` - Supprimer un trade

### Statistiques
- `GET /api/stats/account/{account_id}` - Statistiques d'un compte
- `GET /api/stats/equity/{account_id}` - Courbe d'équité
- `GET /api/stats/performance/{account_id}` - Métriques de performance

### Comptes
- `GET /api/accounts/` - Liste des comptes
- `POST /api/accounts/` - Créer un compte
- `GET /api/accounts/{id}` - Détails d'un compte
- `PUT /api/accounts/{id}` - Modifier un compte
- `DELETE /api/accounts/{id}` - Supprimer un compte

### IA Coach
- `POST /api/ai/analyze` - Analyser la performance
- `GET /api/ai/edge/{account_id}` - Edge tracker

## 🐛 Dépannage

### Le backend ne démarre pas
- Vérifiez que le port 8001 n'est pas déjà utilisé
- Vérifiez que toutes les dépendances sont installées
- Consultez les logs dans le terminal

### Le frontend ne se connecte pas au backend
- Vérifiez que le backend est en cours d'exécution
- Vérifiez que l'URL dans `frontend/js/api.js` est correcte
- Consultez la console du navigateur pour les erreurs

### Les données ne s'affichent pas
- Assurez-vous d'avoir créé un compte
- Sélectionnez un compte actif dans le sidebar
- Vérifiez que vous avez enregistré des trades

## 🚀 Améliorations Futures

- [ ] Authentification des utilisateurs
- [ ] Export des données en CSV/Excel
- [ ] Graphiques supplémentaires
- [ ] Mode sombre/clair
- [ ] Notifications push
- [ ] Application mobile
- [ ] Intégration avec des brokers
- [ ] Backtesting de stratégies

## 📝 Licence

Ce projet est fourni à titre éducatif. Vous êtes libre de l'utiliser et de le modifier selon vos besoins.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou un pull request.

## 📧 Support

Pour toute question ou problème, n'hésitez pas à ouvrir une issue sur le projet.

---

**Bon trading ! 📈**
