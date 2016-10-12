rm -rf celerybeat*
docker-compose build
docker-compose up -d
docker-compose logs
