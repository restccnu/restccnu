#!/bin/sh

/usr/local/bin/docker-compose -f docker-compose.test.yml build
/usr/local/bin/docker-compose -f docker-compose.test.yml up -d
/usr/local/bin/docker-compose -f docker-compose.test.yml logs --tail="all" restccnu_test
