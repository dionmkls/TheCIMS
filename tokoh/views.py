from django.shortcuts import render
from django.db.utils import DatabaseError
from django.http import HttpResponseRedirect, response
from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.
def readTokoh(request):
    if "pengguna" in request.session:
        isLogged = True
    else:
        isLogged = False

    if not isLogged:
        return redirect('main:home')

    if request.session['tipe'] == 'Admin':
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT Username_pengguna, Nama, Jenis_kelamin, Status, XP, Energi, Kelaparan, Hubungan_sosial, Warna_kulit, Level FROM Tokoh")
            tokoh = dictfetchall()
            context = {'tokoh': tokoh}

    if request.session['tipe'] == 'Pemain':
        var = request.session.get("pengguna")

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT Username_pengguna, Nama, Jenis_kelamin, Status, XP, Energi, Kelaparan, Hubungan_sosial, Warna_kulit, Level FROM Tokoh where"+ var +"= username_pengguna")
            tokoh = dictfetchall()
            context = {'tokoh': tokoh}

    return render(request,'index.html',context)

def detailTokoh(request):
    if not (request.session.get("pengguna", False)):
        return redirect("main/home.html")
        
    if request.method == "POST":
        #username
        uname = request.POST['uname']
        #nama
        nama = request.POST['nama']

    response = {}

    with connection.cursor() as cursor:
        #Nama
        response['nama'] = nama
        #ID rambut
        cursor.execute(
                "SELECT Id_rambut FROM Tokoh WHERE Username_pengguna =" + uname + "AND nama ="+nama)
        response['idrambut'] = dictfetchall()
    
        #ID mata
        cursor.execute(
                "SELECT Id_mata Tokoh WHERE Username_pengguna =" + uname + "AND nama ="+nama)
        response['idmata'] = dictfetchall()

        #ID rumah
        cursor.execute(
                "SELECT Id_rumah Tokoh WHERE Username_pengguna =" + uname + "AND nama ="+nama)
        response['idrumah'] = dictfetchall()

        #warna kulit
        cursor.execute(
                "SELECT warna_kulit Tokoh WHERE Username_pengguna =" + uname + "AND nama ="+nama)
        response['warnaKulit'] = dictfetchall()

        #pekerjaan
        cursor.execute(
                "SELECT pekerjaan Tokoh WHERE Username_pengguna =" + uname + "AND nama ="+nama)
        response['idmata'] = dictfetchall()

    return render(request, 'tokoh/detailTokoh.html', response)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
