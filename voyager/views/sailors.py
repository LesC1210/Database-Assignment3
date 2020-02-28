from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request
from flask import redirect

from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE

def sailors(conn):
    return execute(conn, "SELECT * FROM Sailors AS s")
def add_sailor(conn, sailor_n, sailor_a, sailor_e):
    return execute(conn, f"INSERT INTO Sailors (name, age, experience) VALUES ('{sailor_n}', '{sailor_a}', '{sailor_e}')")
def sailed_sailors(conn, boatName):
    return execute(conn, f" SELECT DISTINCT Sailors.name FROM Sailors, Voyages, Boats WHERE Sailors.sid=Voyages.sid AND Voyages.bid=Boats.bid AND Boats.name='{boatName}'")
def date_sailed(conn, _date):
    return execute(conn, f"SELECT DISTINCT Sailors.name FROM Sailors, Voyages WHERE Sailors.sid=Voyages.sid AND Voyages.date_of_voyage='{_date}'")
def color_sailed(conn, _color):
    return execute(conn, f"SELECT DISTINCT Sailors.name FROM Sailors, Voyages, Boats WHERE Sailors.sid=Voyages.sid AND Voyages.bid=Boats.bid AND Boats.color='{_color}'")


def views(bp):
    @bp.route("/sailors")
    def _sailors():
        with get_db() as conn:
            rows = sailors(conn)
        return render_template("table.html", name="Sailors Table", rows=rows)
    @bp.route("/sailors/who-sailed", methods = ['GET', 'POST'])
    def get_sailors():
            with get_db() as conn:
                boatName= request.form["boat-name"]
                rows = sailed_sailors(conn, boatName)
            return render_template("table.html", name=boatName + " has been sailed by", rows=rows)
    @bp.route("/sailors/who-sailed-on-date", methods = ['GET', 'POST'])
    def sailors_on_date():
            with get_db() as conn:
                _date = request.form["date"]
                rows = date_sailed(conn, _date)
            return render_template("table.html", name= "these sailors have sailed on " + _date, rows=rows)
    @bp.route("/sailors/who-sailed-on-boat-of-color", methods = ['GET', 'POST'])
    def sailors_on_color():
            with get_db() as conn:
                _color = request.form["color"]
                rows = color_sailed(conn, _color)
            return render_template("table.html", name= "These sailors sailed a " + _color + " boat", rows=rows)
    @bp.route("/sailors/add", methods = ['GET', 'POST'])
    def _sailors_added():
        with get_db() as conn:
            sailor_n= request.form["s_name"]
            sailor_a= request.form["s_age"]
            sailor_e= request.form["s_exp"]
            rows = add_sailor(conn, sailor_n, sailor_a, sailor_e)
        return redirect('/sailors')