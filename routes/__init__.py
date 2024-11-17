from .authentication import authentication_blueprint
from .battle import battles_blueprint
from .building import buildings_blueprint
from .city import cities_blueprint
from .island import islands_blueprint
from .player import players_blueprint
from .unit import units_blueprint
from .world import worlds_blueprint


def register_routes(app):
    app.register_blueprint(authentication_blueprint, url_prefix="/auth")
    app.register_blueprint(battles_blueprint, url_prefix="/battles")
    app.register_blueprint(buildings_blueprint, url_prefix="/buildings")
    app.register_blueprint(cities_blueprint, url_prefix="/cities")
    app.register_blueprint(islands_blueprint, url_prefix="/islands")
    app.register_blueprint(players_blueprint, url_prefix="/players")
    app.register_blueprint(units_blueprint, url_prefix="/units")
    app.register_blueprint(worlds_blueprint, url_prefix="/worlds")
