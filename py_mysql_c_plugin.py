import MySQLdb
import gevent
import gevent.monkey
gevent.monkey.patch_socket()

config = ('localhost', 'root', '', 'bm')

cnx = MySQLdb.connect(*config)
cursor = cnx.cursor()

#clear db before the tests
cursor.execute('truncate table bm;')

def make_10k_db_calls(i):
    cnx = MySQLdb.connect(*config)
    cursor = cnx.cursor()
    i = str(i)
    query = 'insert into bm(id,col,value) values(%s,"%s","%s")' % (i, 'col'+i, 'value'+i)
    cursor.execute(query)
    query = 'select * from bm where id=%s' % (i)
    cursor.execute(query)
    print cursor.fetchone()

import time
start = time.time()

jobs =  [ gevent.spawn(make_10k_db_calls, i) for i in xrange(100)]
gevent.joinall(jobs)
cnx.commit()

end = time.time()

print end - start

cnx.close()
