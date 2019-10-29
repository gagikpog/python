# python3 -m flask run

# db.create_all()
# user = User(phone = '92200000', mail = 'vahepog@gmail.com', name = 'Vahe', sname = 'Pogosyan', activity='student')

gagik = User.query.filter_by(id='1').first()
vahe = User.query.filter_by(id='2').first()
# print(gagik)
# print(vahe)
bill = Bill(title='first bill', summ=500, user_id = gagik.id)
db.session.add(bill)
db.session.commit()