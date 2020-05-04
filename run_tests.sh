#!/bin/bash

docker-compose -f docker-compose.tests.yml rm -fsv
docker-compose -f docker-compose.tests.yml build --pull
docker-compose -f docker-compose.tests.yml up --remove-orphans --exit-code-from=tests tests
docker-compose -f docker-compose.tests.yml rm -fsv
