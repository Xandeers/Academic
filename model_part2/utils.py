import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer


def load_and_clean_data(filename="credit.data"):
    
    try:
        # On ajoute sep=',' pour obliger Pandas à séparer les colonnes
        df = pd.read_csv(filename, header=None, sep=',')
    except FileNotFoundError:
        return None, None, None

    # verif
    if df.shape[1] < 2:
        # Si ça n'a toujours pas marché, on tente avec un autre séparateur
        try:
             df = pd.read_csv(filename, header=None, sep=None, engine='python')
        except:
             pass

    # Transformation Numpy
    data = df.values
    X_brut = data[:, :-1]
    Y_brut = data[:, -1]

    # Sélection des numériques
    indices_numeriques = [1, 2, 7, 10, 13, 14]
    
    # Sécurité : Vérifie que l'index max existe bien
    if X_brut.shape[1] <= max(indices_numeriques):
        raise IndexError(f"Erreur de lecture : Le fichier n'a que {X_brut.shape[1]} colonnes, impossible d'accéder à l'index 14.")

    X_num = X_brut[:, indices_numeriques]

    # Nettoyage
    X_num[X_num == '?'] = np.nan
    X_num = X_num.astype(float)

    # Suppression NaN
    mask_clean = ~np.isnan(X_num).any(axis=1)
    X_clean = X_num[mask_clean]
    Y_clean = Y_brut[mask_clean]

    # Binarisation
    Y_clean = np.where(Y_clean == '+', 1, 0).astype(int)

    return X_clean, Y_clean, df.shape






def run_normalization_tests(X, Y, clfs, run_classifiers_function):
 
    # A. StandardScaler
    print("\n" + "="*60)
    print(" 2a. RÉSULTATS AVEC STANDARDSCALER (Moy=0, Std=1)")
    print("="*60)
    scaler_std = StandardScaler()
    X_std = scaler_std.fit_transform(X)
    run_classifiers_function(X_std, Y, clfs)

    # B. MinMaxScaler
    print("\n" + "="*60)
    print(" 2b. RÉSULTATS AVEC MINMAXSCALER (0 -> 1)")
    print("="*60)
    scaler_mm = MinMaxScaler()
    X_mm = scaler_mm.fit_transform(X)
    run_classifiers_function(X_mm, Y, clfs)



def load_and_process_full_data(filename="credit.data"):
  
    # 1. Chargement
    try:
        df = pd.read_csv(filename, header=None, sep=',')
    except:
        return None, None

    if df.shape[1] < 2:
        df = pd.read_csv(filename, header=None, sep=None, engine='python')

    # Remplacement global des '?'
    df = df.replace('?', np.nan)
    data = df.values
    X_raw = data[:, :-1]
    Y_raw = data[:, -1]

    # 2. Séparation des colonnes (Indices fixés par UCI)
    col_num = [1, 2, 7, 10, 13, 14]
    col_cat = [0, 3, 4, 5, 6, 8, 9, 11, 12]

    # --- TRAITEMENT NUMÉRIQUE ---
    X_num = X_raw[:, col_num]
    X_num = X_num.astype(float)
    
    # Imputation par la MOYENNE (Mean)
    imp_num = SimpleImputer(strategy='mean')
    X_num_imputed = imp_num.fit_transform(X_num)
    
    # Normalisation (StandardScaler) - Demandé dans la consigne
    scaler = StandardScaler()
    X_num_scaled = scaler.fit_transform(X_num_imputed)

    # --- TRAITEMENT CATÉGORIEL ---
    X_cat = X_raw[:, col_cat]
    
    # Imputation par la VALEUR LA PLUS FRÉQUENTE (Most Frequent)
    imp_cat = SimpleImputer(strategy='most_frequent')
    X_cat_imputed = imp_cat.fit_transform(X_cat)
    
    # Encodage ONE-HOT (Création des variables binaires)
    # sparse_output=False pour avoir un tableau Numpy direct
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_cat_bin = encoder.fit_transform(X_cat_imputed)

    # --- CONCATÉNATION ---
    # On colle les colonnes numériques normalisées et les colonnes binaires
    X_final = np.hstack((X_num_scaled, X_cat_bin))
    
    # Target
    Y_final = np.where(Y_raw == '+', 1, 0).astype(int)

    return X_final, Y_final