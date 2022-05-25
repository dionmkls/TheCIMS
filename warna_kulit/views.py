from distutils.sysconfig import customize_compiler
from django.db import connection
from django.shortcuts import redirect, render
from django.contrib import messages

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
    cursor.execute(f"""SELECT * FROM WARNA_KULIT 
    WHERE KODE IN (SELECT KODE FROM WARNA_KULIT
    JOIN TOKOH ON WARNA_KULIT.KODE = TOKOH.WARNA_KULIT);""")
    result = dictfetchall(cursor)

    cursor.execute(f"""SELECT * FROM WARNA_KULIT
    WHERE KODE NOT IN (SELECT KODE FROM WARNA_KULIT
    JOIN TOKOH ON WARNA_KULIT.KODE = TOKOH.WARNA_KULIT);""")
    resultx = dictfetchall(cursor)

    print(result)
    print(resultx)
  #   row = dictfetchall(cursor)
  #   print(row)
  # context = {'row':row}
  return render(request, 'warnakulit.html', {'data':result, 'updateable':resultx})

def createWarnaKulit(request):
  if not (request.session.get("pengguna", False)):
    return redirect("main:index")

  response = {}
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"SELECT kode FROM WARNA_KULIT;")
    kode = dictfetchall(cursor)
    response['kode'] = kode
    cursor.execute("set search_path to public")
    
  if request.method == "POST":
    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      try:
          kode = request.POST.get('kode')
          print(kode)
          cursor.execute(f"""
          INSERT INTO WARNA_KULIT (kode) VALUES
          ('{kode}')
          """)
          print("masuk")
          return redirect("warna_kulit:index")
      except:
          print("ga masuk")
          messages.add_message(request, messages.WARNING, f"Terdapat gangguan, mohon mencoba kembali")
      cursor.execute("set search_path to public")
  return render(request, 'create_warna_kulit.html',response)

def deleteWarnaKulit(request, kode):
  if not (request.session.get("pengguna", False)):
    return redirect("main:index")

  print(kode)
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""
      DELETE FROM WARNA_KULIT WHERE kode = '{kode}'
      """)
    print("berhasil delete")
    cursor.execute("set search_path to public")

    return redirect("warna_kulit:index")
      
    cursor.execute("set search_path to public")

  return redirect('warna_kulit:index')