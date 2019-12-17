from mars_planet_library import app, settings

if __name__ == '__main__':
    app.run(debug=bool(settings.SECURITY_SETTINGS.get("DEBUG_MODE")))
