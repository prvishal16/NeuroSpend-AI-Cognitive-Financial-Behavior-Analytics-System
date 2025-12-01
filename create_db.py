from app import create_app
from models import db, User, Transaction
import random
import datetime
app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    # seed user
    u = User(name='Demo User', email='demo@example.com')
    db.session.add(u)
    db.session.commit()
    # seed transactions
    cats = ['groceries','food','entertainment','transport','utility','shopping']
    base = datetime.date.today()
    for i in range(1,200):
        t = Transaction(
            user_id=u.id,
            amount=round(random.uniform(20,5000),2),
            category=random.choice(cats),
            description='Auto generated txn %d' % i,
            date=base - datetime.timedelta(days=random.randint(0,90))
        )
        db.session.add(t)
    db.session.commit()
    print('DB initialized with demo user and transactions.')
