from flask import Flask, render_template, request
from static.models.account import Account
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
users = db.users


@app.route('/')
def hello_world():
    return render_template('homepage.html')


@app.route('/tc/')
def tnc():
    return render_template("tnc.html")


@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/login/')
def logg():
    return render_template('login.html')


@app.route('/send_details', methods=['POST'])
def registration():
    email = request.form['email']
    pwd = request.form['psw']
    pwd_rpt = request.form['psw-repeat']

    if pwd != pwd_rpt:
        error = "password doesn't match"
        return render_template('register.html', error=error)

    acct = Account()
    acct.email = email
    acct.password = pwd

    users.insert_one({"email": acct.email, "password": acct.password, "tx_history": acct.transaction_history})
    return render_template('login.html', Httpstatus="okay")


account = Account()


def save(acct):
    users.update_one({"email": acct.email},
                     {"$set": {"tx_history": acct.transaction_history}})


@app.route("/transfer/", methods=['POST'])
def transfer():
    re_email = request.form['re-email']
    amount = request.form['amt']
    pwd = request.form['pwd']

    status = 'transfer not successful'

    if account.validatePassword(pwd, account.gbq()):
        acc = find_acct_by_email(re_email)
        acc.transaction_history.append(
            dict(amount=int(amount),
                 date=datetime.now().strftime(f"%Y-%m-%d {'time->'} %H:%M"), type="Transfer-in")
        )
        save(acc)
        account.transaction_history.append(
            dict(amount=int(amount), date=datetime.now().strftime(f"%Y-%m-%d {'time->'} %H:%M"), type="Transfer-out"))

        save(account)
        status = 'transfer successful'
    else:
        print("invalid pass")

    return render_template('user_page.html', account=account, status=status)


def find_acct_by_email(email: str) -> Account | None:
    user_list = list(users.find())
    for user in user_list:
        if user['email'] == email:
            acct = Account()
            acct.email = user['email']
            acct.transaction_history = user['tx_history']
            return acct

    return None


def deposit(acct: Account, amount):
    status = 'deposit successful'
    try:
        acct.deposit(int(amount))

    except ValueError as e:
        status = e.args[0]
        return status

    save(acct)
    return status


@app.route('/deposit/', methods=['POST'])
def deposit_and_return():
    amount = request.form['amt']
    status = deposit(account, amount)
    return render_template('user_page.html', account=account, status=status)


@app.route('/withdraw/', methods=['POST'])
def withdraw_():
    amount = request.form['amt']
    status = withdraw(account, amount)
    return render_template('user_page.html', account=account, status=status)


def withdraw(acct: Account, amount):
    status = 'withdrawal successful'
    try:
        acct.withdraw(int(amount))
        print(acct.transaction_history)

    except ValueError as e:
        status = e.args[0]
        return status

    save(acct)
    return status


@app.route('/user_page/withdraw/')
def withdraw_req():
    return render_template('withdraw.html', account=account)


@app.route('/user_page/transfer/')
def transfer_req():
    return render_template('transfer.html', account=account)


@app.route('/user_page/tx_history')
def tx_history_req():
    return render_template('tx_history.html', account=account)


@app.route('/user_page/deposit/')
def deposit_page():
    return render_template('deposit.html', account=account)


@app.route('/user_page', methods=['POST'])
def getAccount():
    email = request.form['email']
    pwd = request.form['psw']
    user_list = list(users.find())
    for user in user_list:
        if user['email'] == email and account.validatePassword(pwd, user['password']):
            account.email = user['email']
            account.transaction_history = user['tx_history']
            account.password = user['password']

            return render_template('user_page.html', account=account)
    error = "invalid credentials, try again"

    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
