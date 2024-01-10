from flask import Blueprint, request, flash, render_template
from flask_login import login_required, current_user
from flaskblog.models import Item

purchases = Blueprint('purchases', __name__)


@purchases.route('/purchase_history')
@login_required
def purchase_history():
    if request.method == 'GET':
        purchased_items = Item.query.filter_by(owner=current_user.id).all()
        return render_template('purchase_history.html', purchased_items=purchased_items)
    else:
        flash('No Purchases Found!', category='danger')
