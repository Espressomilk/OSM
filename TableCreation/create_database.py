import pymysql


def create_database(_host, _user, _passwd, _dbname):
    db = pymysql.connect(host=_host, user=_user, passwd=_passwd, charset='utf8')
    cur = db.cursor()

    try:
        cur.execute("create database `%s` default character set utf8 collate utf8_general_ci" % _dbname)
        db.commit()
    except Exception as e:
        print(e)
