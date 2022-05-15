from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection

# Create your views here.


def index(request):
    # Check apakah sudah logged in, bila iya redirect ke landing
    print("cek")
    if request.session.get("pengguna", False):
        return redirect("main:home")
    print(request)

    if request.method == "POST":
        print("post")
        is_found = False  # Akun ditemukan
        tipe_login = None  # Admin / Pemain
        password = None
        authentic = False  # Password benar
        print(request)
        with connection.cursor() as cursor:
            cursor.execute("set search_path to cims")
            # Check apakah Admin

            cursor.execute(f"""SELECT * FROM AKUN
                NATURAL JOIN ADMIN
                WHERE username = '{request.POST["username"]}'""")
            row = cursor.fetchall()
            print(row)
            if (len(row) != 0):
                print("admin")
                is_found = True
                tipe_login = 'Admin'
                password = row[0][1]
                username = row[0][0]

            # Check apakah Pemain
            cursor.execute(f"""SELECT * FROM AKUN
                NATURAL JOIN PEMAIN
                WHERE username = '{request.POST["username"]}'""")
            row = cursor.fetchall()

            if (len(row) != 0):
                print("pemain")
                is_found = True
                tipe_login = 'Pemain'
                password = row[0][2]
                username = row[0][0]

            if is_found:
                print("ada akun")
                print(password)
                reqpass = f'{request.POST["password"]}'
                print(reqpass)
                if (password == reqpass):
                    authentic = True
                    print('berhasil login')
                else:
                    # Handler bila password salah
                    messages.add_message(
                        request, messages.WARNING, f"Password salah, silahkan coba lagi")

            # Handler bila berhasil login
            if authentic:
                cursor.execute("set search_path to public")
                request.session["pengguna"] = username
                request.session["tipe"] = tipe_login
                return redirect("../")

            # Handler bila tidak ditemukan usernamenya
            if (not is_found):
                messages.add_message(
                    request, messages.WARNING, f"Login gagal, username tidak ditemukan silahkan coba lagi")

            cursor.execute("set search_path to public")
    return render(request, 'login/index.html')


def logout(request):
    # Hilangkan semua dari session
    request.session.flush()

    return redirect("main:home")
