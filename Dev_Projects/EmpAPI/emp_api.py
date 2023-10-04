from flask import Flask, jsonify, request
from json import dumps, loads

print('Importing MySQL Connector Module...')
try:
    import mysql.connector as msqlc
except:
    print('Error importing MySQL Connector Module')
    print('Please run the setup.py file first and try again')
    exit(1)
print('Done')
print('Reading connections.json file...')
try:
    f = open('connections.json', 'r')
    conn = loads(f.read())
    mysql_host = conn['mysql_host']
    mysql_user = conn['mysql_user']
    mysql_pass = conn['mysql_pass']
    mysql_db = conn['mysql_db']
    mysql_table = conn['mysql_table']
    f.close()
except:
    print('Error reading connections.json file')
    print('Please run the setup.py file first and try again')
    exit(1)
print('Done')

print('Connecting to MySQL database...')
db = msqlc.connect(host=mysql_host, user=mysql_user, password=mysql_pass, database=mysql_db)
db_cursor = db.cursor()
print('Done')

print('Launching Flask app')
app = Flask(__name__)

# TODO:
# 1. Add string checks and cleanup to avoid SQL injection
# 2. Cleanup code to avoid code duplication

@app.route('/api/create_emp', methods=['POST'])
def create_emp():
    data = request.get_json()
    if any(key not in data.keys() for key in ['id', 'name', 'salary']):
        return {'Error': 'Invalid JSON keys. Please use "id", "name" and "salary" keys for the employee data'}
    
    id = data['id']
    name = data['name']
    salary = data['salary']

    req = f'INSERT INTO {mysql_table} (id, name, salary) VALUES (%s, %s, %s)'
    val = (id, name, salary)
    db_cursor.execute(req, val)
    db.commit()

    return {'Success': f'Employee with ID {id} created successfully'}

@app.route('/api/view_emps', methods=['GET'])
def view_emps():
    emp_data = {}
    
    req = f'SELECT * FROM {mysql_table}'

    db_cursor.execute(req)
    result = db_cursor.fetchall()
    if result == []:
        return {'Error': 'No employees found'}
    
    else:
        for r in result:
            emp_data[f'{r[0]}'] =  {'id': r[0], 'name': r[1], 'salary': r[2]}

        return emp_data

@app.route('/api/view_emp/<emp_id>', methods=['GET'])
def view_emp(emp_id):
    emp_data = {}
    
    req = f'SELECT * FROM {mysql_table} WHERE id = %s'
    val = (emp_id,)
    db_cursor.execute(req, val)
    result = db_cursor.fetchall()
    for r in result:
        emp_data[f'{emp_id}'] = {'id': r[0], 'name': r[1], 'salary': r[2]}
    
    if emp_data == {}:
        return {'Error': 'No employee found with the given ID'}
    else:
        return emp_data

@app.route('/api/update_emp/<emp_id>', methods=['POST'])
def update_emp(emp_id):
    data = request.get_json()

    req = f'SELECT * FROM {mysql_table} where id = %s'
    val = (emp_id,)

    db_cursor.execute(req, val)
    result = db_cursor.fetchall()
    if result == []:
        return {'Error': 'No employee found with the given ID'}

    if 'name' in data.keys():
        req = f'UPDATE {mysql_table} SET name = %s WHERE id = %s'
        val = (data['name'], emp_id)
        db_cursor.execute(req, val)
        db.commit()
        
    if 'salary' in data.keys():
        req = f'UPDATE {mysql_table} SET salary = %s WHERE id = %s'
        val = (data['salary'], emp_id)
        db_cursor.execute(req, val)
        db.commit()
        
    return {'Success': f'Employee with ID {emp_id} updated successfully'}

@app.route('/api/delete_emp/<emp_id>', methods=['GET'])
def delete_emp(emp_id):
    req = f'SELECT * FROM {mysql_table} where id = %s'
    val = (emp_id,)

    db_cursor.execute(req, val)
    result = db_cursor.fetchall()
    if result == []:
        return {'Error': 'No employee found with the given ID'}
    
    req = f'DELETE FROM {mysql_table} WHERE id = %s'
    val = (emp_id,)
    db_cursor.execute(req, val)
    db.commit()

    return {'Success': f'Employee with ID {emp_id} deleted successfully'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)