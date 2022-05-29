from flask import Flask, request, send_file, render_template, make_response, abort
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import pandas as pd
import pydot
from io import BytesIO

app = Flask(__name__)
conn = None

def connect_db():
    try:
        return psycopg2.connect("dbname='flask_tree' user='postgres' host='localhost' password=''")
    except:
        raise Exception("I am unable to connect to the database")

def get_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)

def sex_filter(sql, params, args, chain=1):
    if "sex" in args:
        where = "AND" if "WHERE" in sql.upper() else "WHERE"
        return sql + f" {where} f{chain}.sex=%s", params + (args["sex"],)
    return sql, params

@app.route('/all/', methods=['GET'])
@app.route('/fetch/', methods=['GET'])
def fetch():
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = "SELECT f1.id, f1.name, f1.sex, f1.parent FROM family_node AS f1"
            params = ()
            sql, params = sex_filter(sql, params, request.args)
            cur.execute(sql, params)
            return json.dumps(cur.fetchall())

@app.route('/<int:self>/', methods=['GET'])
def get(self):
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = """
                SELECT f1.id, f1.name, f1.sex, f1.parent
                FROM family_node AS f1
                WHERE f1.id=%s
            """
            params = (self,)
            #sql, params = sex_filter(sql, params, request.args)
            cur.execute(sql, params)
            return json.dumps(cur.fetchall())

@app.route('/<int:self>/child/', methods=['GET'])
def child(self):
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = """
                SELECT f1.id, f1.name, f1.sex, f1.parent
                FROM family_node AS f1
                WHERE f1.parent=%s
            """
            params = (self,)
            sql, params = sex_filter(sql, params, request.args)
            cur.execute(sql, params)
            return json.dumps(cur.fetchall())

@app.route('/<int:self>/grandchild/', methods=['GET'])
def grandchild(self):
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = """
                SELECT f1.id, f1.name, f1.sex, f1.parent
                FROM family_node AS f1
                WHERE f1.parent IN (
                    SELECT f2.id
                    FROM family_node AS f2
                    WHERE f2.parent=%s
                )
            """
            params = (self,)
            sql, params = sex_filter(sql, params, request.args)
            cur.execute(sql, params)
            return json.dumps(cur.fetchall())

@app.route('/<int:self>/grandchild_p/', methods=['GET'])
@app.route('/<int:self>/grandchild_f/', methods=['GET'])
def grandchild_p(self):
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = """
                SELECT f1.id, f1.name, f1.sex, f1.parent
                FROM family_node AS f1
                WHERE f1.parent IN (
                    SELECT f2.id
                    FROM family_node AS f2
                    WHERE f2.parent=%s
                ) AND f1.sex, f1.parent='P'
            """
            params = (self,)
            # sql, params = sex_filter(sql, params, request.args)
            cur.execute(sql, params)
            return json.dumps(cur.fetchall())

@app.route('/<int:self>/aunt_uncle/', methods=['GET'])
@app.route('/<int:self>/uncle_aunt/', methods=['GET'])
def aunt_uncle(self):
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = """
                SELECT f1.id, f1.name, f1.sex, f1.parent
                FROM family_node AS f1
                WHERE f1.parent=(
                    SELECT f2.parent
                    FROM family_node AS f2
                    WHERE f2.id=(
                        SELECT f3.parent
                        FROM family_node AS f3
                        WHERE f3.id=%s
                    )
                )
            """
            params = (self,)
            sql, params = sex_filter(sql, params, request.args)
            cur.execute(sql, params)
            return json.dumps(cur.fetchall())

@app.route('/<int:self>/aunt/', methods=['GET'])
def aunt(self):
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = """
                SELECT f1.id, f1.name, f1.sex, f1.parent
                FROM family_node AS f1
                WHERE f1.parent=(
                    SELECT f2.parent
                    FROM family_node AS f2
                    WHERE f2.id=(
                        SELECT f3.parent
                        FROM family_node AS f3
                        WHERE f3.id=%s
                    )
                ) AND f1.sex, f1.parent='P'
            """
            params = (self,)
            # sql, params = sex_filter(sql, params, request.args)
            cur.execute(sql, params)
            return json.dumps(cur.fetchall())

@app.route('/<int:self>/niece_nephew/', methods=['GET'])
@app.route('/<int:self>/nephew_niece/', methods=['GET'])
def niece_nephew(self):
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = """
                SELECT f1.id, f1.name, f1.sex, f1.parent
                FROM family_node AS f1
                WHERE f1.parent IN (
                    SELECT f2.id
                    FROM family_node AS f2
                    WHERE f2.parent=(
                        SELECT f3.parent
                        FROM family_node AS f3
                        WHERE f3.id=(
                            SELECT f4.parent
                            FROM family_node AS f4
                            WHERE f4.id=%s
                        )
                    )
                )
            """
            params = (self,)
            sql, params = sex_filter(sql, params, request.args)
            cur.execute(sql, params)
            return json.dumps(cur.fetchall())

@app.route('/<int:self>/nephew/', methods=['GET'])
def nephew(self):
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = """
                SELECT f1.id, f1.name, f1.sex, f1.parent
                FROM family_node AS f1
                WHERE f1.parent IN (
                    SELECT f2.id
                    FROM family_node AS f2
                    WHERE f2.parent=(
                        SELECT f3.parent
                        FROM family_node AS f3
                        WHERE f3.id=(
                            SELECT f4.parent
                            FROM family_node AS f4
                            WHERE f4.id=%s
                        )
                    )
                )
            """
            params = (self,)
            sql, params = sex_filter(sql, params, request.args)
            cur.execute(sql, params)
            return json.dumps(cur.fetchall())

def build_query(up=0, down=0, **kwargs):
    up, down = int(up), int(down)
    chain = 1
    sql = "SELECT %s"
    for i in range(up):
        sql = f"""
SELECT f{chain}.parent
FROM family_node AS f{chain}
WHERE f{chain}.id IN (
    {sql}
)
        """

        chain += 1
    for i in range(down):
        sql = f"""
SELECT f{chain}.id
FROM family_node AS f{chain}
WHERE f{chain}.parent IN (
    {sql}
)
        """
        chain += 1

    sql = f"""
SELECT f{chain}.id, f{chain}.name, f{chain}.sex, f{chain}.parent
FROM family_node AS f{chain}
WHERE f{chain}.id IN (
    {sql}
)
    """
    return sql, chain

@app.route('/<int:self>/select/', methods=['GET'])
def select(self):
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql, chain = build_query(**request.args)
            print(sql)
            params = (self,)
            sql, params = sex_filter(sql, params, request.args, chain=chain)
            cur.execute(sql, params)
            return json.dumps(cur.fetchall())

def fetch_all():
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = "SELECT f1.id, f1.name, f1.sex, f1.parent FROM family_node AS f1"
            cur.execute(sql)
            return cur.fetchall()

@app.route('/chart/', methods=['GET'])
def chart():
    data = fetch_all()

    G = pydot.Dot('Family Tree', graph_type='graph', bgcolor='#F0F8FB')

    for node in data:
        G.add_node(pydot.Node(
            node["id"],
            fillcolor="#3587BF" if node["sex"] == "L" else "#FA7A79",
            label=node["name"],
            shape="hexagon",
            style="filled"
        ))

    for node in [n for n in data if n["parent"]]:
        G.add_edge(pydot.Edge(
            node["parent"],
            node["id"]
        ))

    #create a png file
    png_str = G.create_png(prog='dot')

    # treat the DOT output as an image file
    sio = BytesIO()
    sio.write(png_str)
    sio.seek(0)

    return send_file(sio, mimetype='image/png', cache_timeout=0)

@app.route('/', methods=['GET'])
def index():
    apis = [
        {
            "label": "Query API",
            "id": "query-api"
        },
        {
            "label": "Query API Select",
            "id": "query-api-select"
        },
    ]
    queries = [
        {
            "label": "Anak A1L",
            "id": "anak-a1l"
        },
        {
            "label": "Cucu A1L",
            "id": "cucu-a1l"
        },
        {
            "label": "Cucu perempuan A1L",
            "id": "cucu-a1l-p"
        },
        {
            "label": "Bibi C2P",
            "id": "bibi-c2p"
        },
        {
            "label": "Sepupu laki-laki E1P",
            "id": "sepupu-e1p-l"
        },
    ]
    response = make_response(render_template('index.html', apis=apis, queries=queries))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response

@app.route('/crud/', methods=['GET'])
def crud():
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = """
        SELECT f1.id, f1.name, f1.sex, f1.parent, f2.name AS parent_name
        FROM family_node AS f1
        LEFT JOIN family_node AS f2
        ON f1.parent=f2.id
            """
            cur.execute(sql)
            nodes = cur.fetchall()
            return render_template('crud.html', nodes=nodes)


@app.route('/<int:id>/delete/', methods=['GET', 'POST', 'DELETE'])
def delete_node(id):
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = "DELETE FROM family_node AS f1 WHERE f1.id=%s"
            cur.execute(sql, (id,))
            if cur.rowcount == 0:
                return "Gagal menghapus node", 500
            return json.dumps({
                "message": "Node berhasil dihapus"
            })

@app.route('/add/', methods=['POST'])
def add_node():
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = """
INSERT INTO family_node(name, sex, parent)
VALUES (%(name)s, %(sex)s, %(parent)s)
RETURNING id
            """
            data = dict(request.form)
            if "parent" not in data or not data["parent"] or data["parent"].lower().strip() == "null" or data["parent"].lower().strip() == "none":
                data["parent"] = None
            if "name" not in data or not data["name"]:
                return "Nama harus diisi", 400
            if "sex" not in data or not data["sex"]:
                return "Jenis kelamin harus diisi", 400
            cur.execute(sql, data)
            if cur.rowcount == 0:
                return "Gagal menambah node", 500
            id = cur.fetchone()['id']
            return json.dumps({
                "message": "Node berhasil ditambahkan",
                "id": id
            })

@app.route('/<int:id>/update/', methods=['POST'])
@app.route('/<int:id>/edit/', methods=['POST'])
def update_node(id):
    with connect_db() as conn:
        with get_cursor(conn) as cur:
            sql = """
UPDATE family_node f1
SET name=%(name)s, sex=%(sex)s, parent=%(parent)s
WHERE f1.id=%(id)s
            """
            data = dict(request.form)
            if "parent" not in data or not data["parent"] or data["parent"].lower().strip() == "null" or data["parent"].lower().strip() == "none":
                data["parent"] = None
            data["id"] = id
            if "name" not in data or not data["name"]:
                return "Nama harus diisi", 400
            if "sex" not in data or not data["sex"]:
                return "Jenis kelamin harus diisi", 400
            cur.execute(sql, data)
            if cur.rowcount == 0:
                return "Gagal menambah node", 500
            return json.dumps({
                "message": "Node berhasil diperbarui"
            })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
