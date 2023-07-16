# The Dynamic District Information Management Server
The DDIM Server is a Django/Neo4J based server that provides connectivity for front end software to create homogonous knowledge graphs from heterogenous data sources such as
CSV files, existing graphs and other data sources. The server provides an API to follow a procedure for uploading and creating semantic relationships between these diverse data
sources. Using the ontology entities are created and related to one another.

## Methodology
The graph is created using the following step (assumes running server).
1. Upload CSV Files – files are uploaded to the server. These are parsed and column headers are parsed and recorded. This serves three purposes
- Its allows for knowledge discovery through the identification of data sources, as well as a description of the attributes that make these up. These can be
queried via the API to populate a user interface to inform users of the system;
- It informs the following steps of graph creation by allowing connections to be made between entities according to the aforementioned ontology.
- Under the hood, Neo4J load/create/merge commands are issued to represent the data. Each CSV row represents a new entity in the graph.
- Files are accessed using the create/files RESTFUL API. Individual files are manipulated using the create/files/&lt;fileid&gt; RESTFUL API.

File meta data (lists of attributes to enable further data discovery beyond data sources available) are accessed through the create/filemeta RESTFUL API.

2. Create Connection Rules – connection rules are used to define one of three relationships between entities created in step 1. These are
- Equivilant to – where two entities are considered to relate to the same real world entity.
- Contains – where entity A is a child of entity B in a hierarchical relationship. Entity A can have many children.
- Contained-by – the inverse relationship of Contains (not created as Neo4J relationships are bi-directional).
- isa – used to relate data to classes – e.g. archetype data related to an entity.
- hasa – used to relate an entity to other data sources that provide futher descriptions.

These relationships are created using the create/createrule/ RESTFUL API which accepts standard HTTP requests to GET and POST to the type. create/createrule/<ruleid>;  is used to access individual rules.

3. Rules are created by posting to the aforementioned API. The call takes 5 parameters
- relationship – one of ‘equalto’, ‘contains’, ‘contained’, ‘isa’ and ‘hasa’
- filename1 and filename2 – filename of datasource uploaded earlier. NOTE: THIS IS A MISNOMER AND IS LISTED AS A BUG TO BE FIXED. THE ATTRIBUTE PROVIDED IS
THE FILE ID RATHER THAN THE FILENAME.
- joincolumn1 and joincolumn2 – the names of columns across which equivalence or other relationship is defined.

## Python Enviornment 
Package Version
------------------- ---------
- asgiref 3.4.1
- beautifulsoup4 4.10.0
- bootstrap4 0.1.0 
- certifi 2021.5.30
- cffi 1.14.6 
- charset-normalizer 2.0.6 
- cryptography 3.4.8 
- Django 3.2.7 
- django-bootstrap4 3.0.1
- djangorestframework 3.12.4
- idna 3.2
- importlib-metadata 2.1.1
- mysqlclient 2.0.3
- neo4j 4.4.3
- numpy 1.21.2
- pandas 1.3.3
- pip 21.0.1
- pycparser 2.20
- PyMySQL 1.0.2
- python-dateutil 2.8.2
- pytz 2021.1
- requests 2.26.0
- setuptools 58.0.4
- six 1.16.0
- soupsieve 2.2.1
- sqlparse 0.4.2
- typing-extensions 3.10.0.2
- urllib3 1.26.6
- wheel 0.37.0
- zipp 3.5.0

## Other Software
As well as Python (3.7.11 is currently used via an Anaconda setup), MySQL (Server version 8.0.23) and Neo4J (latest – connections via HTTP services) must 
also be installed.

Note comments on setup.py file adjustments to ensure connection to these packages.
