import mysql.connector
import gevent
import gevent.monkey
gevent.monkey.patch_socket()

config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'database': 'bm',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

#clear db before the tests
cursor.execute('truncate table bm;')

def make_10k_db_calls(i):
    #gevent cant reuse open socket in another greenlet
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    i = str(i)
    query = 'insert into bm(id,col,value) values(%s,"%s","%s")' % (i, 'col'+i, 'value'+i)
    cursor.execute(query)
    cnx.commit()
    query = 'select * from bm where id=%s' % (i)
    cursor.execute(query)
    for i in cursor:
        print i
    cnx.close()

import time
start = time.time()

jobs =  [ gevent.spawn(make_10k_db_calls, i) for i in xrange(100)]
gevent.joinall(jobs)

end = time.time()
print end - start
