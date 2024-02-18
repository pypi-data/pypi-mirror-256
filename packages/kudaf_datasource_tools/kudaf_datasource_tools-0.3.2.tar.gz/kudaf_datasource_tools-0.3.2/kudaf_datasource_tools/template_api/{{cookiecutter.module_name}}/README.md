# KUDAF Datasource API

This package is Python FastAPI **Datasource back-end** developed to enable a **Data Producer to make small-file data available on the KUDAF data-sharing platform**.    

This REST API has the following **endpoints**: 
- `api/metadata/variables` : Outputs KUDAF JSON **Variables Metadata** for this Datasource.  
1. `api/variables/:variable_name` : Stream-downloads a **CSV file** corresponding to the requested **KUDAF Variable** data.   

---

## About KUDAF

(Summary info and links for the Kudaf initiative)

--- 

## High-level workflow for Data Source administrators

(Summary of the process for Datasource admins to make their data available in KUDAF, and where this Datasource back-end fits in that journey)

--- 

## Local API installation and launch instructions (Linux/Mac)  

Navigate to the folder containing this generated API:

\$ `cd /home/me/path/to/api/folder` 

### Create a Python virtual environment and activate it  

\$ `python3 -m venv .venv` 

This created the virtualenv under the hidden folder `.venv`  

Activate it with: 

\$ `source .venv/bin/activate`  

### Install needed Python packages 

\$ `pip install -r requirements.txt` 

### Launch the Kudaf Datasource API 

\$ `uvicorn app.main:app` 

### Browser: Navigate to the the API's interactive documentation at: 

**`http://localhost:8000/docs`** 

---

## Docker API launch (Linux)

### Install Docker for your desktop 

Follow instructions for your desktop model at `https://docs.docker.com/desktop/`  

### Navigate to the folder containing this generated API:

\$ `cd /home/me/path/to/api/folder`

### Create a Docker image 

\$ **`sudo docker build -t my-kudaf-datasource-image .`**  

(Note: The **last `.`** in the above command is important! Make sure it's entered like that )

### Create and launch a Docker container for the generated image 

\$ **`sudo docker run -d --name my-kudaf-datasource-container -p 9000:8000 my-kudaf-datasource-image`**  


### Browser: Navigate to the the API's interactive documentation at: 

**`http://localhost:9000/docs`**  


---