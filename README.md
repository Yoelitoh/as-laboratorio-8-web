# as-laboratorio-8-web
# as-laboratorio-8-web

Laboratorio 8 de Administración de Sistemas: CI/CD con GitHub Actions,
Docker Hub y Google Kubernetes Engine (GKE).

## Aplicación

Web en Flask (Python) que muestra un contador de visitas guardado en Redis.
Son 2 contenedores: `web` (imagen propia) y `redis` (imagen `redis:alpine`).

## Estructura del repositorio

- `app/`: código de la aplicación (`app.py`, `requirements.txt`, `Dockerfile`).
- `k8s/`: ficheros YAML de Kubernetes (2 Deployments, Service ClusterIP
  `redis` y Service LoadBalancer `web`).
- `.github/workflows/despliegue.yml`: workflow de despliegue.
- `.github/workflows/pruebas.yml`: workflow de pruebas.

## Workflow de despliegue

Se lanza solo con un push a la rama `main`. Pasos:

1. Descarga el código del repositorio.
2. Hace login en Docker Hub (con secretos), construye la imagen y la sube a
   `as-laboratorio-8-web`.
3. Se autentica en Google Cloud con Workload Identity Federation (sin claves).
4. Obtiene las credenciales del cluster GKE para poder usar `kubectl`.
5. Aplica los YAML con `kubectl apply -f k8s/` y reinicia el Deployment `web`
   con `kubectl rollout restart deployment web`.

El Deployment `web` usa `imagePullPolicy: Always`, y se hace el
`rollout restart` porque, si solo cambia el código, los YAML no cambian y
Kubernetes no actualizaría los Pods por sí solo.

## Workflow de pruebas

Se lanza con un push a cualquier rama que no sea `main`. Descarga el código y
lo analiza con pylint (`advanced-security/python-lint-code-scanning-action`).
Los resultados aparecen en Security > Code scanning.

## Flujo de trabajo

1. Crear una rama (`nueva-caracteristica`) y hacer cambios.
2. Push a la rama: se ejecutan las pruebas.
3. Corregir los avisos y hacer una Pull Request hacia `main`.
4. Al fusionarla, el push a `main` lanza el despliegue automático.
