import pickle
import numpy as np
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# Initialisation de l'application
app = FastAPI(
    title="API Credit Scoring",
    description="API de prédiction de solvabilité client (MLP Optimisé)",
    version="1.0"
)

# Chargement du Pipeline entraîné
# On le charge une seule fois au démarrage pour gagner du temps
try:
    with open("credit_scoring_pipeline.pkl", "rb") as f:
        model = pickle.load(f)
    print(" Modèle chargé avec succès.")
except FileNotFoundError:
    print(" Erreur : Le fichier 'credit_scoring_pipeline.pkl' est introuvable.")

# Définition du format des données d'entrée (Schéma Pydantic)
# Doit correspondre exactement aux 13 colonnes initiales de votre X_train
class ClientData(BaseModel):
    Seniority: float
    Home: float
    Time: float
    Age: float
    Marital: float
    Records: float
    Job: float
    Expenses: float
    Income: float
    Assets: float
    Debt: float
    Amount: float
    Price: float

# Route de prédiction
@app.post("/predict")
def predict_credit(data: ClientData):
    """
    Reçoit les caractéristiques d'un client et renvoie la décision de crédit.
    """
    # Conversion des données reçues en liste ordonnée
    # L'ordre doit être STRICTEMENT le même que lors de l'entraînement (X_train)
    features = [
        data.Seniority, data.Home, data.Time, data.Age, data.Marital,
        data.Records, data.Job, data.Expenses, data.Income, data.Assets,
        data.Debt, data.Amount, data.Price
    ]
    
    # Transformation en tableau Numpy 2D (1 ligne, 13 colonnes)
    # Le pipeline s'attend à recevoir une matrice, pas une simple liste
    features_array = np.array(features).reshape(1, -1)
    
    # Prédiction via le Pipeline
    # Le pipeline gère tout : Normalisation -> Sélection -> Prédiction
    prediction = model.predict(features_array)[0]
    
    # Calcul de la probabilité (Confiance du modèle)
    # predict_proba renvoie [proba_0, proba_1]. On prend la proba d'être classe 1.
    proba_bon_payeur = model.predict_proba(features_array)[0][1]
    
    # Mise en forme de la réponse
    resultat_texte = "Bon Payeur (Crédit Accordé)" if prediction == 1 else "Mauvais Payeur (Crédit Refusé)"
    
    return {
        "decision": int(prediction),
        "message": resultat_texte,
        "probabilite_bon_payeur": round(float(proba_bon_payeur), 4),
        "niveau_risque": "Faible" if proba_bon_payeur > 0.7 else "Élevé"
    }

# Lancement local (uniquement si exécuté comme script principal)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)