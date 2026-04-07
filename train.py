import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path
import warnings

def ignore_warnings():
    # Ignorar advertencias para mantener limpia la salida en la consola
    warnings.filterwarnings('ignore')

def create_output_directory(folder_name):
    # Crear el directorio para guardar los graficos si no existe
    os.makedirs(folder_name, exist_ok=True)

def load_data(file_path):
    # Cargar el conjunto de datos y seleccionar las columnas relevantes
    df = pd.read_csv(file_path)
    columns_to_keep = [
        "games", "time", "goals", "xG", "assists", "xA", "shots", 
        "key_passes", "yellow_cards", "red_cards", "position", 
        "npg", "npxG", "xGChain", "xGBuildup", "tackles"
    ]
    return df[columns_to_keep]

def engineer_features(df):
    # Crear nuevas caracteristicas basadas en promedios por partido
    df_engineered = df.copy()
    df_engineered['tackles_per_game'] = df_engineered['tackles'] / df_engineered['games']
    df_engineered['goals_per_game'] = df_engineered['goals'] / df_engineered['games']
    df_engineered['assists_per_game'] = df_engineered['assists'] / df_engineered['games']
    df_engineered['key_passes_per_game'] = df_engineered['key_passes'] / df_engineered['games']
    return df_engineered

def prepare_features_and_labels(df):
    # Limpiar la columna de posicion y separar caracteristicas de la etiqueta
    df["position"] = [x.split()[0] for x in df["position"]]
    
    X = df.drop("position", axis=1)
    y_raw = df["position"]

    # Codificar las etiquetas de texto a valores numericos
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)
    class_names = label_encoder.classes_

    # Mapear las siglas de las posiciones al espanol
    mapping = {
        "D": "Defensa",
        "GK": "Portero",
        "F": "Delantero",
        "M": "Centrocampista",
        "S": "Segundo delantero"
    }

    vectorized_mapping_function = np.vectorize(lambda x: mapping.get(x, x))
    mapped_class_names = vectorized_mapping_function(class_names)

    return X, y, mapped_class_names

def train_model(X, y):
    # Dividir los datos y entrenar el pipeline
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y
    )

    pipeline = Pipeline([
        ('poly', PolynomialFeatures(degree=2, include_bias=False)),
        ('model', RandomForestClassifier(
            class_weight="balanced",
            n_estimators=200,
            max_depth=20,
            min_samples_leaf=2,
            max_features='log2'
        ))
    ])

    pipeline.fit(X_train, y_train)
    
    # Predecir en Train y en Test para poder evaluar el sobreajuste (overfitting)
    y_pred_train = pipeline.predict(X_train)
    y_pred_test = pipeline.predict(X_test)
    
    return pipeline, X_train, X_test, y_train, y_test, y_pred_train, y_pred_test

if __name__ == "__main__":
    # 1. Configuracion inicial
    ignore_warnings()
    file_path = "data_input/Estadisticas_Jugadores.csv"
    graphics_folder = "model_info"
    
    # Crear carpeta para los graficos
    create_output_directory(graphics_folder)
    
    # 2. Carga y preprocesamiento
    df_raw = load_data(file_path)
    df_engineered = engineer_features(df_raw)
    X, y, mapped_class_names = prepare_features_and_labels(df_engineered)
    
    # 3. Entrenamiento del modelo evaluando train y test
    pipeline, X_train, X_test, y_train, y_test, y_pred_train, y_pred_test = train_model(X, y)

    # 4. Almacenar el pipeline en disco
    path_modelos= Path("modelos")
    path_modelos.mkdir(exist_ok=True)
    joblib.dump(pipeline, "modelos/pipeline_futbolistico.pkl")