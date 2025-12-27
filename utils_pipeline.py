import numpy as np
import pickle
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from utils import feature_importance, search_best_parameters, evaluation
from sklearn.model_selection import GridSearchCV



# --- Fonction 6 : Creation et Sauvegarde du Pipeline ---
def create_and_save_pipeline(X_train, Y_train, best_params_mlp, filename="credit_scoring_pipeline.pkl"):
 
    print(f"\n>>> Création du Pipeline de production...")
    
    # Définition du selec de var
    # On automatise ce qu'on a fait manuellement à l'étape 5.
    # On demande au RF de garder les 8 meilleures variables (max_features=8)
    selector = SelectFromModel(
        estimator=RandomForestClassifier(n_estimators=1000, random_state=1),
        max_features=8,
        threshold=-np.inf 
    )
    
    # def du classifieur avec meilleurs paramètres trouvés
    classifier = MLPClassifier(**best_params_mlp)
    
    # assemblage du Pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),       # Etape 1 : On normalise
        ('selection', selector),            # Etape 2 : On garde les 8 variables importantes
        ('classifier', classifier)          # Etape 3 : On prédit avec le MLP
    ])
    
    # entraînement global
    # On lui donne X_train bruten(non normalisé, non réduit), le pipeline gère tout 
    print("Entraînement du pipeline complet en cours...")
    pipeline.fit(X_train, Y_train)
    
    # Sauv en Pickle
    with open(filename, 'wb') as f:
        pickle.dump(pipeline, f)
        
    print(f"Pipeline sauvegardé avec succès dans '{filename}'")
    return pipeline



def pipeline_generation_train_test_split(X, Y, feature_names):

    print("\n" + "="*60)
    print(">>> DÉMARRAGE DE L'ORCHESTRATION (PIPELINE GENERATION) <<<")
    print("="*60)

    # Split
    print("\n[ETAPE 1] Séparation Train/Test...")
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5, random_state=1)
    
    # prep tempo pour l'analyse (Normalisation)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Selec des var
    print("\n[ETAPE 2] Sélection des variables...")
 
    sorted_idx = feature_importance(X_train_scaled, Y_train, feature_names)
    
    optimal_k = 8
    indices_keep = sorted_idx[:optimal_k]
    X_train_select = X_train_scaled[:, indices_keep]
    print(f"-> Variables retenues : {feature_names[indices_keep]}")

    # opti
    print("\n[ETAPE 3] Optimisation (GridSearch)...")
    param_grid = {
        'hidden_layer_sizes': [(100,), (40, 20)], 
        'activation': ['tanh', 'relu'],
        'alpha': [0.05, 0.0001],
        'solver': ['adam'],
        'max_iter': [1000]
    }
    base_model = MLPClassifier(random_state=1)
   
    best_params, _ = search_best_parameters(base_model, param_grid, X_train_select, Y_train)

    # crea Pipeline
    print("\n[ETAPE 4] Création du Pipeline Final...")
    
    pipeline = create_and_save_pipeline(X_train, Y_train, best_params, "credit_scoring_pipeline.pkl")
    
    # Test Final 
    print("\n[ETAPE 5] Test final automatique...")
    Y_pred_final = pipeline.predict(X_test)
    
    
    evaluation("Pipeline Orchestré Final", Y_test, Y_pred_final, None)
    
    print("\n" + "="*60)
    print(">>> ORCHESTRATION TERMINÉE <<<")
    print("="*60)
    
    return pipeline





#---fonction pipeline question 10 meilleur alogo identifié

def pipeline_generation_cv(X, Y, best_model_name, best_model_instance, param_grid_best_model):
    """
    Orchestre la mise en production du MEILLEUR algorithme identifié.
    1. Split
    2. GridSearch sur le meilleur algo
    3. Création Pipeline Final
    4. Sauvegarde Pickle
    """
    print(f"\n>>> ORCHESTRATION FINALE POUR LE VAINQUEUR : {best_model_name} <<<")
    
    # Split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5, random_state=1)
    
    # Recherche des meilleurs paramètres pour ce champion
    print(f"Optimisation des paramètres pour {best_model_name}...")
    grid = GridSearchCV(best_model_instance, param_grid_best_model, scoring='accuracy', cv=5)
    
    # On normalise juste pour le GridSearch (le pipeline final le fera lui-même)
    scaler_temp = StandardScaler()
    X_train_scaled = scaler_temp.fit_transform(X_train)
    
    grid.fit(X_train_scaled, Y_train)
    best_params = grid.best_params_
    print(f"Meilleurs paramètres trouvés : {best_params}")
    
    # 3. Création du Pipeline Final (Scaler + Model Optimisé)
    
    final_model = grid.best_estimator_
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', final_model)
    ])
    
    pipeline.fit(X_train, Y_train) # Entraînement sur données brutes
    
    # Sauvegarde
    filename = f"pipeline_final_{best_model_name.replace(' ', '_')}.pkl"
    with open(filename, 'wb') as f:
        pickle.dump(pipeline, f)
        
    print(f" Pipeline sauvegardé : {filename}")
    
    # 5. Score final
    score = pipeline.score(X_test, Y_test)
    print(f"Score final sur Test Set : {score:.4f}")
    
    return pipeline