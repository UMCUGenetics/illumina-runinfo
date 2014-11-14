from app import app, WSGIMiddleware

# Setup prefix
app.wsgi_app = WSGIMiddleware(app.wsgi_app, "")

app.run(debug = True)
