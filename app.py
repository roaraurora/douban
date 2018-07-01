from project import create_app

app = create_app('flask.cfg')


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True)
