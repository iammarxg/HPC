# HPC
This is a repository to document my work during summer training at the High Performance Computing Center.

To start using any of the python files, please make sure to install the required packages using:

```python
pip install -r requirements.txt
```

Then run any Task*.py file with python.


## Docker

Build Task 1 from Week 1 Day 2 with Docker:

```
docker build -t hpc-w1d2-t1 .
```

Run the container:

```
docker run -it -p 9000:6000 --rm --env-file .env hpc-w1d2-t1
```