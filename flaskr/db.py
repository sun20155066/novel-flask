import pymysql

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        # 'database':'novel',
        'passwd': 'root',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor

    }


    if 'db' not in g:
        g.db = pymysql.connect(**config)
        
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    cur = db.cursor()
    ##读取SQL文件,获得sql语句的list
    with open(file='schema.sql', mode='r+') as f:
        sql_list = f.read().split(';')[:-1]  # sql文件最后一行加上;
        sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]  # 将每段sql里的换行符改成空格
    ##执行sql语句，使用循环执行sql语句
    for sql_item in sql_list:
        # print (sql_item)
        cur.execute(sql_item)




@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
