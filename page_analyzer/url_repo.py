import validators
import psycopg2
import os
from urllib.parse import urlparse
from dataclasses import dataclass
from psycopg2.extras import NamedTupleCursor
from typing import Optional
from datetime import datetime

@dataclass
class UrlItem:
    name: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    last_check: Optional[datetime] = None
    status_code: Optional[int] = None


@dataclass
class CheckItem:
    id: int
    status_code: int
    h1: str
    title: str
    description: str
    created_at: datetime
    url_id: Optional[int] = None


DATABASE_URL = os.getenv('DATABASE_URL')

class UrlRepo:
    def __init__(self):
        self.db = DATABASE_URL

    @staticmethod
    def is_valid_url(url):
        if len(url) > 255:
            return 'URL превышает 255 символов'
        elif validators.url(url) is not True:
            return 'Некорректный URL'
        return None

    @staticmethod
    def normalize_url(url):
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def save_url(self, name):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as curs:
                sql = """
                INSERT INTO urls
                (name) VALUES (%s)
                RETURNING id;
                """
                curs.execute(sql, (name,))
                id = curs.fetchone()[0]
            conn.commit()
            return id

    def save_check(self, url_id, status_code, h1, title, description):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as curs:
                sql = """
                INSERT INTO url_checks
                (url_id, status_code, h1, title, description) VALUES 
                (%s, %s, %s, %s, %s)
                RETURNING id;
                """
                curs.execute(sql, (url_id, status_code, h1, title, description))
                id = curs.fetchone()[0]
            conn.commit()
            return id

    def find_url_by_name(self, name):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
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
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
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
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                try:
                    sql = """
                    SELECT 
                        urls.id, 
                        urls.name, 
                        MAX(url_checks.created_at) AS last_check, 
                        (SELECT status_code
                        FROM url_checks
                        WHERE url_id = urls.id
                        ORDER BY created_at DESC
                        LIMIT 1) as status_code
                    FROM urls FULL JOIN url_checks
                    ON urls.id = url_checks.url_id
                    GROUP BY urls.id
                    ORDER BY id DESC; 
                    """
                    curs.execute(sql)
                    res = []
                    for item in curs.fetchall():
                        res.append(UrlItem(
                            id=item.id,
                            name=item.name,
                            last_check=item.last_check.isoformat() if item.last_check else "",
                            status_code=item.status_code
                        ))
                    return res
                except Exception as e:
                    print(f"Error executing SQL: {e}")
                    conn.rollback()
                    raise

    def get_checks(self, url_id):
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                sql = """
                SELECT * FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
                """
                curs.execute(sql, (url_id,))
                res = []
                for item in curs.fetchall():
                    res.append(CheckItem(
                        id=item.id,
                        status_code=item.status_code,
                        h1=item.h1,
                        title=item.title,
                        description=item.description,
                        created_at=item.created_at.isoformat() if item.created_at else ""
                    ))
                return res
