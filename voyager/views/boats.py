
from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape
from flask import redirect

from voyager.db import get_db, execute

def boats(conn):
    return execute(conn, "SELECT * FROM Boats AS b")
def add_boat(conn, boat_n, boat_c):
    return execute(conn, f"INSERT INTO Boats (name, color) VALUES ('{boat_n}', '{boat_c}')")
def sailed_boats(conn, sailorName):
    return execute(conn, f"SELECT DISTINCT Boats.name FROM Boats, Voyages, Sailors WHERE Boats.bid=Voyages.bid AND Voyages.sid=Sailors.sid AND Sailors.name='{sailorName}'")
def boats_pop(conn):
    return execute(conn, "SELECT Boats.name, COUNT(*) FROM Boats, Voyages WHERE Boats.bid=voyages.bid GROUP BY Voyages.bid ORDER BY COUNT(*) DESC" )

def views(bp):
    @bp.route("/boats")
    def _boats():
        with get_db() as conn:
            rows = boats(conn)
        return render_template("table.html", name="Boats Table", rows=rows)
        
    @bp.route("/boats/sailed-by", methods = ['GET', 'POST'])
    def _get_boats():
            with get_db() as conn:
                sailorName= request.form["sailor-name"]
                rows = sailed_boats(conn, sailorName)
            return render_template("table.html", name=sailorName + " sailed these boats", rows=rows)
    @bp.route("/boats/by-popularity", methods = ['GET', 'POST'])
    def _get_boats_pop():
        with get_db() as conn:
            rows = boats_pop(conn)
        return render_template("table.html", name="Boats Popularity", rows=rows)
    @bp.route("/boats/add", methods = ['GET', 'POST'])
    def _boats_added():
        with get_db() as conn:
            boat_n= request.form["b_name"]
            boat_c= request.form["b_color"]
            rows = add_boat(conn, boat_n, boat_c)
        return redirect('/boats')