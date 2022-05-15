from multiprocessing import context
from wsgiref.util import request_uri
from django.db import connection
from django.shortcuts import redirect, render

# Create your views here.
def list_bekerja(request):
#   print("cek")
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute("SELECT * FROM BEKERJA;")
    row = dictfetchall(cursor)
  context = {'row':row}
  return render(request, 'list_bekerja.html', context)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]