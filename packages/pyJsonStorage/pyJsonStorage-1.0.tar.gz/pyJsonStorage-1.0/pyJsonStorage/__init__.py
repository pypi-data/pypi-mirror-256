import json
from package import *

class pyJsonStorage:
    """
    ## pyJsonStorage
    pyJsonStorage is a Python package designed to implement basic database functionalities using JSON (JavaScript Object Notation). This package provides various features such as creating a new database, inserting rows, updating, and deleting rows. It leverages the JSON module from Python's core libraries for managing JSON files.

    ### Features:

    - Database Creation:      Easily create new databases using JSON files.
    - Row Operations:         Perform operations like inserting, updating, and deleting rows within the database.
    - JSON Integration:       Utilize the JSON module for seamless management of JSON files.
    - Schema Management:      Define and manage schemas for structured data storage.
    - Querying:               Retrieve data from the database using custom queries.
    - Error Handling:         Implement robust error handling mechanisms for data integrity and consistency.
    - Concurrency Control:    Manage concurrent access to the database to prevent data corruption. 
    """
    def __init__(self, filePath:str, intent:int = 4):
        """Initialize the pyJsonStorage object.

        Parameters:
        - filePath (str): File path of json file, If not exist then create new.
        - intent (int): intent level for json, by default 4.
        """
        self.model = None
        self.filePath = filePath
        self.intent = intent
        self.available_dtype = ["STRING", "INTEGER", "BOOL", "FLOAT"]
        try:
            with open(self.filePath, 'r') as model:
                self.model = json.load(model)
        except(FileNotFoundError):
            with open(self.filePath, 'w') as model:
                json.dump({}, model, indent=self.intent)
        self.model = json.load(open(self.filePath, 'r+'))
    # Commit
    def save(self):
        """
    This method is used to save the changes made to the database.

    ### Returns:
    - bool: Returns True if the changes were successfully saved, otherwise False.
        """
        with open(self.filePath, 'w') as model:
            json.dump(self.model, model, indent=self.intent)
        return True
    # Create Table with Schema
    def createTable(self, tableName:str, tableSchema:dict):
        """
    This method is used to create a new table in the database with the specified table name and schema.

    ### Parameters:
    - tableName (str): The name of the table to be created.
    - tableSchema (dict): A dictionary defining the schema of the table where keys are column names and values are data types.
    
    ### Example:
    - tableSchema = {"COLUMN_NAME": "DATATYPE", "COLUMN_NAME1": "DATATYPE"}

    ### Returns:
    - str: A status message indicating the result of the table creation along with the count of columns.
        """
        tableValidSchema ={"<TABLE_SCHEMA>":{"OBJECT_ID":"INTEGER"}}
        for schema, dtype in tableSchema.items():
            if dtype in self.available_dtype:
                tableValidSchema["<TABLE_SCHEMA>"][schema]=dtype
            else:
                print(f"Dtype error: {dtype} is not valid data type.")
                break

        self.model[tableName] = tableValidSchema
        self.model[tableName]["<TABLE_ROW>"] = []
        return f"Change applied: {len(tableValidSchema)-1} column added."
    # insertRow
    def insertRow(self, tableName:str, rows:list):
        """
    This method is used to insert rows into a table while validating the data types set for each column.

    ### Parameters:
    - tableName (str): The name of the table in which the rows will be inserted.
    - rows (list): A list of lists containing data for each row, where the inner lists represent the data for each column indexed accordingly.
    
    ### Example:
    - rows = [["Example Name", "Example Address"],["Example Name", "Example Address"]]

    ### Returns:
    - str: A status message indicating the result of the row insertion along with the count, or an error message if insertion fails.
        """
        try:

            self.model[tableName]["<TABLE_ROW>"]
            columnDtype = [dtype for dtype in self.model[tableName]["<TABLE_SCHEMA>"].values()]
            columnName = [dtype for dtype in self.model[tableName]["<TABLE_SCHEMA>"].keys()]
            insertedRow = 0
            for indx, row in enumerate(rows):
                validRow =  True
                OBJECT_ID = len(self.model[tableName]["<TABLE_ROW>"]) + 1
                row.insert(0, OBJECT_ID)

                for index, data in enumerate(row):

                    if getDtype(data) !=  columnDtype[index]:
                        print(f"Dtype error: at {indx} '{data}' is not valid data type for column '{columnName[index]}'.")
                        validRow = False
                        break

                if validRow:
                    self.model[tableName]["<TABLE_ROW>"].append(row)
                    insertedRow +=1
            return f"Change applied: {insertedRow} row inserted."
        except(KeyError):
            print(f"Entry error: '{tableName}' named table not found.")
            return None
    # FetchOne Row
    def fetchOne(self, filter:tuple, tableName:str, field:list=[]):
        """
    This method fetches one row from the table based on the specified filters and returns only the specified columns.

    ### Parameters:
    - filter (tuple): A tuple representing the filter condition. The first element is the column name, and the second element is a list of values to filter.
    - tableName (str): The name of the table from which to fetch the row.
    - field (list): A list of column names to be included in the fetched row. Leave it empty to include all columns.

    ### Example:
    - filter = ("OBJECT_ID", [1])
    - field = ["COLUMN", "COLUMN2"]

    ### Returns:
    - list: A list of dictionaries representing the rows that satisfy the filter condition, containing only the specified columns. Returns an error if the operation fails.
        """
        try:
            row = self.model[tableName]["<TABLE_ROW>"]
            columnName = [dtype for dtype in self.model[tableName]["<TABLE_SCHEMA>"].keys()]
            field = columnName if len(field) == 0 else field
            resultRow = []
            if filter[0] in columnName:
                for index, elemt in enumerate(row):
                    if elemt[columnName.index(filter[0])] in list(filter[1]):
                        tempData = {}
                        for indx, data in enumerate(elemt):
                            if columnName[indx] in field:
                                tempData[columnName[indx]]=data
                        resultRow.append(tempData)
            return resultRow
        except(KeyError):
            print(f"Entry error: '{tableName}' named table not found.")
            return None
    # FetchAll Row
    def fetchAll(self, tableName:str,field:list=[]):
        """
    This method fetches all row from the table based on the specified field and returns only the specified columns.

    ### Parameters:
    - tableName (str): The name of the table from which to fetch the row.
    - field (list): A list of column names to be included in the fetched row. Leave it empty to include all columns.

    ### Example:
    - field = ["COLUMN", "COLUMN2"]

    ### Returns:
    - list: A list of dictionaries representing the rows that satisfy the filter condition, containing only the specified columns. Returns an error if the operation fails.
        """
        try:
            row = self.model[tableName]["<TABLE_ROW>"]
            columnName = [dtype for dtype in self.model[tableName]["<TABLE_SCHEMA>"].keys()]
            field = columnName if len(field) == 0 else field
            resultRow = []
            for data in row:
                tempData = {}
                for indx, data in enumerate(data):
                    if columnName[indx] in field:
                        tempData[columnName[indx]]=data
                resultRow.append(tempData)
            return resultRow
        except(KeyError):
            print(f"Entry error: '{tableName}' named table not found.")
            return None
    # DeleteOne
    def deleteOne(self, filter:tuple, tableName:str, commit:bool=False):
        """
    This method removes or deletes one rows from the table based on the specified filter conditions.

    ### Parameters:
    - filter (tuple): A tuple representing the filter condition. The first element is the column name, and the second element is the value to filter.
    - tableName (str): The name of the table from which to remove the rows.
    - commit (bool): If True, the changes will be saved to the JSON file. Default is False.

    ### Example:
    - filter = ("COLUMN_NAME","COLUMN_VALUE")
        
    ### Returns:
    - str: A status message indicating the result of the operation and the count of the removed rows.
    """
        try:
            row = self.model[tableName]["<TABLE_ROW>"]
            columnName = [dtype for dtype in self.model[tableName]["<TABLE_SCHEMA>"].keys()]
            deletedRow = 0
            if filter[0] in columnName:
                for index, elemt in enumerate(row):
                    if elemt[columnName.index(filter[0])] == filter[1]:
                        self.model[tableName]["<TABLE_ROW>"].pop(index)
                        deletedRow += 1
            self.save() if commit else ""
            return f"Change applied: {deletedRow} column deleted."
        except(KeyError):
            print(f"Entry error: '{tableName}' named table not found.")
            return None
    # DeleteMany
    def deleteMany(self, filter:tuple, tableName:str, commit:bool=False):
        """
    This method removes or deletes multiple rows from the table based on the specified filter conditions.

    ### Parameters:
    - filter (tuple): A tuple representing the filter condition. The first element is the column name, and the second element is a list containing multiple values to filter.
    - tableName (str): The name of the table from which to remove the rows.
    - commit (bool): If True, the changes will be saved to the JSON file. Default is False.

    ### Example:
    - filter = ("COLUMN_NAME",["COLUMN_VALUE1","COLUMN_VALUE2"])
        
    ### Returns:
    - str: A status message indicating the result of the operation and the count of the removed rows.
    """
        try:
            row = self.model[tableName]["<TABLE_ROW>"]
            columnName = [dtype for dtype in self.model[tableName]["<TABLE_SCHEMA>"].keys()]
            deletedRow = 0
            if filter[0] in columnName:
                for index, elemt in enumerate(row):
                    if elemt[columnName.index(filter[0])] in filter[1]:
                        self.model[tableName]["<TABLE_ROW>"].pop(index)
                        deletedRow += 1
            self.save() if commit else ""
            return f"Change applied: {deletedRow} column deleted."
        except(KeyError):
            print(f"Entry error: '{tableName}' named table not found.")
            return None
    # UpdateOne
    def updateOne(self, filter:tuple, newData:dict, tableName:str,commit:bool=False):
        """This method is used for update one row data with new value and their desires datatypes and column index

        ### Parameters:
        - filter (tuple): A tuple representing the filter condition. The first element is the column name, and the second element is a list containing multiple values to filter.
        - newData (dict): A dictinaory containing new value with column name as key and new value as value of key pair,
        - tableName (str): The name of the table from which to remove the rows.
        - commit (bool): If True, the changes will be saved to the JSON file. Default is False.
        
        ### Example:
        - newData = {"COLUMN_NAME":"COLUMN_VALUE"}
        - filter = ("COLUMN_NAME","COLUMN_VALUE")
        ### Returns:
        - str: A status message indicating the result of the operation and the count of the updated rows.
        """
        ("name","Sachin Shrivastav")
        {
            "name":"New Name",
            "email":"newemail@gmail.com"
        }
        try:
            row = self.model[tableName]["<TABLE_ROW>"]
            columnName = [dtype for dtype in self.model[tableName]["<TABLE_SCHEMA>"].keys()]
            columnDtype = [dtype for dtype in self.model[tableName]["<TABLE_SCHEMA>"].values()]
            updatedRow = []
            rowCount = 0
            for keys, value in newData.items():
                if keys not in columnName:
                    print(f"Entry error: '{keys}' named column not found.")
                    return None
            if filter[0] not in columnName:
                print(f"Entry error: '{filter[0]}' named column not found.")
                return None
            for index, data in enumerate(row):
                if data[columnName.index(filter[0])] == filter[1]:
                    rowCount +=1
                    validRow = True
                    for key, value in newData.items():
                        if getDtype(value) != columnDtype[columnName.index(key)]:
                            print(f"Dtype error: at '{key}' in new data '{value}' is not valid data type for column '{columnName[columnName.index(key)]}'.")
                            validRow = False
                            break
                    if validRow:
                        for key, value in newData.items():
                            data[columnName.index(key)] = value
                        updatedRow.append(data)
                        self.model[tableName]["<TABLE_ROW>"].pop(index)
                    break
                return None
            self.model[tableName]["<TABLE_ROW>"].extend(updatedRow)
            self.save() if commit else ""
            return f"Change applied: {rowCount} column updated."
        except(KeyError):
            print(f"Entry error: '{tableName}' named table not found.")
            return None