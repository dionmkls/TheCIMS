
from django.shortcuts import redirect, render
from django.db import connection


# Create your views here.
def index(request):

  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  with connection.cursor() as cursor:

    uName = request.session.get("pengguna")
    tipe = request.session.get("tipe")

    if(tipe == 'admin'):
      cursor.execute("set search_path to cims")
      cursor.execute(f"""SELECT * FROM koleksi_tokoh;""")
      row = dictfetchall(cursor)

    else:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""SELECT * FROM koleksi_tokoh
      where username_pengguna ='{uName}'""")
      row = dictfetchall(cursor)

  context = {'row':row}
  return render(request, 'kt_index.html', context)

def createKoleTokoh(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False
  if not isLogged:
    return redirect('main:home')
  if request.session["tipe"] == 'Admin':
    return redirect('main:home')
  return render(request, 'create_kt.html')

  
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]