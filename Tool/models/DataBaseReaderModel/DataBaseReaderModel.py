
from flask import render_template
from Tool import CONSTANTS
from Tool.models.DataBaseReaderModel import DataBaseReaderManager as DBManager


def index(args):
    pathFile = args.get('db')
    fullPath = f'{CONSTANTS.path}{pathFile}'
    dbName = pathFile.split('/')[-1]

    db_tables = DBManager.get_tables(path_db=fullPath)

    tableSelected = args.get('table')
    get_tableColumns = None
    get_tableData = None
    get_primary_key_columns = []

    if (tableSelected is None):
        tableSelected = ''
    else:
        get_tableColumns = DBManager.get_tableColumns(path_db=fullPath, table=tableSelected)
        print(get_tableColumns)
        for column in get_tableColumns:
            if column[5] == 1:
                get_primary_key_columns.append(column)
        print(get_primary_key_columns)
        get_tableData = DBManager.get_tableData(path_db=fullPath, table=tableSelected)
        print(get_tableData)

    #return data
    return render_template(
        'pages/databasereader/databasereader.html',
        tables=db_tables,
        pathFile=pathFile,
        dbName=dbName,
        tableSelected=tableSelected,
        tableColumns=get_tableColumns,
        tableData=get_tableData,
        primary_keys=get_primary_key_columns,
    )
