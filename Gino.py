# Gino – Catalogo Biblioteca
# Realizzato da Antonio Vigilante
# Licenza: GNU General Public License v3 (https://www.gnu.org/licenses/gpl-3.0.html)
#
# Questo programma è software libero: puoi ridistribuirlo e/o modificarlo
# secondo i termini della GNU GPL versione 3.
#


import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

catalogo = []
indice_modifica = None

def mostra_guida():
    guida = (
        "📘 Guida all'uso di Gino – Catalogo Biblioteca\n\n"
        "➕ Aggiungere un libro:\n"
        "- Compila i campi a sinistra.\n"
        "- Autori separati da virgola.\n"
        "- Seleziona il formato dal menu.\n"
        "- Premi 'Aggiungi Libro'.\n\n"
        "💾 Salvare il catalogo:\n"
        "- Clicca su 'Salva Catalogo' per salvare in un file .json.\n\n"
        "📂 Caricare un catalogo esistente:\n"
        "- Clicca su 'Carica Catalogo' e seleziona un file .json valido.\n\n"
        "🔍 Cercare un libro:\n"
        "- Inserisci una parola chiave e clicca su 'Cerca'.\n\n"
        "🌐 Esportare in HTML:\n"
        "- Clicca su 'Esporta in HTML', inserisci un titolo e salva.\n\n"
        "✏️ Modificare un record:\n"
        "- Seleziona una riga e clicca su 'Modifica'.\n"
        "- I dati appariranno nei campi. Modifica e premi 'Aggiungi Libro / Salva Modifica'."
    )
    messagebox.showinfo("Guida", guida)

def salva_json():
    if not catalogo:
        messagebox.showwarning("Attenzione", "Il catalogo è vuoto.")
        return
    file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("File JSON", "*.json")])
    if file:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(catalogo, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Salvato", "Catalogo salvato con successo.")

def carica_json():
    global catalogo
    file = filedialog.askopenfilename(filetypes=[("File JSON", "*.json")])
    if file:
        with open(file, "r", encoding="utf-8") as f:
            catalogo = json.load(f)
        aggiorna_lista()

def aggiorna_lista():
    elenco.delete(*elenco.get_children())
    for libro in catalogo:
        elenco.insert("", "end", values=("; ".join(libro["autore"]), libro["titolo"], libro["editore"], libro["data"]))

def aggiungi_libro():
    global indice_modifica
    libro = raccogli_dati()
    if indice_modifica is not None:
        catalogo[indice_modifica] = libro
        indice_modifica = None
    else:
        catalogo.append(libro)
    aggiorna_lista()
    pulisci_campi()

def raccogli_dati():
    return {
        "titolo": titolo_var.get(),
        "sottotitolo": sottotitolo_var.get(),
        "autore": [a.strip() for a in autore_var.get().split(",")],
        "traduttore": traduttore_var.get(),
        "cura": cura_var.get(),
        "editore": editore_var.get(),
        "luogo": luogo_var.get(),
        "data": data_var.get(),
        "edizione": edizione_var.get(),
        "argomento": argomento_var.get(),
        "tag": tag_var.get(),
        "formato": formato_var.get(),
        "note": note_var.get(),
        "collocazione": collocazione_var.get()
    }

def pulisci_campi():
    for var in [titolo_var, sottotitolo_var, autore_var, traduttore_var, cura_var,
                editore_var, luogo_var, data_var, edizione_var, argomento_var, tag_var,
                note_var, collocazione_var]:
        var.set("")
    formato_var.set("cartaceo")

def cerca_libro():
    chiave = ricerca_var.get().lower()
    elenco.delete(*elenco.get_children())
    for libro in catalogo:
        testo_completo = " ".join([str(v) if not isinstance(v, list) else " ".join(v) for v in libro.values()]).lower()
        if chiave in testo_completo:
            elenco.insert("", "end", values=("; ".join(libro["autore"]), libro["titolo"], libro["editore"], libro["data"]))

def esporta_html():
    if not catalogo:
        messagebox.showwarning("Attenzione", "Il catalogo è vuoto.")
        return
    titolo_html = simpledialog.askstring("Titolo HTML", "Inserisci il titolo della pagina (es. Biblioteca di Gino):")
    if not titolo_html:
        return
    file = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("File HTML", "*.html")])
    if file:
        with open(file, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html><html><head><meta charset='UTF-8'><title>%s</title>" % titolo_html)
            f.write("<style>table{width:100%%;border-collapse:collapse}th,td{border:1px solid #ccc;padding:8px;text-align:left;}th{background:#eee}</style>")
            f.write("</head><body><h1>%s</h1>" % titolo_html)
            f.write("<input type='text' id='filtro' onkeyup='filtra()' placeholder='Cerca...'><table id='tabella'><thead><tr>")
            for campo in ["Autori", "Titolo", "Sottotitolo", "Traduttore", "A cura di", "Editore", "Luogo", "Data", "Edizione", "Argomento", "Tag", "Formato", "Collocazione", "Note"]:
                f.write("<th>%s</th>" % campo)
            f.write("</tr></thead><tbody>")
            for libro in catalogo:
                f.write("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                    "; ".join(libro["autore"]), libro["titolo"], libro["sottotitolo"], libro["traduttore"], libro["cura"],
                    libro["editore"], libro["luogo"], libro["data"], libro["edizione"], libro["argomento"],
                    libro["tag"], libro["formato"], libro["collocazione"], libro["note"]
                ))
            f.write("</tbody></table><script>function filtra(){let i=document.getElementById('filtro').value.toLowerCase();document.querySelectorAll('#tabella tbody tr').forEach(r=>{r.style.display=r.innerText.toLowerCase().includes(i)?'':'none';});}</script></body></html>")
        messagebox.showinfo("Esportazione completata", "File HTML generato con successo.")

def modifica_libro():
    global indice_modifica
    selezione = elenco.selection()
    if not selezione:
        messagebox.showwarning("Attenzione", "Seleziona un record da modificare.")
        return
    indice_modifica = elenco.index(selezione[0])
    libro = catalogo[indice_modifica]
    titolo_var.set(libro["titolo"])
    sottotitolo_var.set(libro["sottotitolo"])
    autore_var.set(", ".join(libro["autore"]))
    traduttore_var.set(libro["traduttore"])
    cura_var.set(libro["cura"])
    editore_var.set(libro["editore"])
    luogo_var.set(libro["luogo"])
    data_var.set(libro["data"])
    edizione_var.set(libro["edizione"])
    argomento_var.set(libro["argomento"])
    tag_var.set(libro["tag"])
    formato_var.set(libro["formato"])
    note_var.set(libro["note"])
    collocazione_var.set(libro["collocazione"])

# Interfaccia grafica
root = tk.Tk()
root.title("Gino")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0)

ttk.Button(frame, text="Guida", command=mostra_guida).grid(row=0, column=2, padx=10)

# Variabili
titolo_var = tk.StringVar()
sottotitolo_var = tk.StringVar()
autore_var = tk.StringVar()
traduttore_var = tk.StringVar()
cura_var = tk.StringVar()
editore_var = tk.StringVar()
luogo_var = tk.StringVar()
data_var = tk.StringVar()
edizione_var = tk.StringVar()
argomento_var = tk.StringVar()
tag_var = tk.StringVar()
formato_var = tk.StringVar(value="cartaceo")
note_var = tk.StringVar()
collocazione_var = tk.StringVar()
ricerca_var = tk.StringVar()

campi = [
    ("Titolo", titolo_var),
    ("Sottotitolo", sottotitolo_var),
    ("Autori (separati da virgola)", autore_var),
    ("Traduttore", traduttore_var),
    ("A cura di", cura_var),
    ("Editore", editore_var),
    ("Luogo", luogo_var),
    ("Data", data_var),
    ("Edizione", edizione_var),
    ("Argomento", argomento_var),
    ("Tag", tag_var),
    ("Collocazione", collocazione_var),
    ("Note", note_var)
]

for i, (label, var) in enumerate(campi):
    ttk.Label(frame, text=label + ":").grid(row=i, column=0)
    ttk.Entry(frame, textvariable=var, width=40).grid(row=i, column=1)

ttk.Label(frame, text="Formato:").grid(row=len(campi), column=0)
ttk.OptionMenu(frame, formato_var, "cartaceo", "cartaceo", "ePub", "PDF").grid(row=len(campi), column=1)

ttk.Button(frame, text="Aggiungi Libro / Salva Modifica", command=aggiungi_libro).grid(row=len(campi)+1, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Modifica", command=modifica_libro).grid(row=len(campi)+2, column=0, columnspan=2, pady=5)

ttk.Label(frame, text="Cerca:").grid(row=len(campi)+3, column=0)
ttk.Entry(frame, textvariable=ricerca_var, width=40).grid(row=len(campi)+3, column=1)
ttk.Button(frame, text="Cerca", command=cerca_libro).grid(row=len(campi)+4, column=0, columnspan=2, pady=5)

elenco = ttk.Treeview(frame, columns=("Autore", "Titolo", "Editore", "Data"), show="headings")
for col in ("Autore", "Titolo", "Editore", "Data"):
    elenco.heading(col, text=col)
elenco.grid(row=len(campi)+5, column=0, columnspan=2, pady=10)

ttk.Button(frame, text="Salva Catalogo", command=salva_json).grid(row=len(campi)+6, column=0)
ttk.Button(frame, text="Carica Catalogo", command=carica_json).grid(row=len(campi)+6, column=1)
ttk.Button(frame, text="Esporta in HTML", command=esporta_html).grid(row=len(campi)+7, column=0, columnspan=2, pady=5)

root.mainloop()
