from fastapi import FastAPI

from app.api import auth, products, orders, invoices, users
from app.core.metrics.prometheus import register_prometheus
from app.core.middlewares.audit import AuditLoggingMiddleware
from app.core.middlewares.cors import register_cors
from app.core.middlewares.rate_limit import register_rate_limit

app = FastAPI(title='Order API', version='0.2.0')

# Middlewares
app.add_middleware(AuditLoggingMiddleware, audit_csv_path='audit_log.csv')
register_cors(app)
register_rate_limit(app)
register_prometheus(app)

# Routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(invoices.router)
app.include_router(users.router)


@app.get('/')
def home():
    return {'message': 'Order API running'}