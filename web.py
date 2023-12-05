import flask

import models

app = flask.Flask("hrms")
db = models.SQLAlchemy(model_class=models.HRDBBase)

@app.route("/")
def index():
    return """<html>
    <head>
    <title> HRMS </title>
    </head>
    <body>
    <h1> Welcome to Hamon HRMS </h1>
    <p>
    <a href="/employees">List of employees</a>
    </p>
    </body>
</html>
"""

@app.route("/employees")
def employees():
    query = db.select(models.Employee).order_by(models.Employee.fname)
    users = db.session.execute(query).scalars()
    userlist = []
    for i in users:
        userlist.append(f"<li>{i.fname}</li")

    return f"""<html>
    <head>
    <title> HRMS </title>
    </head>
    <body>
    <h1> List of employees</h1>
    <ol>
    {"".join(userlist)}
    </ol>
    </body>
</html>
"""






