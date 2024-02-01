let is_debug = true;
let cart_size = 0;
let cart_id_array = [];

function zmniejszIloscWMagazynie(id) {
    let id_l = id - 1;
    let medsTable = document.querySelector('.magazyn table tbody');
    for (let i = 0; i < medsTable.rows.length; i++) {
        if (i == parseInt(id_l)) {
            let meds_quantity = parseInt(medsTable.rows[i].cells[3].innerText);
            if (meds_quantity > 0) {
                medsTable.rows[i].cells[3].innerText = (meds_quantity - 1).toString();
            }
            break;
        }
    }
}

function zwrocDoMagazynu(id) {
    let id_l = id - 1;

}

function dodajDoKoszyka(id, nazwa, ilosc, dawka, ilosc_opakowan, waznosc, cena) {
    console.log(ilosc_opakowan);
    let id_l = id - 1;
    if (is_debug) {
        console.log(id_l);
    }
    let cartTable = document.getElementById('tabelaKoszyk').getElementsByTagName('tbody')[0];
    let medsTable = document.querySelector('.magazyn table tbody');
    for (let i = 0; i < cart_size; i++) {
        if (cart_id_array[i] == id_l) {
            zmniejszIloscWMagazynie(id);
            let med_quantity_buffer = parseInt(cartTable.rows[i].cells[3].innerText) + 1;
            if (med_quantity_buffer > 0) {
                cartTable.rows[i].cells[3].innerText = (med_quantity_buffer).toString();
                return;
            }
        }
    }
    zmniejszIloscWMagazynie(id);
    if(!cart_id_array.includes(id)){
        cart_id_array[cart_size] = id_l;
        cart_size++
        if (is_debug) {
            console.log("CART TABLE LEN " + cart_size);
        }
    }
    console.log(cart_id_array);
    var row = cartTable.insertRow();
    row.insertCell(0).innerText = nazwa;
    row.insertCell(1).innerText = ilosc;
    row.insertCell(2).innerText = dawka;
    row.insertCell(3).innerText = 1;
    row.insertCell(4).innerText = waznosc;
    row.insertCell(5).innerText = cena;

    var returnButton = row.insertCell(6);
    returnButton.innerHTML = `<button onclick="zwrocDoMagazynu('${id}')" type="button">Zwróć do magazynu</button>`;
}