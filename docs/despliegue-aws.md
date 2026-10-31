# Despliegue en AWS EC2

## Requisitos

- Cuenta AWS con permiso para EC2.
- Instancia Ubuntu 24.04 con puertos 22, 80, 8001 y 8002 habilitados en el grupo de seguridad.
- Docker Hub o GitHub Container Registry.
- Dominio HTTPS público para publicación real en Instagram.

## Publicación

```bash
docker login
docker build -t USUARIO/el3302-champions:1.0 pregunta1-champions
docker push USUARIO/el3302-champions:1.0
docker build -t USUARIO/el3302-marketing:1.0 pregunta2-marketing
docker push USUARIO/el3302-marketing:1.0
```

## Preparación de la instancia

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl git
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu
git clone URL_DEL_REPOSITORIO el3302-lab5
cd el3302-lab5
```

## Ejecución

```bash
cd pregunta1-champions
docker compose up --build -d
cd ../pregunta2-marketing
docker compose up --build -d
```

## Verificación

```bash
curl http://IP_PUBLICA:8001/health
curl http://IP_PUBLICA:8002/health
docker compose ps
docker volume ls
```

## Instagram real

Cambiar `SOCIAL_MODE` a `live`, configurar `PUBLIC_BASE_URL`, `INSTAGRAM_USER_ID`, `INSTAGRAM_ACCESS_TOKEN` e `INSTAGRAM_GRAPH_VERSION`. La cuenta debe ser profesional, la aplicación de Meta debe tener permiso de publicación y las imágenes deben ser accesibles desde una URL HTTPS pública.

## Evidencias requeridas

- Repositorio y etiquetas de las imágenes publicadas.
- Contenedores activos en EC2.
- Respuesta de ambos endpoints de salud.
- Interfaces accesibles desde la IP o dominio público.
- Volúmenes persistentes.

