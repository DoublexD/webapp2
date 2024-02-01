from sqlalchemy.sql import text
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# QUERY SELECT id_apteki FROM `API NFZ` WHERE id_apteki LIKE 'NFZ41241';

#class YourModel(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    id_apteki = db.Column(db.String(255), unique=True, nullable=False)

login = 'apteka'
password = 'aketpa'
debugging = 'debugging' # production
ip = '135.125.155.141' #ip here or 4.tcp.eu.ngrok.io:17440
#ip = '192.168.1.14'

is_debug = True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{login}:{password}@{ip}/{debugging}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def query_login(user_id):
    query = text("SELECT id_apteki FROM `API NFZ` WHERE id_apteki LIKE :user_id;")
    try:
        # Execute the query
        result = db.session.execute(query, {'user_id': f'%{user_id}%'})

        # Fetch the data
        data = result.fetchall()
        if(is_debug):
            print(data[0][0])
        if user_id == str(data[0][0]):
            return True
        else:
            return False

    except Exception as e:
        # Handle exceptions
        print(f"Error executing query: {e}")
        return "An error occurred"

def query_password(user_passsword):
    query = text("SELECT password FROM `API NFZ` WHERE password LIKE :user_passsword;")
    try:
        # Execute the query
        result = db.session.execute(query, {'user_passsword': f'%{user_passsword}%'})

        # Fetch the data
        data = result.fetchall()
        if(is_debug):
            print(data[0][0])
        if user_passsword == str(data[0][0]):
            #print(data_psswrd)
            return True
        else:
            return False

    except Exception as e:
        # Handle exceptions
        print(f"Error executing query: {e}")
        return "An error occurred"
    
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
    # Zapytanie do bazy danych o interakcje dla wybranych leków
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

    # Assuming the logic that if both medicines have the same interaction_id, there's an interaction
    if interactions and interactions[0][0] == interactions[0][1]:
        # There's an interaction, return the description
        return [interactions[0][0]]
    else:
        # No interaction found, return empty list or a message indicating no interaction
        return ["Brak interakcji."]
    
def query_precriptions(pesel = None, access_key = None):
    if pesel is None and access_key is None:
        return [], False  # Return an empty list and False when both parameters are missing
    else:
        query = text("SELECT * FROM `e-recepty`.`recepty_zbiorcze` WHERE kod_dostepu LIKE :access_key AND pesel = :pesel;")
        result = db.session.execute(query, {'access_key': f'%{access_key}%', 'pesel': pesel})
        rows = result.fetchall()
        if not rows:  # Check if the query returned any rows
            return [], False  # Return an empty list and False if no rows were found

        id_recepty_zbiorczej = [row[0] for row in rows]
        data_array = []
        for id_recepty in id_recepty_zbiorczej:
            query = text("SELECT `nazwa_leku`, `ilosc_opakowan`, `ilosc_tabletek`, `dawka`, `odplatnosc` FROM `e-recepty`.`recepty_jed` WHERE id_recepty_zbiorczej LIKE :id_recepty_zbiorczej;")
            result = db.session.execute(query, {'id_recepty_zbiorczej': f'%{id_recepty}%'})
            data = result.fetchall()
            data_array.append(data)
        
        return data_array, True
    #SELECT * FROM `recepty_zbiorcze` WHERE kod_dostepu = 1111 AND pesel = 10121230121;    
    #query = text("SELECT * FROM `e-recepty`.`recepty_jed`;")
    #query = text("SELECT * FROM `e-recepty`.`recepty_jed`;")
    #try:
    #    result = db.session.execute(query)
    #    data = result.fetchall()
    #    print(data)
    #    return data
    #except Exception as e:
    #    print(f"Error executing query: {e}")
    #    return "An error occurred"

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





def sell_meds(nazwa_leku = None, dawka = None, ilosc_opakowan = None):
    try:
        query = text("SELECT * FROM `leki` WHERE `nazwa_leku` LIKE :nazwa_leku AND 'dawka' LIKE :dawka;")
        result = db.session.execute(query, {'nazwa_leku': nazwa_leku, 'dawka': f'%{dawka}%'})
        current_stock = int(rows[0][3])
        print("ID STOCK " + str(current_stock))
        query = text("SELECT `id_paragonu` FROM `historia_sprzedaz`.`historia_sprzedazy_leku`")
        result = db.session.execute(query)
        rows = result.fetchall()
        id_paragonu_last = int(rows[0][0])
        print("ID PARAGONU " + str(id_paragonu_last))


        query = text("INSERT INTO `historia_sprzedaz`.`historia_sprzedazy_leku` (`id_sprzedazy_leku`, `nazwa_leku`, `ilosc_opakowan`, `dawka_leku`, `data_sprzedazy`, `id_paragonu`) VALUES (NULL, :nazwa_leku, :ilosc_opakowan, :dawka_leku, CURDATE(), :id_paragonu);")
        result = db.session.execute(query, {'nazwa_leku': nazwa_leku, 'dawka_leku' : dawka, 'ilosc_opakowan' : ilosc_opakowan, 'id_paragonu' : str(id_paragonu_last+1)})
        

        if current_stock < int(ilosc_opakowan):
            raise Exception("Niewystarczająca ilość leków na stanie")

        new_stock = current_stock - ilosc_opakowan
        query = text("UPDATE `leki` SET `Ilosc_opakowan` = :new_stock WHERE `nazwa_leku` LIKE :nazwa_leku AND `dawka_leku` LIKE :dawka;")
        db.session.execute(query, {'new_stock': new_stock, 'nazwa_leku':nazwa_leku})
        db.session.commit()

        print(f"Sprzedano {ilosc_opakowan} tabletek leku o ID {nazwa_leku}.")

    except Exception as e:
        print("Błąd podczas sprzedaży leku:", str(e))

def sell_history():
    query = text("SELECT * FROM `historia_sprzedaz`.`historia_sprzedazy_leku`;")
    try:
        result = db.session.execute(query)
        data = result.fetchall()
        return data
    except Exception as e:
        print(f"Error executing query: {e}")
        return "An error occurred"