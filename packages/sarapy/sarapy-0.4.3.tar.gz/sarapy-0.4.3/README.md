# SARAPY

Library for processing SARAPICO project metadata of _AMG_.

#### Version 0.4.3

- Se agrega fit() dentro de transform() de PlantinFMCreator.

#### Version 0.4.2

- Se agrega \*\*kwargs en OpsProcessor, PlantinClassifier y PlantinFMCreator para poder setear los atributos de PlantinFMCreator desde las clases que lo usen.

#### Version 0.4.1

- Se corrigen problemas de importaciones circulares.

#### Version 0.4.0

- Se implementa _OpsProcessor_.
- Se implementa _PlanntinClassifier_.
- Se corrige salida de _transform()_ y _fit_transform()_ de GeoProcessor.
- Se mueve PlantinFMCreator a mlProcessors
- Se cambia nombre de TLMSensorDataCreator a TLMSensorDataProcessor
