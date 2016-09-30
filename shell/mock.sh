docker-compose build
docker-compose stop restccnu_restccnu
docker-compose stop restccnu_redis1
docker-compose stop restccnu_redis2
docker-compose up -d
docker-compose logs
