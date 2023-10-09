# python-firebase-export-rtdb-storage  
A simple Python program to export current date's data from realtime database and download images from specific bucket from firebase storage.  
---
There is the script file `main.py` containing all the code for the program to run, inside the `src` folder there are the files to configure and get the `urls` and Service Account Keys required to access each firebase project, also there is a file named `clientes.txt` which is a text file containing the "key" or "identifier" for each project, at last but not least, there must contain the service account key json file for each project, the file name must follow this format: `SAK-{'key/id'}` the key/id being the same as you configured in `clientes.txt`.  
## Using the program
The script initially creates a small menu screen containing a select-box and a button for the user to choose wich project they want to export data from.  
### clientes.txt
The content of this file must follow the pattern '`id`\n`id`\n...':
```
project-id-1
project-id-2
...
``` 
main.py will read this file and split the content into lines and list then as options for the select-box.
### rtdb-urls.txt & bucket-urls.txt
As the name sugests it contains the urls for each realtime database (rtdb) / bucket and the key to identify based on the chosen option by the user separated by a single blank space, each project being separated by \n: 
#### rtdb:
```
project-id-1 https://project-1.firebaseio.com
project-id-2 https://project-2.firebaseio.com
...
```
#### storage:
```
project-id-1 project-1.appspot.com
project-id-2 project-2.appspot.com
...
```
by doing so each line will be separated by the blank space between the key and the value of the url
### SAK-{key/id}
The service account key can be downloaded from Project Settings > Service accounts > *select Python > Generate new private key, it must look more or less like this:
```
{
    "type": "service_account",
    "project_id": "project-1",
    "private_key_id": "abc123xyz789",
    ...
}
```
note that you must change the name of the file in order for it to work.
