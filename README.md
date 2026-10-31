# Laboratorio 5 Contenedores

## Pregunta 1

Aplicación web en tres capas para consultar partidos de Champions League y registrar predicciones.

```text
Navegador -> Presentación -> Lógica de negocio -> Acceso a datos -> PostgreSQL
                                   |
                                   -> API simulada de partidos
```

Al iniciar, la aplicación consulta la API simulada y guarda los partidos en PostgreSQL. Las predicciones se registran y consultan desde la misma base de datos.

### Instalación y ejecución

```powershell
cd pregunta1-champions
Copy-Item .env.example .env
docker compose up --build -d
```

Abrir http://localhost:8001

Para detener la aplicación:

```powershell
docker compose down
```

## Pregunta 2

Aplicación web que recibe una fotografía, propone tres guiones, permite escoger uno, genera tres imágenes y un video, y publica la campaña en modo simulado o mediante Instagram Graph API.

```text
Navegador -> Presentación -> Lógica de negocio -> PostgreSQL
                                   |
                                   -> Archivos persistentes
                                   -> Instagram Graph API
```

### Instalación y ejecución

```powershell
cd pregunta2-marketing
Copy-Item .env.example .env
docker compose up --build -d
```

Abrir http://localhost:8002

Para detener la aplicación:

```powershell
docker compose down
```

El modo predeterminado es `simulation`. Para publicar en Instagram se debe editar `.env`:

```env
SOCIAL_MODE=instagram
PUBLIC_BASE_URL=https://dominio-publico
INSTAGRAM_USER_ID=identificador
INSTAGRAM_ACCESS_TOKEN=token
```

## Persistencia

Docker Compose crea los volúmenes `champions_data`, `marketing_data` y `marketing_assets`. El comando `docker compose down` conserva la información.

## Imágenes publicadas

- `ghcr.io/tomlaura-bit/el3302-champions:latest`
- `ghcr.io/tomlaura-bit/el3302-marketing:latest`

## Despliegue en AWS EC2

Crear una instancia Ubuntu en `us-east-2` y permitir los puertos `22`, `8001` y `8002`. Conectarse por SSH y ejecutar:

```bash
sudo apt update
sudo apt install -y git docker.io docker-compose-v2
sudo usermod -aG docker $USER
newgrp docker
git clone https://github.com/tomlaura-bit/lab5.git
cd lab5/pregunta1-champions
cp .env.example .env
docker compose up --build -d
cd ../pregunta2-marketing
cp .env.example .env
docker compose up --build -d
```

Accesos:

- `http://IP_PUBLICA:8001`
- `http://IP_PUBLICA:8002`
