from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    with app.app_context():
        db.create_all()

        engine = db.get_engine()
        connection = engine.connect()

        result = connection.execute(
            "SELECT 1 FROM nodes LIMIT 1"
        ).fetchone()

        if result is None:
            connection.execute(
                "INSERT INTO nodes (id, title, ordering, parent_node_id) "
                "VALUES (1, 'Root', 0, NULL)"
            )

        connection.close()
