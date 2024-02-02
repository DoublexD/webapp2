from sqlalchemy.sql import text
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



login = 'apteka'
password = 'aketpa'
debugging = 'debugging'
ip = '135.125.155.141'


is_debug = True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{login}:{password}@{ip}/{debugging}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def query_login(user_id):
    query = text("SELECT id_apteki FROM `API NFZ` WHERE id_apteki LIKE :user_id;")
    try:

        result = db.session.execute(query, {'user_id': f'%{user_id}%'})

        data = result.fetchall()
        if(is_debug):
            print(data[0][0])
        if user_id == str(data[0][0]):
            return True
        else:
            return False

    except Exception as e:

        print(f"Error executing query: {e}")
        return False

def query_password(user_passsword):
    query = text("SELECT password FROM `API NFZ` WHERE password LIKE :user_passsword;")
    try:

        result = db.session.execute(query, {'user_passsword': f'%{user_passsword}%'})


        data = result.fetchall()
        if(is_debug):
            print(data[0][0])
        if user_passsword == str(data[0][0]):

            return True
        else:
            return False

    except Exception as e:
        print(f"Error executing query: {e}")
        return False
    
def query_meds():
    query = text("SELECT * FROM `leki`;")
    try:
        result = db.session.execute(query)
        data = result.fetchall()
        return data
    except Exception as e:
        print(f"Error executing query: {e}")
        return "An error occurred"
    
def query_med_list():
    query = text("SELECT DISTINCT nazwa_leku FROM `leki`;") 
    try:
        result = db.session.execute(query)
        data = result.fetchall()
        return data
    except Exception as e:
        print(f"Error executing query: {e}")
        return "An error occurred"
    
def query_interactions(med1, med2):
    query = text("""
        SELECT i1.opis, i2.opis 
        FROM leki l1
        JOIN interakcje i1 ON l1.interakcje_id = i1.id
        JOIN leki l2 ON l2.interakcje_id = i1.id
        JOIN interakcje i2 ON l2.interakcje_id = i2.id
        WHERE l1.nazwa_leku = :med1 AND l2.nazwa_leku = :med2;
    """)
    result = db.session.execute(query, {'med1': med1, 'med2': med2})
    interactions = result.fetchall()

    if interactions and interactions[0][0] == interactions[0][1]:
        return [interactions[0][0]]
    else:
        return ["Brak interakcji."]
    
def query_precriptions(pesel = None, access_key = None):
    if pesel is None and access_key is None:
        return [], False  
    else:
        query = text("SELECT * FROM `e-recepty`.`recepty_zbiorcze` WHERE kod_dostepu LIKE :access_key AND pesel = :pesel;")
        result = db.session.execute(query, {'access_key': f'%{access_key}%', 'pesel': pesel})
        rows = result.fetchall()
        if not rows:  
            return [], False  

        id_recepty_zbiorczej = [row[0] for row in rows]
        data_array = []
        for id_recepty in id_recepty_zbiorczej:
            query = text("SELECT `nazwa_leku`, `ilosc_opakowan`, `ilosc_tabletek`, `dawka`, `odplatnosc` FROM `e-recepty`.`recepty_jed` WHERE id_recepty_zbiorczej LIKE :id_recepty_zbiorczej;")
            result = db.session.execute(query, {'id_recepty_zbiorczej': f'%{id_recepty}%'})
            data = result.fetchall()
            data_array.append(data)
        
        return data_array, True
   

def add_meds(nazwa_leku = None, ilosc_tabletek = None, dawka = None, ilosc_opakowan = None, waznosc = None, cena = None, substancja_czynna = None):
    query = text("SELECT MAX(`id_leku`) FROM `leki`;")
    result = db.session.execute(query)
    rows = result.fetchall()
    id_lek = int(rows[0][0])
    if(is_debug):
        print("Latest ID = " + str(id_lek))
    new_id = id_lek + 1
    if(is_debug):
        print("New ID = " + str(new_id))
    query = text("INSERT INTO `leki` (`id_leku`, `nazwa_leku`, `Ilosc tabletek`, `dawka`, `Ilosc opakowan`, `Waznosc`, `cena`, `Substancja_czynna`) "
                 "VALUES (:id, :nazwa_leku, :ilosc_tabletek, :dawka, :ilosc_opakowan, :waznosc, :cena, :substancja_czynna);")
    parameters = {
        'id': new_id,
        'nazwa_leku': nazwa_leku,
        'ilosc_tabletek': ilosc_tabletek,
        'dawka': dawka,
        'ilosc_opakowan': ilosc_opakowan,
        'waznosc': waznosc,
        'cena': cena,
        'substancja_czynna': substancja_czynna
    }
    result = db.session.execute(query, parameters)
    db.session.commit()


def sell_history():
    query = text("SELECT * FROM `debugging`.`historia_sprzedaz`;")
    try:
        result = db.session.execute(query)
        data = result.fetchall()
        return data
    except Exception as e:
        print(f"Error executing query: {e}")
        return "An error occurred"

def sell_meds(leki_do_sprzedazy):
    for lek in leki_do_sprzedazy:
        id_leku = lek['id_leku']
        ilosc_opakowan = lek['ilosc_opakowan']

        query = text("SELECT `Ilosc opakowan` FROM `debugging`.`leki` WHERE `id_leku` = :id_leku;")
        result = db.session.execute(query, {'id_leku': id_leku})
        lek_info = result.fetchone()
        if lek_info and lek_info[0] >= ilosc_opakowan:
            new_ilosc_opakowan = lek_info[0] - ilosc_opakowan
            update_query = text("UPDATE `debugging`.`leki` SET `Ilosc opakowan` = :new_ilosc_opakowan WHERE `id_leku` = :id_leku;")
            db.session.execute(update_query, {'new_ilosc_opakowan': new_ilosc_opakowan, 'id_leku': id_leku})

            insert_query = text("""
                INSERT INTO `debugging`.`historia_sprzedaz`
                (`nazwa_leku`, `ilosc_opakowan`, `cena`, `dawka`, `data_sprzedazy`) 
                VALUES ((SELECT `nazwa_leku` FROM `leki` WHERE `id_leku` = :id_leku), :ilosc_opakowan, (SELECT `cena` FROM `leki` WHERE `id_leku` = :id_leku), (SELECT `dawka` FROM `leki` WHERE `id_leku` = :id_leku), CURDATE());
            """)
            db.session.execute(insert_query, {'id_leku': id_leku, 'ilosc_opakowan': ilosc_opakowan})

            db.session.commit()
        else:
            print(f"Nie można sprzedać leku o ID {id_leku} w ilości {ilosc_opakowan}. Nie wystarczająca ilość w magazynie.")
            return {"error": "Nie wystarczająca ilość w magazynie."}

    return {"success": "Sprzedaż zakończona sukcesem."}
    