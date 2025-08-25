import validators

from urllib.parse import urlparse
from page_analyzer.exceptions import (
    EmptyUrlError, TooLongUrlError, InvalidUrlError
)
from dataclasses import dataclass
from psycopg2.extras import DictCursor, NamedTupleCursor
from typing import Optional
from datetime import datetime

@dataclass
class UrlItem:
    name: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    last_check: Optional[datetime] = None
    check_status: Optional[int] = None


class UrlRepo:
    def __init__(self, conn):
        self.conn = conn

    @staticmethod
    def validate(url):
        if not url:
            raise EmptyUrlError
        if len(url) > 255:
            raise TooLongUrlError
        if not validators.url(url):
            raise InvalidUrlError
        return True

    @staticmethod
    def normalize_url(url):
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def save(self, name):
        with self.conn.cursor() as curs:
            sql = """
            INSERT INTO urls
            (name) VALUES (%s)
            RETURNING id;
            """
            curs.execute(sql, (name,))
            id = curs.fetchone()[0]
        self.conn.commit()
        return id

    def find_url_by_name(self, name):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            sql = """
            SELECT * FROM urls
            WHERE name = %s;
            """
            curs.execute(sql, (name,))
            row = curs.fetchone()
            return UrlItem(
                name=row.name,
                id=row.id,
                created_at=row.created_at.isoformat()
            ) if row else None

    def find_url_by_id(self, id):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            sql = """
            SELECT * FROM urls
            WHERE id = %s;
            """
            curs.execute(sql, (id,))
            row = curs.fetchone()
            return UrlItem(
                name=row.name,
                id=row.id,
                created_at=row.created_at.isoformat()
            ) if row else None

    def get_content(self):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            try:
                sql = """
                SELECT id, name FROM urls
                ORDER BY id DESC;
                """
                curs.execute(sql)
                res = []
                for item in curs.fetchall():
                    res.append(UrlItem(
                        id=item.id,
                        name=item.name
                    ))
                return res
            except Exception as e:
                print(f"Error executing SQL: {e}")
                self.conn.rollback()
                raise