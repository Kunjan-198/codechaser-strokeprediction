from flask import Flask, render_template

app=flask.Flask(__name__, template_folder='templates')

@app.route('/')
def main():
    return (flask.render_template('main.html'))
if __name__=='__main__':
    app.run()



