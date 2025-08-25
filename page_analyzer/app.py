import os

import psycopg2

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages
)
from dotenv import load_dotenv

from page_analyzer.exceptions import EmptyUrlError, TooLongUrlError, InvalidUrlError
from page_analyzer.url_repo import UrlRepo, UrlItem

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

repo = UrlRepo()


@app.route('/')
def init_index():
    f = get_flashed_messages()
    return render_template(
        "index.html",
        tmp_output=f
    )


@app.get('/urls')
def index_urls():
    url_items = repo.get_content()
    return render_template(
        "index_urls.html",
        url_items=url_items
    )


@app.post('/urls')
def add_url():
    url = request.form.get("url", "").strip()

    try:
        UrlRepo.validate(url)

    except EmptyUrlError:
        flash("URL не может быть пустым", "danger")
        return render_template("index.html"), 422

    except TooLongUrlError:
        flash("URL превышает 255 символов", "danger")
        return render_template("index.html"), 422

    except InvalidUrlError:
        flash("Некорректный URL", "danger")
        return render_template("index.html"), 422

    normalized_url = UrlRepo.normalize_url(url)
    url_find = repo.find_url_by_name(normalized_url)
    if url_find:
        flash("Страница уже существует", "info")
        id = url_find.id
    else:
        id = repo.save(normalized_url)
        flash("Страница успешно добавлена", "success")

    return redirect(
        url_for("show_url", url_id=id),
        code=302
    )


@app.get('/urls/<url_id>')
def show_url(url_id):
    url = repo.find_url_by_id(url_id)
    return render_template(
        "show_url.html",
        url=url
    )

