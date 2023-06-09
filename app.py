from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Route to handle the API call for fetching project data
@app.route('/api/project')
def fetch_project_data():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()

        # Execute the query to retrieve the project data from the database
        cursor.execute('SELECT * FROM projects')
        project_data = cursor.fetchone()

        # Close the database connection
        cursor.close()
        conn.close()

        # Transform the fetched data into a dictionary
        project_dict = {
            'title': project_data[0],
            'description': project_data[1],
            'skills': project_data[2]
        }

        return jsonify(project_dict)

    except Exception as e:
        print('Error fetching project data:', str(e))
        return jsonify({'error': 'Failed to fetch project data'})

if __name__ == '__main__':
    app.run()
