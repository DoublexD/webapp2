let is_debug = true;
let cart_size = 0;
let cart_id_array = [];
let cart_boxes_array = [];

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
    let id_l = parseInt(id) - 1;
    let medsTable = document.querySelector('.magazyn table tbody');
    let meds_quantity = parseInt(medsTable.rows[id_l].cells[3].innerText);
    medsTable.rows[id_l].cells[3].innerText = (meds_quantity + 1).toString();

    
    let cartTable = document.getElementById('tabelaKoszyk').getElementsByTagName('tbody')[0];
    for (let i = 0; i < cartTable.rows.length; i++) {
        let rowId = cartTable.rows[i].getAttribute('data-id');
        if (rowId === id) {
            let currentQty = parseInt(cartTable.rows[i].cells[3].innerText);
            if (currentQty > 1) {
                cartTable.rows[i].cells[3].innerText = (currentQty - 1).toString();
            } else {
                cartTable.deleteRow(i);
                cart_id_array = cart_id_array.filter(item => item !== id_l);
                cart_size--;
            }
            break;
        }
    }
}
function sprzedajKoszyk() {
    const tabelaKoszyk = document.getElementById('tabelaKoszyk').getElementsByTagName('tbody')[0];
    const rows = tabelaKoszyk.rows;
    const lekiDoSprzedazy = [];

    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const idLeku = row.getAttribute('data-id');
        const ilosc = parseInt(row.cells[3].innerText); 
        lekiDoSprzedazy.push({ idLeku, ilosc });
    }

    fetch('/sprzedaz_koszyk', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(lekiDoSprzedazy),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Sprzedaż zakończona sukcesem');
       
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Wystąpił błąd podczas sprzedaży');
    });
}

function dodajDoKoszyka(id, nazwa, ilosc, dawka, ilosc_opakowan, waznosc, cena) {
    let id_l = id - 1;
    if (is_debug) {
        console.log(`Dodawanie produktu o ID: ${id_l} do koszyka.`);
    }

    let cartTable = document.getElementById('tabelaKoszyk').getElementsByTagName('tbody')[0];
    let medsTable = document.querySelector('.magazyn table tbody');
    let meds_quantity = parseInt(medsTable.rows[id_l].cells[3].innerText);

    if (meds_quantity <= 0) {
        console.log("Brak dostępnych leków w magazynie.");
        return; 
    }

    
    let isProductInCart = false;
    for (let i = 0; i < cartTable.rows.length; i++) {
        if (cartTable.rows[i].getAttribute('data-id') == id) {
            isProductInCart = true;
            let currentQty = parseInt(cartTable.rows[i].cells[3].innerText);
            cartTable.rows[i].cells[3].innerText = (currentQty + 1).toString();
            zmniejszIloscWMagazynie(id); 
            break;
        }
    }


    if (!isProductInCart) {
        zmniejszIloscWMagazynie(id); 
        let row = cartTable.insertRow();
        row.setAttribute('data-id', id); 
        row.insertCell(0).innerText = nazwa;
        row.insertCell(1).innerText = ilosc;
        row.insertCell(2).innerText = dawka;
        row.insertCell(3).innerText = 1; 
        row.insertCell(4).innerText = waznosc;
        row.insertCell(5).innerText = cena;

        let returnButton = row.insertCell(6);
        returnButton.innerHTML = `<button onclick="zwrocDoMagazynu('${id}')" type="button">Zwróć do magazynu</button>`;

        if (!cart_id_array.includes(id_l)) {
            cart_id_array.push(id_l);
            cart_size++;
        }
    }
}

function sprzedajKoszyk() {
    const tabelaKoszyk = document.getElementById('tabelaKoszyk').getElementsByTagName('tbody')[0];
    const rows = tabelaKoszyk.rows;
    const lekiDoSprzedazy = [];

    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const id_leku = row.getAttribute('data-id');
        const ilosc_opakowan = parseInt(row.cells[3].innerText);
        lekiDoSprzedazy.push({ id_leku, ilosc_opakowan });
    }
    console.log(lekiDoSprzedazy);
    fetch('/sprzedaz_koszyk', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(lekiDoSprzedazy),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Sprzedaż zakończona sukcesem');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Wystąpił błąd podczas sprzedaży');
    } );
}