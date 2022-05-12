from distutils.sysconfig import customize_compiler
from django.db import connection
from django.shortcuts import render

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
    with connection.cursor() as cursor:
        cursor.execute("set search_path to cims")
        cursor.execute(f"""SELECT * FROM KATEGORI_APPAREL""")
        row = dictfetchall(cursor)
        print(row)
    context = {'row':row}
    return render(request, 'ka_index.html', context)

