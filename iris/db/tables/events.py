from sqlalchemy import BOOLEAN, INT, Column, String, Table
from sqlalchemy.sql.expression import desc, select

from iris.db.tables import BaseModel


class Events(BaseModel):

    def __init__(self, engine, metadata, role='reader'):
        table = Table(
            'events',
            metadata,
            Column('id', INT, primary_key=True, autoincrement=True),
            Column('name', String),
            Column('type_id', INT),
            Column('description', String),
            Column('markdown_path', String),
            Column('attachment_hex', String),
            Column('attachment_type', INT),
            Column('is_deleted', BOOLEAN),
            Column('updated_at', INT)
        )
        super().__init__(engine, metadata, table, role)

    def insert(self, row):
        self.raw_insert(row)

    def get_events(self):
        stmt = select(['*']) \
            .where(self.table.c.is_deleted == 0) \
            .order_by(desc(self.table.c.id))

        cursor = self.execute(stmt)
        row = cursor.fetchone()
        while row:
            yield dict(zip([col.key for col in self.table.columns], row))
            row = cursor.fetchone()
