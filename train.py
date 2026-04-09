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
    # Ignorar advertencias no críticas para mantener limpia la salida en la consola de ejecución
    warnings.filterwarnings('ignore')

def create_output_directory(folder_name):
    # Crear el directorio estructurado para guardar los gráficos si este no existe
    os.makedirs(folder_name, exist_ok=True)

def load_data(file_path):
    # Cargar el conjunto de datos completo y seleccionar exclusivamente las columnas relevantes para el modelo
    raw_df = pd.read_csv(file_path)
    columns_to_keep = [
        "games", "time", "goals", "xG", "assists", "xA", "shots", 
        "key_passes", "yellow_cards", "red_cards", "position", 
        "npg", "npxG", "xGChain", "xGBuildup", "tackles"
    ]
    return raw_df[columns_to_keep]

def engineer_features(df):
    # Crear nuevas características de desempeño promediadas por el volumen de partidos
    df_engineered = df.copy()
    df_engineered['tackles_per_game'] = df_engineered['tackles'] / df_engineered['games']
    df_engineered['goals_per_game'] = df_engineered['goals'] / df_engineered['games']
    df_engineered['assists_per_game'] = df_engineered['assists'] / df_engineered['games']
    df_engineered['key_passes_per_game'] = df_engineered['key_passes'] / df_engineered['games']
    return df_engineered

def prepare_features_and_labels(df):
    # Limpiar la columna objetivo de la posición (etiqueta) y separarla de las características
    df["position"] = [x.split()[0] for x in df["position"]]
    
    X = df.drop("position", axis=1)
    y_raw = df["position"]

    # Codificar las etiquetas de texto de los objetivos a sus respectivos valores numéricos
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)
    class_names = label_encoder.classes_

    # Mapear las siglas en inglés de las posiciones futbolísticas al español para la inferencia
    mapping = {
        "D": "Defensa",
        "GK": "Portero",
        "F": "Delantero",
        "M": "Centrocampista",
        "S": "Segundo delantero"
    }

    # Vectorización y aplicación del mapa de traducciones a los nombres de las clases del modelo
    vectorized_mapping_function = np.vectorize(lambda x: mapping.get(x, x))
    mapped_class_names = vectorized_mapping_function(class_names)

    return X, y, mapped_class_names

def train_model(X, y):
    # Dividir estratificadamente los datos de entrenamiento y de test y entrenar el pipeline final
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y
    )

    # Creación del Pipeline con transformaciones polinomiales para la expansión de características
    model_pipeline = Pipeline([
        ('poly', PolynomialFeatures(degree=2, include_bias=False)),
        ('model', RandomForestClassifier(
            class_weight="balanced",
            n_estimators=200,
            max_depth=20,
            min_samples_leaf=2,
            max_features='log2'
        ))
    ])

    # Ajuste e inferencia del modelo
    model_pipeline.fit(X_train, y_train)
    
    # Predecir sobre los sets de Train y Test para permitir la posterior evaluación técnica de sobreajuste (overfitting)
    y_pred_train = model_pipeline.predict(X_train)
    y_pred_test = model_pipeline.predict(X_test)
    
    return model_pipeline, X_train, X_test, y_train, y_test, y_pred_train, y_pred_test

if __name__ == "__main__":
    # 1. Configuración de entorno inicial
    ignore_warnings()
    dataset_file_path = "data_input/Estadisticas_Jugadores.csv"
    output_graphics_folder = "model_info"
    
    # Crear la carpeta de alojamiento de meta-gráficos
    create_output_directory(output_graphics_folder)
    
    # 2. Pipeline de Carga y preprocesamiento de datos
    df_raw = load_data(dataset_file_path)
    df_engineered = engineer_features(df_raw)
    X_features, y_target, mapped_class_names = prepare_features_and_labels(df_engineered)
    
    # 3. Entrenamiento del modelo evaluando particiones train/test
    pipeline, X_train, X_test, y_train, y_test, y_pred_train, y_pred_test = train_model(X_features, y_target)

    # 4. Serialización y almacenamiento del modelo final (Pipeline) en disco
    models_path = Path("modelos")
    models_path.mkdir(exist_ok=True)
    joblib.dump(pipeline, "modelos/pipeline_futbolistico.pkl")