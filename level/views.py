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

  # with connection.cursor() as cursor:
  #   cursor.execute("set search_path to cims")
  #   cursor.execute(f"""SELECT * FROM LEVEL""")
  #   row = dictfetchall(cursor)
  #   print(row)
  # context = {'row':row}
  # return render(request, 'level_index.html', context)

  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT * FROM LEVEL AS L
    WHERE L.level IN (SELECT LV.level FROM LEVEL AS LV
    JOIN TOKOH ON LV.level = TOKOH.level);""")
    result = dictfetchall(cursor)

    cursor.execute(f"""SELECT * FROM LEVEL AS L 
    WHERE L.level NOT IN (SELECT LV.level FROM LEVEL AS LV
    JOIN TOKOH ON LV.level = TOKOH.level);""")
    resultx = dictfetchall(cursor)

    print(result)
    print(resultx)
  #   row = dictfetchall(cursor)
  #   print(row)
  # context = {'row':row}
  return render(request, 'level_index.html', {'data':result, 'updateable':resultx})

def createLevel(request):
    return render(request, 'create_level.html')

def updateLevel(request):
    return render(request, 'update_level.html')