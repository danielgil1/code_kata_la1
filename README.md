# MyParser

## Installing and Running
The easiest way to run the app is using [docker](https://docs.docker.com/get-docker/). Once docker is available run in command line:  
* Run using docker compose:
```
docker-compose up -d
```
The output is automatically available through a bind mount on `output` folder. In addition, you can see the logs:
```
docker logs code_kata_la1
```

* Run using individual container, here you will need to bind mount according to your operating system if needed:
```
# build the image
docker build --tag parser:latest . 

# run the container. For unix based OS add `-v $(pwd)/output:/workdir/output` if you want to extract the output at host
docker run --rm -it parser:latest python run.py -s spec.json
```

Use python run.py -h to see other options available:
```
docker run --rm -it parser:latest python run.py -h
usage: run.py [-h] -s SPEC [-d DELIMITER] [-n NUMLINES]

optional arguments:
  -h, --help            show this help message and exit
  -s SPEC, --spec SPEC  Specs
  -d DELIMITER, --delimiter DELIMITER
                        Delimiter
  -n NUMLINES, --numlines NUMLINES
                        Number of lines in file
```

## Running tests
Tests will be loaded automatically using `pytest`. Run from command line
```
docker run --rm -it parser:latest pytest
```

# More info and documentation
Find additional documentation in [docs](build/html/index.html)

