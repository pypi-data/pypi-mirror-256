def print_table(table_data:list):
    print("+------+-----------------+-----------+")
    print("| SNO  | Columnn Name    | Data Type |")
    print("+------+-----------------+-----------+")
    for id, data in enumerate(table_data):
        print(f"|  {str(id+1)}{' '*(4 -int(len(str(id))))}| {data[0]}{' '*(16 -int(len(str(data[0]))))}| {data[1]}{' '*(10 -int(len(str(data[1]))))}|")
    print("+------+-----------------+-----------+")


def getDtype(obj):
    if isinstance(obj, str):
        return "STRING"
    elif isinstance(obj, bool):
        return "BOOL"
    elif isinstance(obj, int):
        return "INTEGER"
    elif isinstance(obj, float):
        return "FLOAT"
    else:
        return False