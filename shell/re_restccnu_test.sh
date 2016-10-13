#!/bin/sh

docker-compose -f docker-compose.test.yml restart
docker-compose -f docker-compose.test.yml logs restccnu_test
