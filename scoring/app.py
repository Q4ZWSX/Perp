import sqlite3
from flask import Flask, g, render_template, request

app = Flask(__name__, template_folder='/app/templates')

# Database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('/app/database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

# Initialize database
def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS teams
                  (team_name TEXT PRIMARY KEY, password TEXT, points INTEGER)''')
    db.execute('''CREATE TABLE IF NOT EXISTS flags
                  (machine TEXT, location TEXT, flag TEXT,
                   PRIMARY KEY (machine, location))''')
    # New table to track submitted flags
    db.execute('''CREATE TABLE IF NOT EXISTS submitted_flags
                  (team_name TEXT, flag TEXT,
                   PRIMARY KEY (team_name, flag),
                   FOREIGN KEY (team_name) REFERENCES teams(team_name))''')
    
    machines = ['172.30.1.11', '172.30.1.12', '172.30.1.13', '172.30.1.15', '172.30.1.21', '172.30.1.22', '172.30.1.23', '172.30.1.25', '172.30.1.31', '172.30.1.32', '172.30.1.33', '172.30.1.35', '172.30.1.41', '172.30.1.42', '172.30.1.43', '172.30.1.45', '172.30.1.51', '172.30.1.52', '172.30.1.53', '172.30.1.55', '172.30.1.61', '172.30.1.62', '172.30.1.63', '172.30.1.65', '172.30.1.71', '172.30.1.72', '172.30.1.73', '172.30.1.75', '172.30.1.81', '172.30.1.82', '172.30.1.83', '172.30.1.85', '172.30.1.91', '172.30.1.92', '172.30.1.93', '172.30.1.95', '172.30.1.101', '172.30.1.102', '172.30.1.103', '172.30.1.105', '172.30.1.111', '172.30.1.112', '172.30.1.113', '172.30.1.115', '172.30.1.121', '172.30.1.122', '172.30.1.123', '172.30.1.125', '172.30.1.131', '172.30.1.132', '172.30.1.133', '172.30.1.135', '172.30.1.141', '172.30.1.142', '172.30.1.143', '172.30.1.145', '172.30.1.151', '172.30.1.152', '172.30.1.153', '172.30.1.155', '172.30.1.161', '172.30.1.162', '172.30.1.163', '172.30.1.165', '172.30.1.171', '172.30.1.172', '172.30.1.173', '172.30.1.175', '172.30.1.181', '172.30.1.182', '172.30.1.183', '172.30.1.185', '172.30.1.191', '172.30.1.192', '172.30.1.193', '172.30.1.195', '172.30.1.201', '172.30.1.202', '172.30.1.203', '172.30.1.205', '172.30.1.211', '172.30.1.212', '172.30.1.213', '172.30.1.215', '172.30.1.221', '172.30.1.222', '172.30.1.223', '172.30.1.225', '172.30.1.231', '172.30.1.232', '172.30.1.233', '172.30.1.235']
    locations = ['/tmp/flag.txt', '/root/flag.txt']
    for machine in machines:
        for location in locations:
            db.execute("INSERT OR IGNORE INTO flags (machine, location, flag) VALUES (?, ?, '')", (machine, location))
    db.commit()

# Routes
@app.route('/')
def home():
    return "Welcome to the Scoreboard!"

@app.route('/scoreboard')
def scoreboard():
    db = get_db()
    teams = db.execute('SELECT team_name, points FROM teams ORDER BY points DESC').fetchall()
    return render_template('scoreboard.html', teams=teams)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        team_name = request.form['team_name']
        password = request.form['password']
        flag = request.form['flag']
        db = get_db()
        
        # Verify team credentials
        team = db.execute('SELECT * FROM teams WHERE team_name = ? AND password = ?', 
                         (team_name, password)).fetchone()
        if not team:
            return 'Invalid team name or password.'
            
        # Check if flag is valid
        valid_flag = db.execute('SELECT * FROM flags WHERE flag = ?', (flag,)).fetchone()
        if not valid_flag:
            return 'Invalid flag.'
            
        # Check if team has already submitted this flag
        existing_submission = db.execute('SELECT * FROM submitted_flags WHERE team_name = ? AND flag = ?', 
                                       (team_name, flag)).fetchone()
        if existing_submission:
            return 'This flag has already been submitted by your team.'
            
        # If we get here, the submission is valid and new
        try:
            # Record the submission
            db.execute('INSERT INTO submitted_flags (team_name, flag) VALUES (?, ?)', 
                      (team_name, flag))
            # Update points
            db.execute('UPDATE teams SET points = points + 100 WHERE team_name = ?', 
                      (team_name,))
            db.commit()
            return 'Flag submitted successfully!'
        except sqlite3.Error as e:
            db.rollback()
            return f'Error submitting flag: {str(e)}'
            
    db = get_db()
    teams = db.execute('SELECT team_name FROM teams').fetchall()
    return render_template('submit.html', teams=teams)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        team_name = request.form['team_name']
        password = request.form['password']
        db = get_db()
        db.execute('INSERT INTO teams (team_name, password, points) VALUES (?, ?, 0)', 
                  (team_name, password))
        db.commit()
        return 'Team added successfully!'
    return render_template('admin.html')

# Initialize database on startup within application context
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
