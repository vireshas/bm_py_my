#### Benchmarking C and pure Python Mysql adapters with Gevent


For 100 db calls(insert and read)  
C mysql adapter takes about 30x more time.  

C mysql adapter inside Gevent: 6.03962492943  
Python mysql adapter inside Gevent: 0.247358083725  

