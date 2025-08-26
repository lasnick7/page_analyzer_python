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
from bs4 import BeautifulSoup
load_dotenv()
from page_analyzer.url_repo import UrlRepo

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

repo = UrlRepo()


@app.route('/')
def init_index():
    return render_template("index.html")


@app.route('/urls', methods=['POST', 'GET'])
def add_url():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()

        error = UrlRepo.is_valid_url(url)
        if error:
            flash(error, "danger")
            return render_template("index.html"), 422

        normalized_url = UrlRepo.normalize_url(url)
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
        r.raise_for_status()
        status_code = r.status_code
        htm_text = r.text
        parsed_html = BeautifulSoup(htm_text, "html.parser")
        h1 = parsed_html.h1.get_text().strip() if parsed_html.h1 else ""
        title = parsed_html.title.string.strip() if parsed_html.title else ""
        description_meta = parsed_html.find('meta', attrs={'name': 'description'})
        description = (
            description_meta["content"].strip()
            if description_meta and "content" in description_meta.attrs
            else ""
        )
        repo.save_check(url_id, status_code, h1, title, description)
        flash("Страница успешно проверена", "success")
    except Exception:
        flash("Произошла ошибка при проверке", "danger")

    return redirect(url_for("show_url", url_id=url_id))



