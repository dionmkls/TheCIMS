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
  if not (request.session.get("pengguna", False)):
    return redirect("main:index")
    
  if request.method == "POST":
    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      try:
          level = request.POST.get('level')
          xp = request.POST.get('xp')
          print(level)
          print(xp)
          cursor.execute(f"""
          INSERT INTO LEVEL (level, xp) VALUES
          ('{level}', '{xp}')
          """)
          print("masuk")
          return redirect("level:index")
      except:
          print("ga masuk")
          messages.add_message(request, messages.WARNING, f"Terdapat gangguan, mohon mencoba kembali")
      cursor.execute("set search_path to public")

  return render(request, 'create_level.html')

def updateLevel(request, level):
  if not (request.session.get("pengguna", False)):
    return redirect("main:index")
  
  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""SELECT xp FROM LEVEL
    WHERE level = '{level}';""")
    awal = dictfetchall(cursor)
    print(awal)
    response = {'awal':awal}

  if request.method == 'POST':
    xp = request.POST.get('xp')

    print(level)
    print(xp)
    with connection.cursor() as cursor:
      cursor.execute("set search_path to cims")
      try:
          cursor.execute(f"""
          UPDATE LEVEL SET xp = '{xp}' WHERE level = '{level}'
          """)
          print("masuk")
          cursor.execute("set search_path to public")
          return redirect("level:index")
      except:
          print("ga masuk")
          messages.add_message(request, messages.WARNING, f"Terdapat gangguan, mohon mencoba kembali")
      cursor.execute("set search_path to public")

  return render(request, 'update_level.html', response)

def deleteLevel(request, level, xp):
  if not (request.session.get("pengguna", False)):
    return redirect("main:index")

  with connection.cursor() as cursor:
    cursor.execute("set search_path to cims")
    cursor.execute(f"""
      DELETE FROM LEVEL WHERE level='{level}' AND xp='{xp}'
      """)
    print("berhasil delete")
    cursor.execute("set search_path to public")

    return redirect("level:index")
      
    cursor.execute("set search_path to public")

  return redirect('level:index')