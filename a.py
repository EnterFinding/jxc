#coding: utf8
import pymssql

			
import os, sys
parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jxc.settings")
import django
django.setup()
from sale.models import Mod,Category, Commdity

sql = "select distinct(replace(ggxh, ' ', '')), rtrim(jldw) from spml where jldw<>'' and ggxh<>''"
with pymssql.connect(host='10.10.136.131', user='sa', password='E53r04', database='ERP', charset='cp936') as data:
	with data.cursor() as cur:
		cur.execute(sql.encode('utf8'))
		for row in cur:
			Mod.objects.update_or_create(mod_name=row[0], mod_gram=row[-1])

sql = "select distinct(rtrim((select mc from spfl where spfl.fl=spml.spfl_1))) from spml where (select mc from spfl where spfl.fl=spml.spfl_1)<>''"
with pymssql.connect(host='10.10.136.131', user='sa', password='E53r04', database='ERP', charset='cp936') as data:
	with data.cursor() as cur:
		cur.execute(sql.encode('utf8'))
		for row in cur:
			Category.objects.update_or_create(category_name=row[0])

sql = "select distinct(rtrim(spbh)), replace(spmc, ' ', ''), replace(ggxh, ' ', ''), rtrim(jldw), rtrim((select mc from spfl where spfl.fl=spml.spfl_1)) as spfl, rtrim(cksj) from spml where spbh<>'' and spmc<>'' and ggxh<>'' and jldw<>'' and cksj<>'' and (select mc from spfl where spfl.fl=spml.spfl_1)<>''"

with pymssql.connect(host='10.10.136.131', user='sa', password='E53r04', database='ERP', charset='cp936') as data:
	with data.cursor() as cur:
		cur.execute(sql.encode('utf8'))
		for row in cur:
			mod = Mod.objects.get(mod_name=row[2], mod_gram=row[3])
			category = Category.objects.get(category_name=row[4])
			print(row[1], mod, category)
			Commdity.objects.update_or_create(commdity_code=row[0], commdity_name=row[1], commdity_mod=mod, commdity_category=category, commdity_price=row[-1])


