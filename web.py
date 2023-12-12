import flask


import models



app = flask.Flask("hrms")
db = models.SQLAlchemy(model_class=models.HRDBBase)

@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "GET":
        return flask.render_template("index.html")
    elif flask.request.method == "POST":
        return "Posted!"


@app.route("/employees")
def employees():
    query = db.select(models.Employee).order_by(models.Employee.fname)
    users = db.session.execute(query).scalars()
    return flask.render_template("userlist.html", users = users)


# @app.route("/employees/<int:empid>")
# def employee_details(empid):
#     query = db.select(models.Employee).where(models.Employee.id == empid)
#     user = db.session.execute(query).scalar()
#     return flask.render_template("userdetails2.html", user = user)

@app.route("/employees/<int:empid>")
def employee_details(empid):
    query = db.select(models.Employee).where(models.Employee.id == empid)
    user = db.session.execute(query).scalar()
    ret = {"fname" : user.fname,
           "lname" : user.lname,
           "title" : user.title.title,
           "email" : user.email,
           "phone" : user.phone}
    return flask.jsonify(ret)






