import MySQLdb
import MySQLdb.cursors

connFirmaF = MySQLdb.Connect(host='192.168.10.51', user='root', passwd='tec.wor_08', db='firma_digital_flask', compress=1, cursorclass=MySQLdb.cursors.DictCursor) # <- important
