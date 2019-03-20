import json, logging, sys
from blueprints import app, manager
from logging.handlers import RotatingFileHandler


if __name__ == '__main__':
    '''define format log dan membuat rotasi log dengan backup
    10 files dan ukuran 10MB'''
    formatter = logging.Formatter("[%(asctime)s]{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    log_handler = RotatingFileHandler("%s/%s" % (app.root_path,
    '../storage/log/app.log'),
    maxBytes=1000000, backupCount=10)
    log_handler.setLevel(logging.INFO)
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)

    try:
        if sys.argv[1] == 'db':
            manager.run()
        else:
            app.run(debug = True, host = '0.0.0.0', port = 8000) # local host
    except IndexError as e:
        app.run(debug = True, host = '0.0.0.0', port = 8000) # local host