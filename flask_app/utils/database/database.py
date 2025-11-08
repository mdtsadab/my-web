import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import datetime

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'

    def query(self, query = "SELECT CURDATE()", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def about(self, nested=False):    
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info



    def createTables(self, purge=False, data_path='flask_app/database/'):
        print('I create and populate database tables.')
        
        # If purge is True, drop all tables first (in reverse order due to foreign keys)
        if purge:
            print('Purging existing tables...')
            tables = ['skills', 'experiences', 'feedback', 'positions', 'institutions']
            for table in tables:
                try:
                    self.query(f'DROP TABLE IF EXISTS {table}')
                except Exception as e:
                    print(f"Warning dropping {table}: {e}")
        
        # Define the order of table creation based on dependencies
        table_order = ['institutions', 'positions', 'experiences', 'skills', 'feedback']
        
        # Execute each SQL file in the correct order
        for table_name in table_order:
            sql_file = f'{data_path}create_tables/{table_name}.sql'
            print(f'Creating table from {sql_file}')
            try:
                # Read file with explicit encoding and error handling
                with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
                    sql_script = f.read()
                    if sql_script.strip():  # Only execute if file has content
                        self.query(sql_script)
            except FileNotFoundError:
                print(f"SQL file not found: {sql_file}")
            except Exception as e:
                print(f"Error creating table {table_name}: {e}")
                # Continue anyway - table might already exist
        
        # Get CSV files and load them in the same order
        for table_name in table_order:
            csv_file = f'{data_path}initial_data/{table_name}.csv'
            try:
                print(f'Loading data from {csv_file}')
                
                # Read CSV file with explicit encoding
                with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                    csv_reader = csv.DictReader(f)
                    rows = list(csv_reader)
                    
                    if len(rows) > 0:
                        # Get column names from CSV header
                        columns = list(rows[0].keys())
                        
                        # Prepare data for insertion
                        data = []
                        for row in rows:
                            row_data = [row[col] if row[col] not in ['NULL', 'None', ''] else None for col in columns]
                            data.append(row_data)
                        
                        # Insert data into table
                        self.insertRows(table=table_name, columns=columns, parameters=data)
            except FileNotFoundError:
                print(f'No data file found for {table_name}, skipping...')
            except Exception as e:
                print(f'Error loading data for {table_name}: {e}')
        
        print('Database tables created and populated successfully!')


    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        print(f'Inserting {len(parameters)} rows into {table}')
        
        # Build the INSERT query
        columns_str = ', '.join([f'`{col}`' for col in columns])
        placeholders = ', '.join(['%s'] * len(columns))
        
        query = f'INSERT INTO {table} ({columns_str}) VALUES ({placeholders})'
        
        # Insert each row
        for row in parameters:
            try:
                self.query(query, row)
            except Exception as e:
                print(f'Error inserting row into {table}: {e}')
                print(f'Row data: {row}')


    def getResumeData(self):
        # Query to get all institutions with their positions, experiences, and skills
        query = '''
            SELECT 
                i.inst_id,
                i.type,
                i.name as inst_name,
                i.department,
                i.address,
                i.city,
                i.state,
                i.zip,
                p.position_id,
                p.title,
                p.responsibilities,
                p.start_date as pos_start_date,
                p.end_date as pos_end_date,
                e.experience_id,
                e.name as exp_name,
                e.description as exp_description,
                e.hyperlink,
                e.start_date as exp_start_date,
                e.end_date as exp_end_date,
                s.skill_id,
                s.name as skill_name,
                s.skill_level
            FROM institutions i
            LEFT JOIN positions p ON i.inst_id = p.inst_id
            LEFT JOIN experiences e ON p.position_id = e.position_id
            LEFT JOIN skills s ON e.experience_id = s.experience_id
            ORDER BY i.inst_id, p.position_id, e.experience_id, s.skill_id
        '''
        
        results = self.query(query)
        
        # Build nested dictionary structure
        resume_data = {}
        
        for row in results:
            inst_id = row['inst_id']
            
            # Add institution if not exists
            if inst_id not in resume_data:
                resume_data[inst_id] = {
                    'address': row['address'],
                    'city': row['city'],
                    'state': row['state'],
                    'type': row['type'],
                    'zip': row['zip'],
                    'department': row['department'],
                    'name': row['inst_name'],
                    'positions': {}
                }
            
            # Add position if exists and not already added
            if row['position_id'] and row['position_id'] not in resume_data[inst_id]['positions']:
                resume_data[inst_id]['positions'][row['position_id']] = {
                    'title': row['title'],
                    'responsibilities': row['responsibilities'],
                    'start_date': row['pos_start_date'],
                    'end_date': row['pos_end_date'],
                    'experiences': {}
                }
            
            # Add experience if exists and not already added
            if row['experience_id'] and row['position_id']:
                if row['experience_id'] not in resume_data[inst_id]['positions'][row['position_id']]['experiences']:
                    resume_data[inst_id]['positions'][row['position_id']]['experiences'][row['experience_id']] = {
                        'name': row['exp_name'],
                        'description': row['exp_description'],
                        'hyperlink': row['hyperlink'],
                        'start_date': row['exp_start_date'],
                        'end_date': row['exp_end_date'],
                        'skills': {}
                    }
            
            # Add skill if exists
            if row['skill_id'] and row['experience_id'] and row['position_id']:
                resume_data[inst_id]['positions'][row['position_id']]['experiences'][row['experience_id']]['skills'][row['skill_id']] = {
                    'name': row['skill_name'],
                    'skill_level': row['skill_level']
                }
        
        return resume_data