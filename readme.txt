

I have not tried using the environment.yml, but when I did this this morning there was somethign about opencv, I could only get this to work with a python2. If your installation of anaconda is python 3 it may be necessary to install the ipython kernal in your python2 environment:
conda install notebook ipykernel
ipython kernel install --user