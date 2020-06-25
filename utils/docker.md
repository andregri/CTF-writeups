# Mastering docker

## Amazing tutorials and guides
1. [Liveoverflow tutorial](https://www.youtube.com/watch?v=cPGZMt4cJ0I)
2. [Basic commands](https://djangostars.com/blog/what-is-docker-and-how-to-use-it-with-python/)

### Basic commands
`sudo docker images`

shows the images installed on the computer from which you can build containers.

`sudo docker ps -a`

shows all containers.

**-a** to show all containers, those not running as well.

### Run a container
`sudo docker run`

**--rm** the container is automatically removed when it stops.

**-d** detached so the container works in the background.

**-v host_dir:container_dir** mount a directory in the host to a directory called in the container. Now you can access the files inside the host directory from the container. For example, you edit the files in the host and you run it from the container. Ex `-w $PWD:/pwd`.

**-i image_name:tag**  followed by the image name. Ex `-i angr/angr:latest`. (If you don't remember the image name use `sudo docker images`).

**-t** to open a terminal inside the container. (Don't use `-d` if you need to open a terminal).

**-p host_port:container_port** to open a port if you want to communicate by means of a server. Ex `-p 1204:1204`.

Full command example: `sudo docker run --rm -v $PWD:/pwd -it angr/angr`.  Now, from the container terminal, type  `cd /pwd && ls`: it lists the same files in the directory of the host! `exit` to exit from the terminal.

`sudo docker stop container name` to stop a running container.

`sudo docker start container name` to start an existing container.

Once you have done you should have the containers automatically removed if you used `--rm`.  If you didn't used that option, type `sudo docker rm container_name`.

### dockerfile

It's a text file that contains some instructions to set up and build a container more rapidly. Example (file name must all lowercase):

_dockerfile_
```
FROM angr/angr:latest

WORKDIR /home/ctf

COPY hello.py .

CMD python hello.py
```

To create a container from a dockerfile `sudo docker run --rm -i dockerfile`.

To build an image using these instructions `sudo docker build -t dockerfile .` TO STUDY
