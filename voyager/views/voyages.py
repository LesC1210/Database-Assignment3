from collections import namedtuple

from flask import render_template
from flask import request
from flask import redirect

from voyager.db import get_db, execute


def voyages(conn):
    return execute(conn, "SELECT * FROM Voyages AS v")
def add_voyage(conn, voy_sid, voy_bid, voy_dov):
    return execute(conn, f"INSERT INTO Voyages (sid, bid, date_of_voyage) VALUES ('{voy_sid}', '{voy_bid}', '{voy_dov}')")

def views(bp):
    @bp.route("/voyages")
    def _voyages():
        with get_db() as conn:
            rows = voyages(conn)
        return render_template("table.html", name="Voyages Table", rows=rows)
    @bp.route("/voyages/add", methods = ['GET', 'POST'])
    def _voyages_added():
        with get_db() as conn:
            voy_sid= request.form["voyage_sid"]
            voy_bid= request.form["voyage_bid"]
            voy_dov= request.form["voyage_date"]
            rows = add_voyage(conn, voy_sid, voy_bid, voy_dov)
        return redirect('/voyages')