from multiprocessing import context
from wsgiref.util import request_uri
from django.db import connection
from django.shortcuts import redirect, render

# Create your views here.
def list_menjalankan_misi_utama(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  if request.session['tipe'] == 'Admin':
    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute("SELECT * FROM MENJALANKAN_MISI_UTAMA;")
      row = dictfetchall(cursor)
    context = {'row':row}

  if request.session['tipe'] == 'Pemain':
    uname = request.session.get("pengguna")

    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute("SELECT * FROM MAKAN WHERE MENJALANKAN_MISI_UTAMA =" + uname + ";")
      row = dictfetchall(cursor)
    context = {'row':row}

  return render(request, 'list_makan.html', context)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]