
# BETO - API de clasificación de comentarios

API REST desarrollada con **FastAPI** que utiliza un modelo BETO basado en BERT para español para clasificar comentarios de texto en dos clases.

Este proyecto forma parte de la asignatura **IA para Todos** y comprende el entrenamiento, la evaluación, la prueba y la exposición del modelo mediante una API.

## Tecnologías

- Python 3.10
- PyTorch
- Hugging Face Transformers
- BETO (`dccuchile/bert-base-spanish-wwm-cased`)
- FastAPI
- Uvicorn
- Pydantic

## Arquitectura

El sistema está compuesto por los siguientes elementos:

1. **Modelo de lenguaje:** BETO, ajustado mediante fine-tuning.
2. **Tokenizador:** transforma los comentarios en entradas que el modelo puede procesar.
3. **API REST:** FastAPI recibe las solicitudes y devuelve las predicciones.
4. **Motor de inferencia:** PyTorch ejecuta el modelo y calcula las probabilidades.

## Estructura del proyecto

```text
IAT-BETO-API/
├── beto-odio-limpio/  # Modelo y tokenizador (no incluido en Git)
├── main.py            # Aplicación FastAPI
├── requirements.txt   # Dependencias del proyecto
├── .gitignore
└── README.md
```

Los archivos del modelo deben obtenerse por separado y colocarse en la carpeta `beto-odio-limpio/`, junto a `main.py`.

## Instalación

Se recomienda utilizar Python 3.10.

### 1. Crear un entorno virtual

```bash
python -m venv .venv
```

Activarlo en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar las dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Preparar el modelo

Colocar los archivos del modelo entrenado en la carpeta `beto-odio-limpio/`. Deben incluir, entre otros, `config.json`, `model.safetensors` y los archivos del tokenizador.

### 4. Iniciar la API

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

La API estará disponible localmente en `http://127.0.0.1:8000`.

## Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Información general de la API. |
| GET | `/health` | Comprueba el estado de la API y del modelo. |
| POST | `/predict` | Clasifica un comentario de texto. |
| GET | `/docs` | Documentación interactiva de Swagger UI. |

## Ejemplo de predicción

Solicitud:

```json
{
  "texto": "Me gusta aprender cosas nuevas y compartir ideas."
}
```

Respuesta ilustrativa:

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

Las probabilidades del ejemplo corresponden a una prueba realizada durante el desarrollo; no son una respuesta fija para todas las solicitudes.

## Entrenamiento y evaluación

El modelo se entrenó mediante fine-tuning utilizando BETO y un conjunto de datos en español con etiquetas de clasificación.

Configuración principal del entrenamiento:

- Longitud máxima de entrada: 128 tokens.
- Épocas: 1.
- Tamaño de lote: 16.
- Tasa de aprendizaje: 2e-5.
- Muestra de entrenamiento utilizada: 20.000 registros.
- Evaluación de validación: 22.571 registros.

Resultados obtenidos en validación:

| Métrica | Resultado |
|---|---:|
| Accuracy | 0.8640 |
| Precision de CLASE_1 | 0.7723 |
| Recall de CLASE_1 | 0.6966 |
| F1 de CLASE_1 | 0.7325 |

Estas métricas corresponden a la validación frente a las etiquetas del conjunto de entrenamiento y no deben interpretarse como una medida definitiva de detección de discurso de odio en situaciones reales.

## Limitaciones y uso responsable

- `CLASE_0` y `CLASE_1` representan las etiquetas aprendidas durante el entrenamiento.
- Una predicción no constituye una determinación definitiva de discurso de odio.
- El rendimiento puede variar según el contexto, las expresiones regionales, la ironía y las características del texto.
- Las probabilidades del modelo no garantizan que una predicción sea correcta.
- Se requiere evaluación adicional con datos representativos y etiquetas humanas antes de considerar su uso en escenarios reales.

Este proyecto tiene fines académicos y experimentales.

## Estado del proyecto

- [x] Entrenamiento y evaluación inicial del modelo.
- [x] Pruebas de inferencia.
- [x] API REST con FastAPI.
- [x] Pruebas locales de `/`, `/health` y `/predict`.
- [ ] Publicación del código en GitHub.
- [ ] Despliegue de la API en AWS EC2.

## Licencia

Pendiente de definir.
