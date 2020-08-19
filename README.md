#### INSTALACIÓN DOCKER, DOCKER MACHINE, DOCKER COMPOSE EN CENTOS 7 ( NO FUNCIONA EN CENTOS 6 )
```
1.- mkdir -p /home/desarrollo/docker_install && cd /home/desarrollo/docker_install
```

```
2.- curl -fsSL get.docker.com -o get-docker.sh
```

```
3.- sh get-docker.sh
```

```
4.- usermod -aG docker root
```

```
5.- curl -L https://github.com/docker/machine/releases/download/v0.14.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine && chmod +x /tmp/docker-machine && sudo cp /tmp/docker-machine /usr/local/bin/docker-machine
```

```
6.- curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/
docker-compose
```

```
7.- chmod +x /usr/local/bin/docker-machine
```

```
8.- chmod +x /usr/local/bin/docker-compose
```

### COMPROBACIÓN DE INSTALACION ###
```
docker version
```
```
docker-machine version
```
```
docker-compose version
```

### ARRANQUE AUTOMATICO DEL SERVICIO DOCKER 
```
systemctl enable docker
```

### INICIAR DOCKER CONTAINERS

- Iniciar servicio docker
```
service docker start
```

- Crear network
```
docker network create devinexoos
```

-Iniciar Backend
```
cd /home/www/html/backend-py && docker-compose up --build -d
```


# Instalacion de Nodejs y NPM en centos 7
```
wget http://nodejs.org/dist/v0.10.30/node-v0.10.30.tar.gz
tar xzvf node-v* && cd node-v*
sudo yum install gcc gcc-c++
./configure
make
sudo make install
npm cache clean -f
npm install -g n
n stable
npm -v && node -v
```

# Extras
```
git rm -r --cached .
git add .
git commit -m "Eliminacion de cache pyc"
git push origins testing
```