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
    cursor.execute(f"""select id, harga, tipe from rambut join koleksi k on k.id = rambut.id_koleksi
    where id in(
    select distinct id_rambut from tokoh
    union select distinct id from koleksi_tokoh join rambut r on koleksi_tokoh.id_koleksi = r.id_koleksi
    );""")
    row = dictfetchall(cursor)
    cursor.execute(f"""select id, harga, tipe from rambut join koleksi k on k.id = rambut.id_koleksi
    where id not in(
    select distinct id_rambut from tokoh
    union select distinct id from koleksi_tokoh join rambut r on koleksi_tokoh.id_koleksi = r.id_koleksi
    );""")
    rows = dictfetchall(cursor)
  context = {'row':row, 'rows':rows}
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
    cursor.execute(f"""select id, warna, harga from mata join koleksi k on k.id = mata.id_koleksi
    where id in(select distinct id_mata from tokoh union
    select distinct m.id_koleksi from koleksi_tokoh join mata m on koleksi_tokoh.id_koleksi = m.id_koleksi);""")
    row = dictfetchall(cursor)
    cursor.execute(f"""select id, warna, harga from mata join koleksi k on k.id = mata.id_koleksi
    where id not in(select distinct id_mata from tokoh union
    select distinct m.id_koleksi from koleksi_tokoh join mata m on koleksi_tokoh.id_koleksi = m.id_koleksi);""")
    rows = dictfetchall(cursor)
  context = {'row':row, 'rows':rows}
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
    cursor.execute(f"""select id, harga, harga_beli, kapasitas_barang, nama from rumah
    join koleksi_jual_beli kjb on kjb.id_koleksi = rumah.id_koleksi
    join koleksi k on k.id = kjb.id_koleksi
    where id in(
    select distinct id_rumah from tokoh union
    select distinct r.id_koleksi from koleksi_tokoh join rumah r on koleksi_tokoh.id_koleksi = r.id_koleksi
    );""")
    row = dictfetchall(cursor)
    cursor.execute(f"""select id, harga, harga_beli, kapasitas_barang, nama from rumah
    join koleksi_jual_beli kjb on kjb.id_koleksi = rumah.id_koleksi
    join koleksi k on k.id = kjb.id_koleksi
    where id not in(
    select distinct id_rumah from tokoh union
    select distinct r.id_koleksi from koleksi_tokoh join rumah r on koleksi_tokoh.id_koleksi = r.id_koleksi
    );""")
    rows = dictfetchall(cursor)
  context = {'row':row, 'rows':rows}
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
    cursor.execute(f"""select id, tingkat_energi, harga_beli, nama,  harga from barang
    join koleksi_jual_beli kjb on kjb.id_koleksi = barang.id_koleksi
    join koleksi k on k.id = kjb.id_koleksi
    where id in (
    select distinct id_barang from menggunakan_barang union
    select distinct b.id_koleksi from barang b join koleksi_tokoh kt on b.id_koleksi = kt.id_koleksi);""")
    row = dictfetchall(cursor)
    cursor.execute(f"""select id, tingkat_energi, harga_beli, nama,  harga from barang
    join koleksi_jual_beli kjb on kjb.id_koleksi = barang.id_koleksi
    join koleksi k on k.id = kjb.id_koleksi
    where id not in (
    select distinct id_barang from menggunakan_barang union
    select distinct b.id_koleksi from barang b join koleksi_tokoh kt on b.id_koleksi = kt.id_koleksi);""")
    rows = dictfetchall(cursor)
  context = {'row':row, 'rows':rows}
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
    cursor.execute(f"""select id,nama_pekerjaan,kategori_apparel,warna_apparel,harga_beli,nama, harga
    from apparel join koleksi_jual_beli kjb on kjb.id_koleksi = apparel.id_koleksi  join koleksi k on k.id = kjb.id_koleksi
    where id in(
    select distinct id_koleksi from menggunakan_apparel union select distinct id
    from apparel join koleksi_tokoh kt on apparel.id_koleksi = kt.id_koleksi); """)
    rows = dictfetchall(cursor)
    cursor.execute(f"""select id,nama_pekerjaan,kategori_apparel,warna_apparel,harga_beli,nama, harga
    from apparel join koleksi_jual_beli kjb on kjb.id_koleksi = apparel.id_koleksi join koleksi k on k.id = kjb.id_koleksi
    where id not in(
    select distinct id_koleksi from menggunakan_apparel union
    select distinct id from apparel join koleksi_tokoh kt on apparel.id_koleksi = kt.id_koleksi);""")
    row = dictfetchall(cursor)
  context = {'row':row, 'rows':rows}
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
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute("select id_koleksi from apparel order by id_koleksi desc limit 1")
    idMat = dictfetchall(cursor)
    x = idMat[0]
    y = x.get("id_koleksi")
    print(y)
    z = int(y[2:])+1
    print(z)
    id = f"AP{z:03d}"
    print(id)
    cursor.execute("select nama_kategori from kategori_apparel")
    rows = dictfetchall(cursor)
    cursor.execute("select nama from pekerjaan")
    row = dictfetchall(cursor)
    context = {'id':id, 'rows':rows, 'row':row}

  if request.method == 'POST':
    print("Post")
    id = request.POST["apparelId"]
    nama = request.POST["nama"]
    hJual = request.POST["jual"]
    hBeli = request.POST["beli"]
    warna = request.POST["warna"]
    kApp = request.POST["kApparel"]
    pekerjaan = request.POST["pekerjaan"]

    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""insert into koleksi values('{id}','{hJual}')""")
      cursor.execute(f"""insert into koleksi_jual_beli values('{id}','{hBeli}', '{nama}')""")
      cursor.execute(f"""insert into apparel values('{id}','{pekerjaan}','{kApp}','{warna}')""")
      return redirect('koleksi:list_apparel')
  return render(request, 'create_apparel.html', context)

def buatBar(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute("select id_koleksi from barang order by id_koleksi desc limit 1")
    idMat = dictfetchall(cursor)
    x = idMat[0]
    y = x.get("id_koleksi")
    print(y)
    z = int(y[2:])+1
    print(z)
    id = f"BR{z:03d}"
    print(id)
    context = {'id':id}

  if request.method == 'POST':
    print("Post")
    id = request.POST["apparelId"]
    nama = request.POST["nama"]
    hJual = request.POST["jual"]
    hBeli = request.POST["beli"]
    energi = request.POST["energi"]

    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""insert into koleksi values('{id}','{hJual}')""")
      cursor.execute(f"""insert into koleksi_jual_beli values('{id}','{hBeli}', '{nama}')""")
      cursor.execute(f"""insert into apparel values('{id}','{energi}')""")
      return redirect('koleksi:list_barang')
  return render(request, 'create_barang.html', context)


def buatMat(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute("select id_koleksi from mata order by id_koleksi desc limit 1")
    idMat = dictfetchall(cursor)
    x = idMat[0]
    y = x.get("id_koleksi")
    print(y)
    z = int(y[2:])+1
    print(z)
    id = f"MT{z:03d}"
    print(id)
    context = {'id':id}

  if request.method == 'POST':
    print("Post")
    id = request.POST["apparelId"]
    hJual = request.POST["jual"]
    warna = request.POST["warna"]

    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""insert into koleksi values('{id}','{hJual}')""")
      cursor.execute(f"""insert into mata values('{id}','{warna}')""")
        
      return redirect('koleksi:list_mata')
  return render(request, 'create_mata.html', context)

def buatRam(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute("select id_koleksi from rambut order by id_koleksi desc limit 1")
    idMat = dictfetchall(cursor)
    x = idMat[0]
    y = x.get("id_koleksi")
    print(y)
    z = int(y[2:])+1
    print(z)
    id = f"RB{z:03d}"
    print(id)
    context = {'id':id}

  if request.method == 'POST':
    print("Post")
    id = request.POST["apparelId"]
    hJual = request.POST["jual"]
    tipe = request.POST["tipe"]

    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""insert into koleksi values('{id}','{hJual}')""")
      cursor.execute(f"""insert into rambut values('{id}','{tipe}')""")
        
      return redirect('koleksi:list_rambut')
  return render(request, 'create_rambut.html', context)

def buatRum(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute("select id_koleksi from rumah order by id_koleksi desc limit 1")
    idMat = dictfetchall(cursor)
    x = idMat[0]
    y = x.get("id_koleksi")
    print(y)
    z = int(y[2:])+1
    print(z)
    id = f"RM{z:03d}"
    print(id)
    context = {'id':id}

  if request.method == 'POST':
    print("Post")
    id = request.POST["apparelId"]
    nama = request.POST["nama"]
    hJual = request.POST["jual"]
    hBeli = request.POST["beli"]
    kapa = request.POST["kapasitas"]

    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""insert into koleksi values('{id}','{hJual}')""")
      cursor.execute(f"""insert into koleksi_jual_beli values('{id}','{hBeli}', '{nama}')""")
      cursor.execute(f"""insert into rumah values('{id}','{kapa}')""")
      return redirect('koleksi:list_rumah')
  return render(request, 'create_rumah.html', context)


def updaAppa(request,id):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""select id,nama_pekerjaan,kategori_apparel,warna_apparel,harga_beli,nama, harga
    from apparel
    join koleksi_jual_beli kjb on kjb.id_koleksi = apparel.id_koleksi
    join koleksi k on k.id = kjb.id_koleksi
    where id = '{id}';""")
    awal = dictfetchall(cursor)
    cursor.execute("select nama_kategori from kategori_apparel")
    rows = dictfetchall(cursor)
    cursor.execute("select nama from pekerjaan")
    row = dictfetchall(cursor)
    print(awal)
    print(rows)
    print(row)
    context = {'awal':awal, 'rows':rows, 'row':row}

  if request.method == "POST":
    id = request.POST["apparelId"]
    nama = request.POST["nama"]
    hJual = request.POST["jual"]
    hBeli = request.POST["beli"]
    warna = request.POST["warna"]
    kApp = request.POST["kApparel"]
    pekerjaan = request.POST["pekerjaan"]
    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""update koleksi set harga = '{hJual}' where id='{id}'""")
      cursor.execute(f"""update koleksi_jual_beli set harga_beli = '{hBeli}' , nama = '{nama}' where id_koleksi = '{id}';""")
      cursor.execute(f"""update apparel set warna_apparel = '{warna}', nama_pekerjaan = '{pekerjaan}', kategori_apparel = '{kApp}' where id_koleksi ='{id}';""")
      return redirect('koleksi:list_apparel')
  return render(request, 'update_apparel.html', context)

def updaBar(request, id):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""select id, tingkat_energi, harga_beli, nama,  harga
    from barang
    join koleksi_jual_beli kjb on kjb.id_koleksi = barang.id_koleksi
    join koleksi k on k.id = kjb.id_koleksi
    where id = '{id}';""")
    awal = dictfetchall(cursor)
    print(awal)
    context = {'awal':awal}

  if request.method == "POST":
    id = request.POST["apparelId"]
    nama = request.POST["nama"]
    hJual = request.POST["jual"]
    hBeli = request.POST["beli"]
    energi = request.POST["energi"]

    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""update koleksi set harga = '{hJual}' where id='{id}'""")
      cursor.execute(f"""update koleksi_jual_beli set harga_beli = '{hBeli}' , nama = '{nama}' where id_koleksi = '{id}';""")
      cursor.execute(f"""update barang set tingkat_energi = '{energi}' where id_koleksi ='{id}';""")
      return redirect('koleksi:list_barang')
  return render(request, 'update_barang.html', context)

def updaMat(request, id):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""select id, warna, harga
    from mata join koleksi k on k.id = mata.id_koleksi
    where id ='{id}';""")
    awal = dictfetchall(cursor)
    print(awal)
    context = {'awal':awal}

  if request.method == "POST":
    id = request.POST["apparelId"]
    warna = request.POST["warna"]
    hJual = request.POST["jual"]

    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""update koleksi set harga = '{hJual}' where id='{id}'""")
      cursor.execute(f"""update barang set warna= {warna} where id_koleksi ='{id}';""")
      return redirect('koleksi:list_mata')
  return render(request, 'update_mata.html', context)

def updaRam(request, id):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""select id, harga, tipe
    from rambut join koleksi k on k.id = rambut.id_koleksi
    where id={id};""")
    awal = dictfetchall(cursor)
    print(awal)
    context = {'awal':awal}

  if request.method == "POST":
    id = request.POST["apparelId"]
    tipe = request.POST["tipe"]
    hJual = request.POST["jual"]

    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""update koleksi set harga = '{hJual}' where id='{id}'""")
      cursor.execute(f"""update barang set tipe={tipe} where id_koleksi ='{id}';""")
      return redirect('koleksi:list_mata')
  return render(request, 'update_rambut.html', context)


def updaRum(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""select id, harga, harga_beli, kapasitas_barang, nama
    from rumah
    join koleksi_jual_beli kjb on kjb.id_koleksi = rumah.id_koleksi
    join koleksi k on k.id = kjb.id_koleksi
    where id  = '{id}';""")
    awal = dictfetchall(cursor)
    print(awal)
    context = {'awal':awal}

  if request.method == "POST":
    id = request.POST["apparelId"]
    nama = request.POST["nama"]
    hJual = request.POST["jual"]
    hBeli = request.POST["beli"]
    kapasitas = request.POST["kapasitas"]

    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""update koleksi set harga = '{hJual}' where id='{id}'""")
      cursor.execute(f"""update koleksi_jual_beli set harga_beli = '{hBeli}' , nama = '{nama}' where id_koleksi = '{id}';""")
      cursor.execute(f"""update rumah set kapasitas_barang = '{kapasitas}' where id_koleksi ='{id}';""")
      return redirect('koleksi:list_rumah')
  return render(request, 'update_rumah.html', context)


def delApp(request,id):
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""delete from koleksi where id ='{id}' """)
    return redirect('koleksi:list_apparel')

def delBar(request,id):
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""delete from koleksi where id ='{id}' """)
    return redirect('koleksi:list_barang')

def delMat(request,id):
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""delete from koleksi where id ='{id}' """)
    return redirect('koleksi:list_mata')

def delRam(request,id):
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""delete from koleksi where id ='{id}' """)
    return redirect('koleksi:list_rambut')

def delRum(request,id):
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""delete from koleksi where id ='{id}' """)
    return redirect('koleksi:list_rumah')












def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]