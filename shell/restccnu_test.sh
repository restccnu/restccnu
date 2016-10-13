#!/bin/sh

docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml up -d
docker-compose -f docker-compose.test.yml logs --tail="all" restccnu_test
