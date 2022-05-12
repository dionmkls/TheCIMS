from multiprocessing import context
from wsgiref.util import request_uri
from django.db import connection
from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'k_index.html')

def menu_koleksi(request):
  return render(request, 'menu_list_koleksi.html')

def list_rambut(request):
  print("cek")
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT id, harga, tipe FROM koleksi k , rambut r 
    where k.id = r.id_koleksi;""")
    row = dictfetchall(cursor)
  context = {'row':row}
  return render(request, 'list_rambut.html', context)

def list_mata(request):
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT * FROM koleksi k , mata m
                    where k.id = m.id_koleksi;""")
    row = dictfetchall(cursor)
  context = {'row':row}
  return render(request, 'list_mata.html', context)

def list_rumah(request):
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT distinct * FROM koleksi k , rumah r, koleksi_jual_beli kjb
    where k.id = r.id_koleksi and k.id = kjb.id_koleksi;""")
    row = dictfetchall(cursor)
  context = {'row':row}
  return render(request, 'list_rumah.html', context)

def list_barang(request):
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT distinct * FROM koleksi k , barang b , koleksi_jual_beli kjb
    where k.id = b.id_koleksi and k.id = kjb.id_koleksi;""")
    row = dictfetchall(cursor)
  context = {'row':row}
  return render(request, 'list_barang.html', context)

def list_apparel(request):
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT distinct * FROM koleksi k , apparel a , koleksi_jual_beli kjb
    where k.id = a.id_koleksi and k.id = kjb.id_koleksi;""")
    row = dictfetchall(cursor)
  context = {'row':row}
  return render(request, 'list_apparel.html', context)









def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]