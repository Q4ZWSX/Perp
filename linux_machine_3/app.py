from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission (e.g., comments)
        flash('Thank you for your message!')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact Us')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # Confirm file upload without processing
            flash(f'File \"{uploaded_file.filename}\" uploaded successfully!')
            return redirect(url_for('upload'))
    return render_template('upload.html', title='Upload File')

# Hidden 'dev' page
@app.route('/dev', methods=['GET', 'POST'])
def dev():
    if request.method == 'POST':
        address = request.form['address']
        try:
            # Directly use the address given by the user in the ping command
            # This allows for command injection for testing purposes
            output = subprocess.check_output(f'ping -c 4 {address}', shell=True, text=True)
            return render_template('dev.html', title='Dev Tools', output=output)
        except subprocess.CalledProcessError as e:
            flash('Ping failed. Please try again.')
            return redirect(url_for('dev'))
    return render_template('dev.html', title='Dev Tools', output='')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
