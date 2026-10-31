# EL3302 Laboratorio 5 Contenedores

Solución de las dos preguntas del laboratorio. Cada aplicación incluye interfaz web, lógica de negocio, acceso a datos, PostgreSQL, Dockerfile, Docker Compose, variables de entorno y volumen persistente.

## Estructura

- `pregunta1-champions`: gestión de partidos y predicciones de Champions League.
- `pregunta2-marketing`: generación de campañas a partir de una fotografía.
- `docs`: arquitectura, flujo de datos, despliegue y guion del video.
- `evidencias`: capturas del funcionamiento.
- `informe`: informe final en Word.

## Ejecución de la Pregunta 1

```bash
cd pregunta1-champions
docker compose up --build -d
```

Abrir `http://localhost:8001`.

```bash
docker compose down
```

## Ejecución de la Pregunta 2

```bash
cd pregunta2-marketing
docker compose up --build -d
```

Abrir `http://localhost:8002`.

```bash
docker compose down
```

## Pruebas

```bash
docker compose -f pregunta1-champions/docker-compose.yml run --rm app pytest -q
docker compose -f pregunta2-marketing/docker-compose.yml run --rm app pytest -q
```

## Publicación de imágenes

```bash
docker login
docker build -t USUARIO/el3302-champions:1.0 pregunta1-champions
docker push USUARIO/el3302-champions:1.0
docker build -t USUARIO/el3302-marketing:1.0 pregunta2-marketing
docker push USUARIO/el3302-marketing:1.0
```

## Despliegue

El procedimiento completo para AWS EC2 está en `docs/despliegue-aws.md`. Requiere una cuenta AWS, una clave SSH y credenciales del registro elegido.

## Entregables

- Código fuente ejecutable.
- Diagramas y flujo de datos.
- Informe con evidencias.
- Guion de demostración menor a cinco minutos.

