import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, roc_curve, auc, make_scorer
from sklearn.ensemble import RandomForestClassifier
import shap
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier


# --- Fonction 1 : Évaluation ---
def evaluation(model_name, Y_test, Y_pred, Y_proba):
    """
    Affiche la matrice de confusion, les métriques et la courbe ROC.
    Retourne le score final (Accuracy + Precision) / 2.
    """
    print(f"\n>>> Evaluation du modèle : {model_name}")
    
    # Matrice de confusion
    cm = confusion_matrix(Y_test, Y_pred)
    print("Matrice de Confusion :")
    print(cm)
    
    # Calcul des métriques
    acc = accuracy_score(Y_test, Y_pred)
    precision = precision_score(Y_test, Y_pred, zero_division=0)
    recall = recall_score(Y_test, Y_pred, zero_division=0)
    
    print(f"Accuracy  : {acc:.3f}")
    print(f"Précision : {precision:.3f}")
    print(f"Rappel    : {recall:.3f}")
    
    # Score combiné
    score_final = (acc + precision) / 2
    print(f"Score Final : {score_final:.3f}")

    # Courbe ROC
    if Y_proba is not None:
        fpr, tpr, _ = roc_curve(Y_test, Y_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(6, 4))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Taux de Faux Positifs')
        plt.ylabel('Taux de Vrais Positifs')
        plt.title(f'Courbe ROC - {model_name}')
        plt.legend(loc="lower right")
        plt.show()
    
    return score_final

# --- Fonction 2 : fonction d’apprentissage et de test  ---

def run_classifiers_train_test(classifiers, X_train, Y_train, X_test, Y_test):
    """
    Entraîne une liste de classifieurs et retourne le meilleur nom de modèle.
    """
    best_score = 0
    best_model_name = ""
    
    print(f"Comparaison de {len(classifiers)} algorithmes...\n")
    
    for name, clf in classifiers.items():
        # A. Apprentissage
        clf.fit(X_train, Y_train)
        
        # B. Prédiction
        Y_pred = clf.predict(X_test)
        
        # C. Gestion des probabilités
        if hasattr(clf, "predict_proba"):
            Y_proba = clf.predict_proba(X_test)[:, 1]
        else:
            Y_proba = None
            
        # D. Appel de la fonction locale evaluation
        current_score = evaluation(name, Y_test, Y_pred, Y_proba)
        
        # E. Comparaison
        if current_score > best_score:
            best_score = current_score
            best_model_name = name
            
    print("="*50)
    print(f"RESULTAT FINAL : Le meilleur modèle est {best_model_name} avec un score de {best_score:.3f}")
    print("="*50)
    
    return best_model_name


# --- Fonction 1 : Importance des variables (Random Forest) ---
def feature_importance(X_train, Y_train, feature_names):
    """
    Calcule et affiche l'importance des variables via Random Forest.
    Retourne les indices triés par importance décroissante.
    """
    print("\n>>> Calcul de l'importance des variables (Random Forest)...")
    
    # 1. Création et entraînement du RF (Paramètres imposés par le TP)
    clf = RandomForestClassifier(n_estimators=1000, random_state=1)
    clf.fit(X_train, Y_train)
    
    # 2. Extraction des importances
    importances = clf.feature_importances_
    std = np.std([tree.feature_importances_ for tree in clf.estimators_], axis=0)
    
    # 3. Tri des indices (du plus important au moins important)
    sorted_idx = np.argsort(importances)[::-1]
    
    # 4. Affichage graphique
    print("\nClassement des variables :")
    # On convertit feature_names en array pour pouvoir l'indexer avec sorted_idx
    features = np.array(feature_names)
    print(features[sorted_idx])
    
    plt.figure(figsize=(10, 6))
    padding = np.arange(X_train.shape[1]) + 0.5
    plt.barh(padding, importances[sorted_idx], xerr=std[sorted_idx], align='center')
    plt.yticks(padding, features[sorted_idx])
    plt.xlabel("Importance Relative")
    plt.title("Importance des Variables (Random Forest)")
    plt.gca().invert_yaxis() # Pour avoir la variable la plus importante en haut
    plt.show()
    
    return sorted_idx

# --- Fonction 2 : Sélection du nombre optimal de variables ---
def select_optimal_variables(best_model, X_train, Y_train, X_test, Y_test, sorted_idx):
    """
    Teste la performance du modèle en ajoutant les variables une par une
    selon l'ordre d'importance défini par sorted_idx.
    """
    print("\n>>> Sélection du nombre optimal de variables...")
    
    scores = np.zeros(X_train.shape[1])
    
    # Boucle sur le nombre de variables (de 1 à Total)
    for f in range(X_train.shape[1]):
        # On sélectionne les f+1 meilleures variables
        # Attention : sorted_idx contient les indices des colonnes
        cols_to_keep = sorted_idx[:f+1]
        
        X1_f = X_train[:, cols_to_keep]
        X2_f = X_test[:, cols_to_keep]
        
        # Entraînement du MEILLEUR ALGORITHME sur ce sous-ensemble
        best_model.fit(X1_f, Y_train)
        Y_pred = best_model.predict(X2_f)
        
        # Stockage du score (ici Accuracy comme demandé dans le snippet du TP)
        scores[f] = np.round(accuracy_score(Y_test, Y_pred), 3)
        
    # Affichage de la courbe
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, X_train.shape[1] + 1), scores, marker='o')
    plt.xlabel("Nombre de Variables")
    plt.ylabel("Accuracy")
    plt.title("Evolution de l'accuracy en fonction du nombre de variables")
    plt.grid(True)
    plt.show()
    
    # Retourne le nombre optimal de variables (là où le score est max)
    optimal_n = np.argmax(scores) + 1
    print(f"Score Max atteint : {np.max(scores)} avec {optimal_n} variables.")
    
    return optimal_n

# --- Fonction 3 : Explicabilité SHAP ---
def explicabilite_shap_mlp(model, Xtrain, Xtest, nom_cols):
    """
    Calcule et affiche l'explicabilité SHAP pour un modèle type boîte noire (MLP).
    Affiche : 
    1. Summary Plot (Global)
    2. Bar Plot pour le premier individu (Local)
    """
    # Conversion explicite en Numpy pour éviter les erreurs de format
    Xtrain_np = np.array(Xtrain)
    Xtest_np = np.array(Xtest)

    # On utilise un échantillon du background (train) pour initialiser l'explainer (plus rapide)
    # 100 exemples suffisent généralement pour estimer la moyenne
    idx_bg = np.random.choice(Xtrain_np.shape[0], 100, replace=False)
    background = Xtrain_np[idx_bg]

    # Fonction wrapper pour récupérer uniquement la proba de la classe 1 (Positive)
    def f(X):
        return model.predict_proba(X)[:, 1]

    # Initialisation du KernelExplainer
    print(">>> Initialisation de KernelExplainer (peut prendre quelques secondes)...")
    explainer = shap.KernelExplainer(f, background)

    # Calcul des valeurs SHAP sur un sous-ensemble de test (50 individus)
    X_exp = Xtest_np[:50]
    shap_values = explainer.shap_values(X_exp)

    # --- 1. Graphique Global (Summary Plot) ---
    print("\n=== Importance globale des variables (SHAP) ===")
    plt.figure()
    shap.summary_plot(shap_values, X_exp, feature_names=nom_cols)

    # --- 2. Graphique Local (Premier individu) ---
    print("\n=== Explication locale (Individu n°0) ===")
    # Création de l'objet Explanation pour le graphique en barres
    expl_local = shap.Explanation(
        values=shap_values[0],          # Contributions pour l'individu 0
        base_values=explainer.expected_value, # La valeur moyenne de base
        data=X_exp[0],                  # Les valeurs brutes des features
        feature_names=nom_cols
    )
    plt.figure()
    shap.plots.bar(expl_local, max_display=10, show=True)




    # --- Fonction 4 : Recherche des meilleurs paramètres (GridSearch) ---
def search_best_parameters(model, param_grid, X_train, Y_train):
    """
    Teste toutes les combinaisons de paramètres définies dans param_grid.
    Optimise le score : (Accuracy + Précision) / 2.
    Retourne les meilleurs paramètres et le meilleur modèle entraîné.
    """
    print(f"\n>>> Recherche des meilleurs hyperparamètres (GridSearchCV)...")
    print(f"Modèle de base : {model.__class__.__name__}")
    print(f"Paramètres testés : {param_grid}")
    
    # 1. Définition du score personnalisé (Accuracy + Precision) / 2
    def custom_score_func(y_true, y_pred):
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, zero_division=0)
        return (acc + prec) / 2
        
    # Transformation en "scorer" pour Scikit-learn
    my_scorer = make_scorer(custom_score_func)
    
    # 2. Configuration du GridSearch
    # cv=5 signifie qu'il fait une validation croisée à 5 blocs pour chaque combinaison
    grid = GridSearchCV(
        estimator=model, 
        param_grid=param_grid, 
        scoring=my_scorer, 
        cv=5, 
        n_jobs=-1, # Utilise tous les cœurs du processeur pour aller plus vite
        verbose=1
    )
    
    # 3. Lancement de la recherche
    grid.fit(X_train, Y_train)
    
    # 4. Affichage des résultats
    print("\n=== RÉSULTATS GRID SEARCH ===")
    print(f"Meilleur Score ((Acc+Prec)/2) : {grid.best_score_:.3f}")
    print("Meilleurs Paramètres trouvés :")
    print(grid.best_params_)
    
    return grid.best_params_, grid.best_estimator_


# --- Fonction 5 : Wrapper pour l'optimisation complète du MLP ---
def run_optimization_mlp(X_train, Y_train, X_test, Y_test):
    """
    Définit la grille de paramètres, lance la recherche (GridSearch)
    et évalue le meilleur modèle sur le jeu de test.
    """
    # 1. Définition de la grille de paramètres
    param_grid_mlp = {
        'hidden_layer_sizes': [(40, 20), (50, 50), (100,), (30, 30, 30)], 
        'activation': ['tanh', 'relu'],
        'alpha': [0.0001, 0.05],
        'solver': ['adam'],
        'max_iter': [1000] 
    }

    # 2. Initialisation du modèle de base
    base_model = MLPClassifier(random_state=1)

    # 3. Appel de la fonction de recherche (définie juste au-dessus dans utils.py)
    # Note : Comme on est dans le même fichier, on peut appeler search_best_parameters directement
    best_params, best_model_final = search_best_parameters(
        base_model, 
        param_grid_mlp, 
        X_train, 
        Y_train
    )

    # 4. Validation finale sur le jeu de Test
    print("\n>>> Validation finale du modèle optimisé sur le Test Set :")
    Y_pred_optim = best_model_final.predict(X_test)
    
    # Gestion des probabilités
    if hasattr(best_model_final, "predict_proba"):
        Y_proba_optim = best_model_final.predict_proba(X_test)[:, 1]
    else:
        Y_proba_optim = None

    # Appel de la fonction d'évaluation (aussi dans ce fichier)
    evaluation("MLP Optimisé", Y_test, Y_pred_optim, Y_proba_optim)
    
    return best_model_final

