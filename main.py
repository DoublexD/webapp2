from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from db import *
from datetime import date

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("index.html")

@app.route('/przypomnij')
def przypomnij():
    return render_template("przypomnij.html")

@app.route('/process_login', methods=['POST'])
def process_login():
    if request.method == 'POST':
        login_text = request.form.get('login_text')
        password_text = request.form.get('password_text')
        if(is_debug):
            print("login_text : " + login_text)
            print("password_text : " + password_text)

        login_result = query_login(login_text)
        print(login_result)
        password_result = query_password(password_text)
        print(password_result)
        if login_result & password_result:
            #print("Login successful\n")
            return redirect('/apteka')
        else:
            return redirect('/login')
        
@app.route('/historia')
def historia():
    return render_template("historia.html",meds=sell_history())

@app.route('/apteka')
def login_success():
    return render_template("landing.html")

@app.route('/stan')
def stan():
    return render_template("stan.html", meds=query_meds())

@app.route('/recepta', methods=['GET', 'POST'])
def recepta():


    if request.method == 'POST':
        pesel = request.form.get('pesel')
        access_key = request.form.get('kod_dostepu')
        
        meds, data_found = query_precriptions(pesel=pesel, access_key=access_key)
        
        return render_template('erecepty.html', meds=meds, data_found=data_found)
    else:
        return render_template('erecepty.html', data_found=True)


@app.route('/magazyn', methods=['GET', 'POST'])
def magazyn():
    if request.method == 'POST':
        nazwa_leku = request.form.get('nazwa_leku')
        ilosc_tabletek = request.form.get('ilosc_tabletek')
        dawka = request.form.get('dawka')
        ilosc_opakowan = request.form.get('ilosc_opakowan')
        waznosc = request.form.get('waznosc')
        cena = request.form.get('cena')
        substancja_czynna = request.form.get('substancja_czynna')
        if nazwa_leku != None and ilosc_tabletek != None and dawka != None and ilosc_opakowan != None and waznosc != None and cena != None and substancja_czynna != None:
            add_meds(nazwa_leku, ilosc_tabletek, dawka, ilosc_opakowan, waznosc, cena, substancja_czynna)
            return render_template("magazyn.html")
    return render_template("magazyn.html")

@app.route('/zamowienia', methods=['GET', 'POST'])
def zamowienia():
    if request.method == 'POST':
        nazwa_leku = request.form.get('nazwa_leku')
        ilosc_tabletek = request.form.get('ilosc_tabletek')
        dawka = request.form.get('dawka')
        ilosc_opakowan = request.form.get('ilosc_opakowan')
        waznosc = request.form.get('waznosc')
        cena = request.form.get('cena')
        substancja_czynna = request.form.get('substancja_czynna')
        if nazwa_leku != None and ilosc_tabletek != None and dawka != None and ilosc_opakowan != None and waznosc != None and cena != None and substancja_czynna != None:
            add_meds(nazwa_leku, ilosc_tabletek, dawka, ilosc_opakowan, waznosc, cena, substancja_czynna)
            return render_template("zamowienia.html")
    return render_template("zamowienia.html")

@app.route('/sprzedaz', methods=['GET', 'POST'])
def sprzedaz():
    if request.method == 'POST':
        leki_do_sprzedazy = request.get_json()
        print(leki_do_sprzedazy)
        sell_meds(leki_do_sprzedazy)
        return render_template("sprzedaz.html", meds=query_meds())
    else:
        return render_template("sprzedaz.html", meds=query_meds())

@app.route('/sprzedaz_koszyk', methods=['GET', 'POST'])
def sprzedaz_koszyk():
    if request.method == 'POST':
        leki_do_sprzedazy = request.get_json()
        print(leki_do_sprzedazy)
        sell_meds(leki_do_sprzedazy)
        return jsonify({"success": True})
        

@app.route('/interakcje')
def interakcje_list():
    return render_template("interakcje.html", leki=query_med_list())

@app.route('/interakcje', methods=['GET', 'POST'])
def interakcje():
    if request.method == 'POST':
        med1_id = request.form.get('firstMedicine')
        med2_id = request.form.get('secondMedicine')

        interaction_messages = query_interactions(med1_id, med2_id)
        interaction_result = " ".join(interaction_messages) if interaction_messages else "Brak interakcji."

        leki = query_med_list()
        return render_template("interakcje.html", leki=leki, interaction_result=interaction_result)
    else:
        leki = query_med_list()
        return render_template("interakcje.html", leki=leki, interaction_result=interaction_messages)



    
if __name__ == '__main__':
    app.run(debug=True)
