document.addEventListener("DOMContentLoaded", () => {
    const btnAvvia = document.getElementById("startButton");
    const tabellaBody = document.getElementById("resultsTableBody");
    const modal = document.getElementById("scopusModal");
    const modalList = document.getElementById("modalList");
    const confirmBtn = document.getElementById("confirmBtn");
    const MAX_AUTHORS = 5;

    btnAvvia.addEventListener("click", async (e) => {
        e.preventDefault();
        btnAvvia.disabled = true;
        tabellaBody.innerHTML = ""; 
        
        const authorsToProcess = [];
        for (let i = 1; i <= MAX_AUTHORS; i++) {
            const n = document.getElementById(`firstName${i}`).value.trim();
            const c = document.getElementById(`lastName${i}`).value.trim();
            const s = document.getElementById(`scholarId${i}`).value.trim();
            if (n && c && s) authorsToProcess.push({ nome: n, cognome: c, id: s });
        }

        if (authorsToProcess.length === 0) {
            alert("Inserisci dati.");
            btnAvvia.disabled = false;
            return;
        }

        for (const auth of authorsToProcess) {
            await processSingleAuthorFlow(auth);
        }
        btnAvvia.disabled = false;
        btnAvvia.textContent = "Avvia Elaborazione";
    });


    async function processSingleAuthorFlow(authData) {
        // Crea la riga iniziale
        const rowId = addRow(authData.nome + " " + authData.cognome, "Ricerca autore in corso...", "stato-loading");
        
        try {
            // 1. Cerca candidati Scopus
            const searchResp = await fetch('/search_scopus', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(authData)
            });
            const searchResult = await searchResp.json();

            let selectedScopus = null;

            // Gestione risultati Scopus
            if (searchResult.candidates.length === 0) {
                updateRow(rowId, "Nessun autore Scopus trovato", "stato-error", null);
                return;
            } else if (searchResult.candidates.length === 1) {
                selectedScopus = searchResult.candidates[0];
            } else {
                updateRow(rowId, "Attesa scelta utente...", "stato-loading");
                // Apre il popup e aspetta il click
                selectedScopus = await openModalAndWait(searchResult.candidates);
            }

            // 2. Elaborazione (Download & Merge)
            updateRow(rowId, "Download e Analisi in corso...", "stato-loading");
            
            const processResp = await fetch('/process_author', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    scopus_id: selectedScopus.id,
                    scopus_name: selectedScopus.name,
                    scholar_id: authData.id
                })
            });
            const finalResult = await processResp.json();

            console.log(finalResult);

            if (finalResult.status === 'success') {
                // CASO VERDE: Tutto ok
                updateRow(rowId, "Completato", "risultato-successo", finalResult.folder);
            } 
            else if (finalResult.status === 'mismatch') {
                // CASO ROSSO SPECIFICO: Match < 60%
                updateRow(rowId, "Errore: Autori non corrispondenti", "stato-error", null);
            } 
            else {
                // CASO ROSSO GENERICO
                updateRow(rowId, "Errore: " + (finalResult.message || "Server Error"), "stato-error", null);
            }

        } catch (err) {
            console.error(err);
            updateRow(rowId, "Errore di connessione", "stato-error", null);
        }
    }

    function openModalAndWait(candidates) {
        return new Promise((resolve) => {
            modalList.innerHTML = "";
            candidates.forEach((c, idx) => {
                const div = document.createElement("div");
                div.className = "modal-option";
                div.innerHTML = `<input type="radio" name="scopusChoice" value="${idx}" ${idx===0?'checked':''}> <strong>${c.name}</strong> (${c.aff})`;
                modalList.appendChild(div);
            });
            modal.style.display = "flex";
            
          
            const newBtn = confirmBtn.cloneNode(true);
            confirmBtn.parentNode.replaceChild(newBtn, confirmBtn);
            
            newBtn.addEventListener("click", () => {
                const val = document.querySelector('input[name="scopusChoice"]:checked').value;
                modal.style.display = "none";
                resolve(candidates[val]);
            });
        });
    }

    function addRow(name, status, cls) {
        const tr = document.createElement("tr");
        tr.id = "row-" + Date.now();
        tr.innerHTML = `<td>${name}</td><td>...</td><td class="${cls}">${status}</td><td>-</td>`;
        tabellaBody.appendChild(tr);
        return tr.id;
    }

    function updateRow(id, status, cls, folder) {
        const tr = document.getElementById(id);
            if(tr) {
         
            tr.className = cls; 
        
         
            const statusCell = tr.querySelector("td:nth-child(3)");
            statusCell.className = cls; 
            statusCell.textContent = status;
        
            if(folder) tr.querySelector("td:nth-child(4)").innerHTML = `<a href="/download/zip/${folder}" class="btn-download">Scarica</a>`;
    }
}
});