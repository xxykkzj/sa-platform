useful docker commands

cd to project folder and run following command to deploy
```
docker compose -f docker-compose.yml up --build -d
```

stop the containers
```
docker compose stop
```

start the containers
```
docker compose start
```

Check docker disk usage
```
docker system df
```

Check the list of containers
```
docker ps
```

Check container stats (CPU, Memory etc)
```
docker stats
```

check docker images
```
docker images
```

remove old images. This will remove dangling images
```
docker image prune
```

check container logs
```
docker logs -f --tail {number of lines of logs to see} {container_name or container_id}
```
