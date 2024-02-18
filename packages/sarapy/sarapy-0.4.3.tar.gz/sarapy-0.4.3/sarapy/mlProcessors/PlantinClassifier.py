###Documentación en https://github.com/lucasbaldezzari/sarapy/blob/main/docs/Docs.md
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sarapy.mlProcessors import PlantinFMCreator

class PlantinClassifier(BaseEstimator, TransformerMixin):
    """Clase para implementar el pipeline de procesamiento de datos para la clasificación del tipo de operación para plantines."""
    
    def __init__(self, **kwargs):
        """Constructor de la clase PlantinClassifier."""
        
        plclass_map = {"imputeDistances", "distanciaMedia", "umbral_precision"," dist_mismo_lugar", "max_dist",
                       "umbral_ratio_dCdP", "deltaO_medio"}
        
        kwargs_plfmc = {}
        
        ##recorro kwargs y usando plclass_map creo un nuevo diccionario con los valores que se pasaron
        for key, value in kwargs.items():
            if key in plclass_map:
                kwargs_plfmc[key] = value
        
        self._plantinFMCreator = PlantinFMCreator.PlantinFMCreator(**kwargs_plfmc)
        
        self._pipeline = Pipeline([
            ("FMCreator", self._plantinFMCreator),
        ])
        
    def classify(self, newData):
        """Genera la clasificación de las operaciones para plantines.
        
        newData: Es un array con los datos (strings) provenientes de la base de datos histórica. La forma de newData debe ser (n,4). Las columnas de newData deben ser,
                - 0: tlm_spbb son los datos de telemetría.
                - 1: date_oprc son los datos de fecha y hora de operación.
                - 2: latitud de la operación
                - 3: longitud de la operación
                - 4: precision del GPS
        """
        
        return self._pipeline.fit_transform(newData).round(2)
    
if __name__ == "__main__":
    from sarapy.dataProcessing import OpsProcessor

    #cargo archivo examples\volcado_17112023_NODE_processed.csv
    import pandas as pd
    import os
    path = os.path.join(os.getcwd(), "examples\\volcado_17112023_NODE_processed.csv")
    data_df = pd.read_csv(path, sep=";", )
    raw_data = data_df.to_numpy().astype(str)

    ##tomo raw_data y obtengo muestras de entre 7 a 15 filas una detrás de la otra. El valor de entre 7 y 15 es aleatorio.
    sample = []
    index = 0
    while True:
        random_value = np.random.randint(8, 15)
        if index + random_value < len(raw_data):
            sample.append(raw_data[index:index+random_value])
        else:
            break
        index += random_value

    op = OpsProcessor.OpsProcessor()
    ##actualizo el diccionario de operaciones
    op.updateOperationsDict(sample[12])
    op.operationsDict
    plantin_classifier = PlantinClassifier(imputeDistances = False)
    plantin_classifier.classify(op.operationsDict["1"]["sample_ops"])    