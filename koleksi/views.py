from multiprocessing import context
from wsgiref.util import request_uri
from django.db import connection
from django.shortcuts import redirect, render

# Create your views here.
def index(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  return render(request, 'k_index.html')

def menu_koleksi(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  return render(request, 'menu_list_koleksi.html')

def list_rambut(request):
  print("cek")
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT id, harga, tipe FROM koleksi k , rambut r 
    where k.id = r.id_koleksi;""")
    row = dictfetchall(cursor)
  context = {'row':row}
  return render(request, 'list_rambut.html', context)

def list_mata(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT * FROM koleksi k , mata m
                    where k.id = m.id_koleksi;""")
    row = dictfetchall(cursor)
  context = {'row':row}
  return render(request, 'list_mata.html', context)

def list_rumah(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT distinct * FROM koleksi k , rumah r, koleksi_jual_beli kjb
    where k.id = r.id_koleksi and k.id = kjb.id_koleksi;""")
    row = dictfetchall(cursor)
  context = {'row':row}
  return render(request, 'list_rumah.html', context)

def list_barang(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT distinct * FROM koleksi k , barang b , koleksi_jual_beli kjb
    where k.id = b.id_koleksi and k.id = kjb.id_koleksi;""")
    row = dictfetchall(cursor)
  context = {'row':row}
  return render(request, 'list_barang.html', context)

def list_apparel(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT distinct * FROM koleksi k , apparel a , koleksi_jual_beli kjb
    where k.id = a.id_koleksi and k.id = kjb.id_koleksi;""")
    row = dictfetchall(cursor)
  context = {'row':row}
  return render(request, 'list_apparel.html', context)



def buatKoleksi(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  return render(request,'k_create_page.html')

def buatAppa(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  return render(request, 'create_apparel.html')

def buatBar(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  return render(request, 'create_barang.html')

def buatMat(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  return render(request, 'create_mata.html')

def buatRam(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  return render(request, 'create_rambut.html')

def buatRum(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  return render(request, 'create_rumah.html')


def updaAppa(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  return render(request, 'update_apparel.html')

def updaBar(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  return render(request, 'update_barang.html')

def updaMat(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  return render(request, 'update_mata.html')

def updaRam(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  return render(request, 'update_rambut.html')


def updaRum(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  return render(request, 'update_rumah.html')

















def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]