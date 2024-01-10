from flask import Blueprint, request, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from flaskblog.market.forms import PurchaseItemForm
from flaskblog.models import Item

market = Blueprint('market', __name__)


@market.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for Rs.{p_item_object.price}",
                      category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!",
                      category='danger')

        return redirect(url_for('market.market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        return render_template('market.html', items=items, purchase_form=purchase_form)
