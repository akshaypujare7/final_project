import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app, flash
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Transaction
from app.transactions.forms import csv_upload
from werkzeug.utils import secure_filename, redirect

transactions = Blueprint('transactions', __name__, template_folder='templates')


@transactions.route('/transactions', methods=['GET'], defaults={"page": 1})
@transactions.route('/transactions/<int:page>', methods=['GET'])
def transaction_browse(page):
    page = page
    per_page = 1000

    pagination = Transaction.query.filter(Transaction.user.any(id=current_user.id)).paginate(page, per_page,
                                                                                             error_out=False)
    data = pagination.items
    try:
        return render_template('browse_transaction.html', data=data, pagination=pagination)
    except TemplateNotFound:
        abort(404)


@transactions.route('/transactions/upload', methods=['POST', 'GET'])
@login_required
def transaction_upload():
    form = csv_upload()
    if form.validate_on_submit():
        log = logging.getLogger("myApp")
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        log.info(filename + 'file uploaded')

        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.mkdir(current_app.config['UPLOAD_FOLDER'])
        form.file.data.save(filepath)

        balance = current_user.balance
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            try:
                for row in csv_file:
                    current_user.transaction.append(Transaction(row['AMOUNT'], row['TYPE']))
                    balance += float(row['AMOUNT'])
                flash(filename + ' has successfully uploaded', 'success')
            except KeyError:
                flash('File upload unsuccessful')
                return redirect(url_for('transactions.transaction_upload'))

        current_user.balance = balance
        db.session.commit()

        return redirect(url_for('transactions.transaction_browse'))

    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)
