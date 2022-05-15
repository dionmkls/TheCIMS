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
    cursor.execute(f"""SELECT * FROM MENGGUNAKAN_APPAREL AS MA, APPAREL AS A, KOLEKSI_JUAL_BELI AS KJB 
    WHERE MA.Id_Koleksi = A.Id_Koleksi AND MA.Id_Koleksi = KJB.Id_Koleksi;""")
    # cursor.execute(f"""SELECT * FROM MENGGUNAKAN_APPAREL INNER JOIN APPAREL ON MENGGUNAKAN_APPAREL.Id_Koleksi = APPAREL.Id_Koleksi;""")
    row = dictfetchall(cursor)
    print(row)
  context = {'row':row}
  return render(request, 'menggunakan_apparel_index.html', context)

def createMenggunakanApparel(request):
  return render(request, 'create_menggunakan_apparel.html')