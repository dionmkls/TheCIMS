from django.db.utils import DatabaseError
from django.shortcuts import redirect, render
from django.db import connection
from django.contrib import messages


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

    # for i in range(len(xyz)):
    #   z = xyz[i]
    #   y = z.get("nama")
    #   print(y)

    if(tipe == 'Admin'):
      cursor.execute("set search_path to cims")
      cursor.execute(f"""SELECT * FROM koleksi_tokoh;""")
      row = dictfetchall(cursor)

    else:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""select username_pengguna, nama_tokoh, id_koleksi
      from koleksi_tokoh where username_pengguna='Soekarno' and id_koleksi not in(
      select id_koleksi from koleksi_jual_beli);""")
      tdkdihapus =dictfetchall(cursor)

      cursor.execute(f"""select tokoh.username_pengguna, nama,  id_rumah,  id_barang, id_koleksi as id_apparel
      from tokoh
      left join menggunakan_apparel ma on tokoh.username_pengguna = ma.username_pengguna and tokoh.nama = ma.nama_tokoh
      left join menggunakan_barang mb on tokoh.username_pengguna = mb.username_pengguna and tokoh.nama = mb.nama_tokoh
      where tokoh.username_pengguna ='{uName}';""")

      dipakai = dictfetchall(cursor)
      cursor.execute(f"""select username_pengguna, nama_tokoh,id_koleksi
      from koleksi_tokoh where username_pengguna='{uName}';""")
      semua = dictfetchall(cursor)
    
      hasil = []
      bukan = []
      for i in range(len(semua)):
        for j in range(len(dipakai)):
          if semua[i].get('nama_tokoh') == dipakai[j].get('nama'):
            if semua[i].get('id_koleksi') == dipakai[j].get('id_rumah') or semua[i].get('id_koleksi') == dipakai[j].get('id_barang')or  semua[i].get('id_koleksi') == dipakai[j].get('id_apparel'):
              if semua[i] in bukan:
                continue
              else:
                bukan.append(semua[i])
            else:
              if semua[i] in hasil:
                continue
              else:
                hasil.append(semua[i])
  context = {'hasil':hasil, 'bukan':bukan, 'tdkdihapus':tdkdihapus}
  return render(request, 'kt_index.html', context)

def createKoleTokoh(request):
  uName = request.session.get("pengguna")
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False
  if not isLogged:
    return redirect('main:home')
  if request.session["tipe"] == 'Admin':
    return redirect('main:home')
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""select nama from tokoh where username_pengguna='{uName}';""")
    tokoh = dictfetchall(cursor)
    cursor.execute(f"""select id from koleksi;""")
    kole = dictfetchall(cursor)
    context = {'tokoh':tokoh, 'kole':kole}

    if request.method == 'POST':
      nama = request.POST["tokohNama"]
      kid = request.POST["k_id"]
      try:
        cursor.execute(f"""insert into koleksi_tokoh values('{kid}', '{uName}', '{nama}')""")
      except DatabaseError:
        messages.add_message(request, messages.WARNING, f"Koin Anda tidak cukup")      
      return redirect('koleksi_tokoh:index')
  return render(request, 'create_kt.html', context)



def delKoleTokoh(request, namatokoh, id):
  uName = request.session.get("pengguna")
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""delete from koleksi_tokoh where nama_tokoh='{namatokoh}'
    and username_pengguna = '{uName}' and id_koleksi = '{id}' """)
    return redirect('koleksi_tokoh:index')
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]