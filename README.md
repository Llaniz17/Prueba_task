# Prueba Técnica: Sistema de Gestión de Tareas con Django y Consumo de Servicio Externo (DRF)

Objetivo: Evaluar el dominio de Django (modelos, vistas, templates) y la capacidad para consumir servicios externos usando Django REST Framework (DRF).

## Requerimientos previos 

Python, preferiblemente *+3.10*
Herramienta para crear entornos virtuales, preferiblemente virtualenv o venv

## Instalación 

## Clonar repositorio 

```bash
git clone https://github.com/Llaniz17/Prueba_task.git
```

## Crear entorno virtual y activartlo 

```bash
python -m venv env
env\Scripts\activate    #Windows
source env/bin/activate   #MAc o Linux
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Realizar migraciones y crear superusuario

```bash
python manage.py makemigrations
python manage.py makemigrations task_manager
python manage.py migrate 
python manage.py createsuperuser
```

## Api Key

Crear un archivo .env en el directorio raiz y guardar tu Api Key de Open Weather en una variable llamada WEATHER_API_KEY

```bash
WEATHER_API_KEY=tuapikey
```

## Uso de la Aplicación
- Iniciar Sesión: Ingresa con el superusuario creado.
- Crear Tareas: Añade una nueva tarea con título, descripción, fecha límite y ciudad.
- Editar y Completar Tareas: Puedes marcar como completada o desmarcarla.
- Consultar Clima: Si la tarea tiene una ciudad, se obtiene el clima desde la api de OpenWeatherMap.

## Llenar base de datos para la prueba y uso 

Ingresar a http://127.0.0.1:8000/tasks/ ó localhost:8000/tasks/, Crear nueva tarea, preferiblemente con una ciudad y hacer uso de los filtros

## Api local con DRF

Ingresar a http://127.0.0.1:8000/api/tasks/1/weather/ para ver la información del clima de la ciudad de tu primera tarea, puedes cambiar el numero o seguir una de las siguientes posibles rutas para ver otra información

- api/
- api/tasks/
- api/tasks/1

## Tests 

Para ejecutar las pruebas automaticas, copia la siguiente línea, si todo marcha correcto el resultado será OK

```bash
python manage.py test
```

## License

@Llaniz
