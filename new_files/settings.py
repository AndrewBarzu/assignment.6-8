import javaproperties

class Settings:
    def __init__(self):
        with open('settings.properties', 'r') as f:
            self._settings = javaproperties.load(f)

    @property
    def repository(self):
        return self._settings['repository']

    @property
    def students(self):
        return self._settings['students']

    @property
    def assignments(self):
        return self._settings['assignments']

    @property
    def grades(self):
        return self._settings['grades']

    @property
    def ui(self):
        return self._settings['UI']