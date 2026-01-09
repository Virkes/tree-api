from tree.db import db

class Node(db.Model):
    __tablename__ = "nodes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    ordering = db.Column(db.Integer, nullable=False)

    parent_node_id = db.Column(
        db.Integer,
        db.ForeignKey("nodes.id", ondelete="CASCADE"),
        nullable=True
    )