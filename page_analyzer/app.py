import os

import requests
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from dotenv import load_dotenv

from page_analyzer.repository import UrlRepo  # noqa: E402
from  page_analyzer.utils import is_valid_url, parse_response, normalize_url


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

repo = UrlRepo(database_url=DATABASE_URL)


@app.route('/')
def init_index():
    return render_template("index.html")


@app.route('/urls', methods=['POST', 'GET'])
def add_url():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()

        error = is_valid_url(url)
        if error:
            flash(error, "danger")
            return render_template("index.html"), 422

        normalized_url = normalize_url(url)
        url_find = repo.find_url_by_name(normalized_url)
        if url_find:
            flash("Страница уже существует", "info")
            id = url_find.id
            return redirect(url_for("show_url", url_id=id), )

        id = repo.save_url(normalized_url)
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("show_url", url_id=id),)

    url_items = repo.get_content()
    return render_template(
        "index_urls.html",
        url_items=url_items
    )


@app.route('/urls/<url_id>')
def show_url(url_id):
    url = repo.find_url_by_id(url_id)
    checks = repo.get_checks(url_id)
    return render_template(
        "show_url.html",
        url=url,
        checks=checks
    )


@app.route('/urls/<url_id>/checks', methods=['POST'])
def make_check(url_id):
    url_item = repo.find_url_by_id(url_id)
    if not url_item:
        flash('Страница не найдена', 'danger')
        return redirect(url_for("init_index"))

    url_name = url_item.name
    try:
        r = requests.get(url_name, allow_redirects=True)
        status_code, h1, title, description = parse_response(r)
        repo.save_check(url_id, status_code, h1, title, description)
        flash("Страница успешно проверена", "success")
    except Exception:
        flash("Произошла ошибка при проверке", "danger")

    return redirect(url_for("show_url", url_id=url_id))
