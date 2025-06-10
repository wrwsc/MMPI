FROM node:20-alpine AS frontend-build
WORKDIR /frontend
COPY frontend/mmpi-test/package.json ./
RUN npm install
COPY frontend/mmpi-test/ ./
RUN npm run build


FROM python:3.12-slim AS backend-build
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev nginx netcat-openbsd procps && \
    rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

COPY --from=frontend-build /frontend/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]
