# Structure of overall APP 

discovery01_blog
==app
====(blueprint) auth : Admin user to write blog
====(blueprint) public : What public see
====(flask_tool) static
====(flask_tool) template
======(blueprint) auth HTMLs
======(blueprint) public HTMLs
======email
====__init__
====decorators.py
====email.py
====(FOLDER) model 
==pipfile
==migrations
==tests
==config.py







