# CS170Project

CS170 Project UC Berkeley Computer Science 2018.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.   

### Prerequisites

```
pip install simanneal  # from pypi

pip install git+https://github.com/perrygeo/simanneal.git    
  
pip install networkx  
```

### Running input generator  
Run input_generator.py Note it will override existing graphs.   

```
python input_generator.py 
```

### Running the solver code:  
Note: you will to create a local file myfolder.py which needs to have a variable named folder which contains a variable folder = "MY_FOLDER_NAME_HERE".
#### Example:
```
touch myfolder.py 
mkdirs MY_FOLDER_NAME_HERE  
mkdir -p MY_FOLDER_NAME_HERE/{small,medium,large}
```  
Inside of the file write:  
> folder = "ian"
  
To actually run the solver in one the three modes:
```
python solver.py [solves all inputs]
```
```
python solver.py file_size [solves either small/medium/large depending on file_size]
```
```
python solver.py file_name [solves a specific file]
```
### Before committing:  
You should run output_merger.py which will merge your local folder so we always have the best outputs in outputs folder.
```
python output_merger.py
```
Make sure to add all the new files in outputs to your commit!
