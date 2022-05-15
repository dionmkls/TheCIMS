from django.shortcuts import render
from django.db.utils import DatabaseError
from django.http import HttpResponseRedirect, response
from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.
def list_misi_utama(request):
    if "pengguna" in request.session:
        isLogged = True
    else:
        isLogged = False

    if not isLogged:
        return redirect('main:home')

    if request.session['tipe'] == 'Admin':
        with connection.cursor() as cursor:
            cursor.execute("set search_path to cims")
            cursor.execute(
                "SELECT * FROM MISI_UTAMA")
            tokoh = dictfetchall()
            context = {'tokoh': tokoh}

    if request.session['tipe'] == 'Pemain':
        cursor.execute("set search_path to cims")
        cursor.execute("SELECT * FROM MISI_UTAMA")
        tokoh = dictfetchall()
        context = {'tokoh': tokoh}

    return render(request,'index.html',context)

def detailTokoh(request):
    if "pengguna" in request.session:
        isLogged = True
    else:
        isLogged = False

    if not isLogged:
        return redirect('main:home')
        
    if request.method == "POST":
        #username
        nama_misi = request.POST['nama_misi']

    response = {}

    with connection.cursor() as cursor:
        cursor.execute("set search_path to cims")
        cursor.execute(
                "SELECT * FROM MISI WHERE NAMA_MISI =" + nama_misi)
        dm = dictfetchall()

    return render(request, 'misi_utama/detailMisi.html', dm)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
