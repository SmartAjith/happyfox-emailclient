import configparser

def read_db_config(filename='resources/config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object """
    parser = configparser.ConfigParser()
    parser.read(filename)

    # Get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db