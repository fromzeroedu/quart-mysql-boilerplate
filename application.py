from quart import Quart

from db import sa_connection


def create_app(**config_overrides):
    app = Quart(__name__)

    # Load config
    app.config.from_pyfile("settings.py")

    # apply overrides for tests
    app.config.update(config_overrides)

    # import blueprints
    from counter.views import counter_app

    # register blueprints
    app.register_blueprint(counter_app)

    @app.before_serving
    async def create_db_conn():
        print("Starting app")
        app.sac = await sa_connection()

    @app.after_serving
    async def close_db_conn():
        print("Closing down app")
        await app.sac.close()

    return app
