# webneuron
A web-interface for running Python-NEURON models in a server backend. Built with flask. This is meant for remote teaching, absolutely not for heavy simulations.

This is at the moment running on the development server of flask, NOT for production or public environment. DO NOT EXPOSE TO THE internet if you do not know what you are doing. Learn about deploying flask-applications here: https://flask.palletsprojects.com/en/1.1.x/deploying/

This is a first demo only. Future updates will hopefully increase the usability (i.e. panning and zooming etc), the design (nicer forms would be nicer...), maintainability (template system to generate experiments without "programming" knowledge??) and security.

At the moment it is labeled in german, but I am also working on getting a „multi-language“ thing going. Sorry.

Here is how I think you should be able to run it (Linux only, sorry, I have no idea whether this can run as is on windows, although flask should be available there as well)

1) download repo

2) create a virtual environment: python3 -m venv webneuron_venv

3) activate the virtual environment (source webneuron_venv/bin/activate)

4) cd into the repo

5) pip install -r requirements.txt

6) start the flask development webserver:

 export FLASK_APP=webneuron.py

 python -m flask run

7) go to 127.0.0.1:5000 and hopefully enjoy!


Shoot me an email if you actually use it, want to contribute or have any questions.
Good luck!
Thomas
