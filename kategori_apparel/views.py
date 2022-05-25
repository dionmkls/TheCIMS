from distutils.sysconfig import customize_compiler
from django.db import connection
from django.shortcuts import redirect, render

# Create your views here.
def dictfetchall(cursor):
  "Returns all rows from a cursor as a dict"
  desc = cursor.description
  return [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
  ]

def index(request):
  print("cek")
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')

  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""select *
      from kategori_apparel
      where nama_kategori in(
      select nama_kategori
      from kategori_apparel
      join apparel a on kategori_apparel.nama_kategori = a.kategori_apparel);""")
    row = dictfetchall(cursor)

    cursor.execute(f"""select *
      from kategori_apparel
      where nama_kategori not in(
      select nama_kategori
      from kategori_apparel
      join apparel a on kategori_apparel.nama_kategori = a.kategori_apparel);""")
    rows = dictfetchall(cursor)
  context = {'row':row, 'rows':rows}
  return render(request, 'ka_index.html', context)

def createKa(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
  if request.session["tipe"] == "Pemain":
    return redirect('main:home')

  if request.method == 'POST':
    print("Post")
    temp = list()
    nama = request.POST["categoryname"]
    temp.append(nama)
    cekNama = tuple(temp)
    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""select * from kategori_apparel""")
      row = cursor.fetchall()
      print(row)
      if cekNama not in row:
        print(nama)
        cursor.execute(f"""insert into kategori_apparel values('{nama}')""")
        return redirect('kategori_apparel:index')
  return render(request, 'ka_create.html')
def deleteKa(request,namakategori):
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""delete from kategori_apparel where nama_kategori='{namakategori}' """)
    return redirect('kategori_apparel:index')

