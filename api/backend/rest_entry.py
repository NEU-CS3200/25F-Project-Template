from flask import Flask

from backend.db_connection import db

from backend.users.user_routes import users
from backend.budgets.budget_routes import budgets
from backend.transactions.transaction_routes import transactions
from backend.savings.saving_routes import savings
from backend.loans.loan_routes import loans
from backend.investments.investment_routes import investments
from backend.bills.bill_routes import bills
from backend.subscriptions.subscription_routes import subscriptions
from backend.insights.insight_routes import insights

import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()

    app.logger.info('current DB name = ' + os.getenv('DB_NAME').strip())

    db.init_app(app)

    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(budgets, url_prefix='/budgets')
    app.register_blueprint(transactions, url_prefix='/transactions')
    app.register_blueprint(savings, url_prefix='/savings')
    app.register_blueprint(loans, url_prefix='/loans')
    app.register_blueprint(investments, url_prefix='/investments')
    app.register_blueprint(bills, url_prefix='/bills')
    app.register_blueprint(subscriptions, url_prefix='/subscriptions')
    app.register_blueprint(insights, url_prefix='/insights')

    @app.route('/')
    def index():
        return "Welcome to the Budget App API"

    @app.route('/health')
    def health():
        return "Healthy"

    return app