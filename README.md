# BETO

## API de clasificación de comentarios en español

**Proyecto académico | Asignatura IA para Todos**

BETO es una API REST desarrollada con FastAPI que utiliza un modelo basado en BERT, adaptado al español, para clasificar comentarios de texto en dos clases.

El proyecto abarca el ajuste del modelo mediante fine-tuning, su evaluación experimental y la exposición de las predicciones mediante una API REST.

Su objetivo es explorar la aplicación de modelos de lenguaje basados en Transformers a tareas de clasificación de texto en español.

> Este proyecto tiene fines académicos y experimentales. Sus predicciones no constituyen una determinación definitiva de discurso de odio.

## Tecnologías

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)

## Funcionalidades principales

- Clasificación de comentarios escritos en español.
- Inferencia mediante un modelo BETO ajustado con fine-tuning.
- Exposición del modelo mediante una API REST.
- Consulta del estado del servicio y del modelo.
- Obtención de la clase predicha y sus probabilidades.
- Documentación interactiva de los endpoints mediante Swagger UI.

## Arquitectura

El sistema se compone de cuatro elementos principales:

| Componente | Responsabilidad |
|---|---|
| Modelo BETO | Procesamiento del texto y clasificación de comentarios. |
| Tokenizador | Conversión del texto en las entradas requeridas por el modelo. |
| Motor de inferencia | Ejecución del modelo mediante PyTorch. |
| API REST | Recepción de solicitudes y entrega de las predicciones mediante FastAPI. |

El modelo base utilizado es `dccuchile/bert-base-spanish-wwm-cased`, ajustado mediante fine-tuning para la tarea de clasificación.

## Estructura del proyecto

```text
IAT-BETO-API/
├── beto-odio-limpio/  # Modelo entrenado y tokenizador
├── main.py            # Aplicación FastAPI
├── requirements.txt   # Dependencias
├── .gitignore
└── README.md
```

Los archivos del modelo entrenado no están incluidos en el repositorio. Para ejecutar la API, deben obtenerse por separado y ubicarse en la carpeta `beto-odio-limpio/`, de acuerdo con la configuración de `main.py`.

## Instalación y ejecución

### Requisitos

- Python 3.10.
- Dependencias definidas en `requirements.txt`.
- Archivos del modelo entrenado y su tokenizador.

### 1. Crear un entorno virtual

```bash
python -m venv .venv
```

En Windows PowerShell, activar el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar las dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Preparar el modelo

Coloca los archivos del modelo entrenado en la carpeta `beto-odio-limpio/`.

Estos pueden incluir `config.json`, `model.safetensors` y los archivos de configuración del tokenizador, según el formato guardado durante el entrenamiento.

### 4. Iniciar la API

Desde el directorio que contiene `main.py`, ejecuta:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

La API estará disponible en `http://127.0.0.1:8000`.

## Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Información general de la API. |
| GET | `/health` | Consulta el estado de la API y del modelo. |
| POST | `/predict` | Clasifica un comentario de texto. |
| GET | `/docs` | Documentación interactiva mediante Swagger UI. |

## Ejemplo de predicción

### Solicitud

```json
{
  "texto": "Me gusta aprender cosas nuevas y compartir ideas."
}
```

### Respuesta ilustrativa

```json
{
  "clase_predicha": "CLASE_0",
  "probabilidades": {
    "CLASE_0": 0.995951,
    "CLASE_1": 0.004049
  },
  "dispositivo": "cpu",
  "advertencia": "Resultado experimental basado en las etiquetas del conjunto de entrenamiento; no constituye una determinación definitiva de discurso de odio."
}
```

Los valores anteriores corresponden a una prueba realizada durante el desarrollo. Se muestran como ejemplo y no representan una respuesta fija para todas las solicitudes.

## Entrenamiento y evaluación

El modelo se ajustó mediante fine-tuning a partir de BETO, utilizando un conjunto de datos en español con etiquetas de clasificación.

### Configuración del entrenamiento

| Parámetro | Valor |
|---|---:|
| Longitud máxima de entrada | 128 tokens |
| Épocas | 1 |
| Tamaño de lote | 16 |
| Tasa de aprendizaje | 2e-5 |
| Muestra de entrenamiento utilizada | 20.000 registros |
| Registros de validación | 22.571 |

### Resultados de validación

| Métrica | Resultado |
|---|---:|
| Accuracy | 0.8640 |
| Precision de CLASE_1 | 0.7723 |
| Recall de CLASE_1 | 0.6966 |
| F1 de CLASE_1 | 0.7325 |

Estos resultados corresponden a la evaluación realizada durante el desarrollo frente a las etiquetas del conjunto de datos utilizado. No deben interpretarse como una medida definitiva del rendimiento del modelo en situaciones reales.

## Limitaciones y uso responsable

- `CLASE_0` y `CLASE_1` corresponden a las etiquetas aprendidas durante el entrenamiento.
- Las predicciones dependen de los datos y las características lingüísticas presentes en el conjunto de entrenamiento.
- El contexto, la ironía, las expresiones regionales y las particularidades del lenguaje pueden afectar los resultados.
- Las probabilidades representan las estimaciones del modelo y no garantizan que una clasificación sea correcta.
- Antes de utilizar el sistema en escenarios reales, se requiere una evaluación adicional con datos representativos y criterios de etiquetado revisados por personas.

## Estado del proyecto

- [x] Entrenamiento y evaluación inicial del modelo.
- [x] Pruebas de inferencia.
- [x] Implementación de la API REST con FastAPI.
- [x] Pruebas locales de los endpoints `/`, `/health` y `/predict`.
- [ ] Publicación del código en GitHub.
- [ ] Despliegue de la API en AWS EC2.

## Licencia

Pendiente de definir.