let medsinCart = 0;


function zmniejszIloscWMagazynie(id) {
    var tabelaMagazynu = document.querySelector('.magazyn table tbody');
    for (var i = 0; i < tabelaMagazynu.rows.length; i++) {
        if (i == parseInt(id)) {
            var aktualnaIlosc = parseInt(tabelaMagazynu.rows[i].cells[3].innerText);
            if (aktualnaIlosc > 0) {
                tabelaMagazynu.rows[i].cells[3].innerText = (aktualnaIlosc - 1).toString();
            }
            break;
        }
    }
}
//function zwrocDoMagazynu(id, medsinCart, ilosc) {
function zwrocDoMagazynu(id, medsinCart, ilosc, rowIndex) {
    //    var tabelaMagazynu = document.querySelector('.magazyn table tbody');
    id = parseInt(id) - 1;
    var tabelaMagazynu = document.querySelector('.magazyn table tbody');
    var tabelaKoszyk = document.getElementById('tabelaKoszyk').getElementsByTagName('tbody')[0];
    var selectedRow = tabelaKoszyk.rows[rowIndex];
    for (var i = 0; i < tabelaMagazynu.rows.length; i++) {
        if (i == parseInt(id)) {
            var aktualnaIlosc = parseInt(tabelaMagazynu.rows[i].cells[3].innerText);
            tabelaMagazynu.rows[i].cells[3].innerText = (aktualnaIlosc + ilosc).toString();
            break;
        }
    }

    //var tabelaKoszyk = document.getElementById('tabelaKoszyk').getElementsByTagName('tbody')[0];
    for (var j = 0; j < tabelaKoszyk.rows.length; j++) {
        if (j == parseInt(medsinCart)) {
            var iloscWKoszyku = parseInt(tabelaKoszyk.rows[j].cells[3].innerText);
            if (iloscWKoszyku > 1) {
                tabelaKoszyk.rows[j].cells[3].innerText = (iloscWKoszyku - ilosc).toString();
            } else {
                tabelaKoszyk.deleteRow(j);
                medsinCart--;
                console.log(medsinCart);
            }
            break;
        }
    }
}

function dodajDoKoszyka(id, nazwa, ilosc, dawka, ilosc_opakowan, waznosc, cena) {
    id = parseInt(id) - 1;
    var tabelaKoszyk = document.getElementById('tabelaKoszyk').getElementsByTagName('tbody')[0];
    var istnieje = false;

    for (var i = 0; i < tabelaKoszyk.rows.length; i++) {
        if (i == id) {
            zmniejszIloscWMagazynie(id, ilosc_opakowan);
            var nowaIlosc = parseInt(tabelaKoszyk.rows[i].cells[3].innerText) + 1;
            tabelaKoszyk.rows[i].cells[3].innerText = nowaIlosc.toString();
            if (parseInt(tabelaKoszyk.rows[i].cells[3].innerText) > 0) {
                istnieje = true;
            }
            return;
        }
    }


    if (!istnieje) {
        zmniejszIloscWMagazynie(parseInt(id), ilosc_opakowan);
        var wiersz = tabelaKoszyk.insertRow();
        wiersz.insertCell(0).innerText = nazwa;
        wiersz.insertCell(1).innerText = ilosc;
        wiersz.insertCell(2).innerText = dawka;
        wiersz.insertCell(3).innerText = 1;
        wiersz.insertCell(4).innerText = waznosc;
        wiersz.insertCell(5).innerText = cena;

        var przyciskZwrotu = wiersz.insertCell(6);
        var medsinCartTemp = medsinCart + 1;
        //przyciskZwrotu.innerHTML = `<button onclick="zwrocDoMagazynu('${id - 1}', ${medsinCart}, 1)" type="button" class="returnMed${medsinCart + 1}">Zwróć do magazynu</button>`;
        przyciskZwrotu.innerHTML = `<button onclick="zwrocDoMagazynu('${id}', ${medsinCart}, 1, ${i})" type="button" class="returnMed${medsinCart + 1}">Zwróć do magazynu</button>`;
        medsinCart++;
        console.log(medsinCart);
        przyciskZwrotu.querySelector(`.returnMed${medsinCartTemp}`).addEventListener('click', function () {
            zwrocDoMagazynu(id, medsinCartTemp, 1);

            // Remove the event listener to ensure it's only executed once
            this.removeEventListener('click', arguments.callee);
        });
    }
}