# from django.shortcuts import render
# from django.db.utils import DatabaseError
# from django.http import HttpResponseRedirect, response
# from django.shortcuts import render, redirect
# from django.db import connection

# # Create your views here.
# def readTokoh(request):
#     if "pengguna" in request.session:
#         isLogged = True
#     else:
#         isLogged = False

#     if not isLogged:
#         return redirect('main:home')

    # if request.session['tipe'] == 'Admin':
    #     with connection.cursor() as cursor:
    #         cursor.execute("set search_path to cims")
    #         cursor.execute(
    #             "SELECT Username_pengguna, Nama, Jenis_kelamin, Status, XP, Energi, Kelaparan, Hubungan_sosial, Warna_kulit, Level FROM Tokoh")
    #         tokoh = dictfetchall()
    #         context = {'tokoh': tokoh}

#     if request.session['tipe'] == 'Pemain':
#         var = request.session.get("pengguna")

#         with connection.cursor() as cursor:
#             cursor.execute("set search_path to cims")
#             cursor.execute(
#                 "SELECT Username_pengguna, Nama, Jenis_kelamin, Status, XP, Energi, Kelaparan, Hubungan_sosial, Warna_kulit, Level FROM Tokoh WHERE"+ var +"= username_pengguna")
#             tokoh = dictfetchall()
#             context = {'tokoh': tokoh}

#     return render(request,'tokoh/list_tokoh.html',context)

# def detailTokoh(request):
#     if "pengguna" in request.session:
#         isLogged = True
#     else:
#         isLogged = False

#     if not isLogged:
#         return redirect('main:home')
        
#     if request.method == "POST":
#         #username
#         uname = request.POST['uname']
#         #nama
#         nama = request.POST['nama']

#     response = {}

#     with connection.cursor() as cursor:
#         #Nama
#         response['nama'] = nama
#         #ID rambut
#         cursor.execute("set search_path to cims")
#         cursor.execute(
#                 "SELECT Id_rambut FROM Tokoh WHERE Username_pengguna =" + uname + "AND nama ="+nama)
#         response['idrambut'] = dictfetchall()
    
#         #ID mata
#         cursor.execute(
#                 "SELECT Id_mata Tokoh WHERE Username_pengguna =" + uname + "AND nama ="+nama)
#         response['idmata'] = dictfetchall()

#         #ID rumah
#         cursor.execute(
#                 "SELECT Id_rumah Tokoh WHERE Username_pengguna =" + uname + "AND nama ="+nama)
#         response['idrumah'] = dictfetchall()

#         #warna kulit
#         cursor.execute(
#                 "SELECT warna_kulit Tokoh WHERE Username_pengguna =" + uname + "AND nama ="+nama)
#         response['warnaKulit'] = dictfetchall()

#         #pekerjaan
#         cursor.execute(
#                 "SELECT pekerjaan Tokoh WHERE Username_pengguna =" + uname + "AND nama ="+nama)
#         response['idmata'] = dictfetchall()

#     return render(request, 'tokoh/detailTokoh.html', response)

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

  if request.session['tipe'] == 'Admin':
    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""SELECT Username_pengguna, Nama, Jenis_kelamin, Status, XP, Energi, Kelaparan, Hubungan_sosial, Level FROM Tokoh;""")
      
      tokoh = dictfetchall(cursor)

    context = {'tokoh': tokoh}

  if request.session['tipe'] == 'Pemain':
    var = request.session.get("pengguna")
    print(var)

    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"""SELECT Nama, Jenis_kelamin, Status, XP, Energi, Kelaparan, Hubungan_sosial, Level FROM Tokoh WHERE Username_pengguna = '{var}';""")
      
      tokoh = dictfetchall(cursor)

    context = {'tokoh': tokoh}

  return render(request, 'tokoh_index.html', context)

def detailTokoh(request):
  if "pengguna" in request.session:
    isLogged = True
  else:
    isLogged = False

  if not isLogged:
    return redirect('main:home')
        
#   if request.method == "POST":
#     #username
#     uname = request.POST['uname']
#     #nama
#     nama = request.POST['nama']

    # response = {}
  var = request.session.get("pengguna")

  with connection.cursor() as cursor:
    # var = request.session['nama']
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT nama, id_rambut, id_mata, id_rumah, warna_kulit, pekerjaan 
    FROM Tokoh 
    WHERE Username_pengguna = '{var}';""")
      
    tokoh = dictfetchall(cursor)
    print(tokoh)

  context = {'tokoh': tokoh}
  print(context)
        # #Nama
        # response['nama'] = nama
        # #ID rambut
        # cursor.execute("set search_path to cims")
        # cursor.execute(
        #         f"""SELECT Id_rambut FROM Tokoh WHERE Username_pengguna = '{uname}' AND nama = '{nama}';""")
        # response['idrambut'] = dictfetchall(cursor)
    
        # #ID mata
        # cursor.execute(
        #         f"""SELECT Id_mata FROM Tokoh WHERE Username_pengguna = '{uname}' AND nama = '{nama}';""")
        # response['idmata'] = dictfetchall(cursor)

        # #ID rumah
        # cursor.execute(
        #         f"""SELECT Id_rumah FROM Tokoh WHERE Username_pengguna = '{uname}' AND nama = '{nama}';""")
        # response['idrumah'] = dictfetchall(cursor)

        # #warna kulit
        # cursor.execute(
        #         f"""SELECT warna_kulit FROM Tokoh WHERE Username_pengguna = '{uname}' AND nama = '{nama}';""")
        # response['warnaKulit'] = dictfetchall(cursor)

        # #pekerjaan
        # cursor.execute(
        #         f"""SELECT pekerjaan FROM Tokoh WHERE Username_pengguna = '{uname}' AND nama = '{nama}';""")
        # response['idmata'] = dictfetchall(cursor)

  return render(request, 'detail_tokoh.html', context)

def createTokoh(request):
  if not (request.session.get("pengguna", False)):
      return redirect("main:index")

  response = {}
  with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      cursor.execute(f"SELECT kode FROM WARNA_KULIT;")
      warnak = dictfetchall(cursor)
      response['warnak'] = warnak
      cursor.execute("set search_path to public")
    
#   if request.method == "POST":
#     with connection.cursor() as cursor:
#         cursor.execute("set search_path to sidona")
#         try:
#             komorbid = request.POST.get('komorbid')
#             cursor.execute(f"""
#                 INSERT INTO KOMORBID (idPD, komorbid) VALUES
#                 ('{request.POST['idpd']}', '{komorbid}')
#                 """)
#             return redirect("penyakit_komorbid:index")
#         except:
#             messages.add_message(request, messages.WARNING, f"Terdapat gangguan, mohon mencoba kembali")
#         cursor.execute("set search_path to public")

  return render(request, 'create_tokoh.html', response)