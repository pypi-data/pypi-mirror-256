# Polytechnique INF581 2024

Copyright (c) 2019-2024 Jérémie Decock

<img src="https://raw.githubusercontent.com/jeremiedecock/polytechnique-inf581-2024-students/main/logo.jpg" width="250">

- Github repository for students: https://github.com/jeremiedecock/polytechnique-inf581-2024-students
- Github repository for teachers: https://github.com/jeremiedecock/polytechnique-inf581-2024-teachers
- Moodle: https://moodle.polytechnique.fr/course/view.php?id=17108


## Lab sessions

### Lab session 4: Dynamic Programming

- Open in Google Colab (short link): http://www.jdhp.org/inf581/lab4
- Open in Google Colab: 
- Open in MyBinder: 
- Open in NbViewer: 
- Download the notebook file: 

### Lab session 5: TD Learning, QLearning and SARSA

- Open in Google Colab (short link): http://www.jdhp.org/inf581/lab5
- Open in Google Colab: 
- Open in MyBinder: 
- Open in NbViewer: 
- Download the notebook file: 


## Run INF581 notebooks locally in a dedicated Python virtual environment

### Dependencies

Python required version: Python 3.11.

Python required libraries: c.f. `requirements.txt`

Install Box2D (instructions for Debian like systems):
```bash
sudo apt update
sudo apt install build-essential swig libbox2d2
```

### Installation

#### Posix (Linux, MacOSX, WSL, ...)

From the source code:
```bash
conda deactivate         # Only if you use Anaconda...
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements-jupyter.txt
python3 setup.py develop
```

#### Windows

From the source code:
```bash
conda deactivate         # Only if you use Anaconda...
python3 -m venv env
env\Scripts\activate.bat
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements-jupyter.txt
python3 setup.py develop
```

## Run INF581 notebooks locally in a dedicated Docker container

Run Jupyter Lab from Docker:
```bash
docker run -it --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work jdhp/inf581:latest
```


## Build and run Docker images (for teachers)

Documentation:
- Jupyter's Docker registry: https://quay.io/organization/jupyter
- Jupyter's Docker images:
  - https://quay.io/repository/jupyter/minimal-notebook
  - https://quay.io/repository/jupyter/scipy-notebook
  - https://quay.io/repository/jupyter/datascience-notebook
  - https://quay.io/repository/jupyter/pytorch-notebook
- Jupyter Docker Stacks project: https://github.com/jupyter/docker-stacks
- Jupyter Docker Stacks documentation: https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html
- Selecting the right image: https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-minimal-notebook


### Install Docker

On Debian:

```bash
sudo apt update
sudo apt install docker.io
```

Then add your user to the `docker` group to avoid having to use `sudo`:

```bash
sudo usermod -aG docker $USER
```

See https://docs.docker.com/get-docker/


### Usage example (without mounted volume)

This command pulls the `jupyter/minimal-notebook` image tagged `2024-01-15` from Quay.io if it is not already present on the local host.
It then starts a container running a Jupyter Server with the JupyterLab frontend and exposes the container's internal port `8888` to port `8888` of the host machine:

```bash
docker run -p 8888:8888 quay.io/jupyter/minimal-notebook:2024-01-15
```

You can modify the port on which the container's port is exposed by [changing the value of the `-p` option](https://docs.docker.com/engine/reference/run/#exposed-ports).
For instance, to expose the container's internal port `8888` to port `8889` of the host machine (e.g. if the port `8888` is already used by another service on the host machine),
you can use this command (the `-p` option is used to [expose the container's port](https://docs.docker.com/engine/reference/run/#exposed-ports) to the host machine:

```bash
docker run -p 8889:8888 quay.io/jupyter/minimal-notebook:2024-01-15
```

Visiting `http://localhost:8888/?token=<token>` in a browser loads JupyterLab,
where:

- The `hostname` is the name of the computer running Docker
- The `token` is the secret token printed in the console.

The container remains intact for restart after the Server exits.


### Usage example (with mounted volume)

This command pulls the `jupyter/minimal-notebook` image tagged `2024-01-15` from Quay.io if it is not already present on the local host.
It then starts an _ephemeral_ container running a Jupyter Server with the JupyterLab frontend and exposes the server on host port 8888.

```bash
docker run -it --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work quay.io/jupyter/minimal-notebook:2024-01-15
```

The use of the `-v` flag in the command mounts the current working directory on the host (`${PWD}` in the example command) as `/home/jovyan/work` in the container.
The server logs appear in the terminal.

Visiting `http://localhost:8888/?token=<token>` in a browser loads JupyterLab.

Due to the usage of [the `--rm` flag](https://docs.docker.com/engine/reference/commandline/container_run/#rm)
Docker automatically cleans up the container and removes the file system when the container exits,
but any changes made to the `~/work` directory and its files in the container will remain intact on the host.
[The `-i` flag](https://docs.docker.com/engine/reference/commandline/container_run/#interactive) keeps the container's `STDIN` open, and lets you send input to the container through standard input.
[The `-t` flag](https://docs.docker.com/engine/reference/commandline/container_run/#tty) attaches a pseudo-TTY to the container.

```{note}
By default, [jupyter's root_dir](https://jupyter-server.readthedocs.io/en/latest/other/full-config.html) is `/home/jovyan`.
So, new notebooks will be saved there, unless you change the directory in the file browser.

To change the default directory, you must specify `ServerApp.root_dir` by adding this line to the previous command: `start-notebook.py --ServerApp.root_dir=/home/jovyan/work`.
```

### Usage example (with mounted volume and all dependencies installed)

Build the inf581 Docker image that contains all requirements to run INF581 notebooks:
```bash
docker build -t inf581:latest .
```

Run JupyterLab in this environment:
```bash
docker run -it --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work inf581:latest
```

Push the image on the DockerHub registry:
```bash
docker tag inf581:latest jdhp/inf581:latest
docker login -u jdhp
docker push jdhp/inf581:latest
```

Pull the image from the DockerHub registry:
```bash
docker pull jdhp/inf581:latest
```

Run the image from the DockerHub registry:
```bash
docker run -it --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work jdhp/inf581:latest
```

### Usage example (evaluation system)

```bash
docker build -t inf581-eval:latest -f python.dockerfile .
docker run -v $(pwd):/mnt -it --rm --name python3 inf581-eval:latest bash -c "cd /mnt && python3 lab05_evaluation.py"
```
