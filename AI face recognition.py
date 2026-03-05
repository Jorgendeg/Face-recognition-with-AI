import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import requests
import cv2
import numpy as np
import os
import pickle
import shutil
from pathlib import Path
from picamera2 import Picamera2
BACKGROUND_IMAGE_PATH = "/home/raspberry/Pictures/achtergrond.jpg"
MODEL = "llama-3.1-8b-instant"
GROQ_API_KEY ="API KEY HERE"
DATA_DIR = Path.home() / "gezichten"
DATASET_DIR = DATA_DIR / "dataset"
MODELS_DIR = DATA_DIR / "models"
DATASET_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
RECOGNIZER_FILE = MODELS_DIR / "trainer.yml"
LABELS_FILE = MODELS_DIR / "labels.pkl"
gebruikers_naam = ""
current_mode = None
recognizer = None
label_to_name = {}
name_to_label = {}
try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if RECOGNIZER_FILE.exists() and LABELS_FILE.exists():
        recognizer.read(str(RECOGNIZER_FILE))
        with open(LABELS_FILE, "rb") as f:
            label_to_name = pickle.load(f)
        name_to_label = {v: k for k, v in label_to_name.items()}
        print(f"Geladen: {len(label_to_name)} bekende personen")
    else:
        print("Geen getraind model gevonden → eerste gebruiker aanmaken")
except AttributeError:
    messagebox.showerror("OpenCV fout", "cv2.face module ontbreekt!\nInstalleer met:\npython3 -m pip install opencv-contrib-python")
    recognizer = None
except Exception as e:
    print(f"Fout bij laden model: {e}")
def open_camera():
    try:
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(main={"size": (640, 480)})
        picam2.configure(config)
        picam2.start()
        print("Picamera2 gestart")
        return picam2
    except Exception as e:
        messagebox.showerror("Camera Fout", f"Kan Picamera2 niet starten:\n{e}")
        return None
def live_preview_and_capture(mode, verwachte_naam=""):
    picam2 = open_camera()
    if picam2 is None:
        return None
    cv2.namedWindow("Camera - SPATIE = foto  /  ESC = annuleren", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera - SPATIE = foto  /  ESC = annuleren", 800, 600)
    cascade_path = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
    if not os.path.exists(cascade_path):
        messagebox.showerror("Haar-cascade ontbreekt", "Installeer met:\nsudo apt install opencv-data")
        if picam2:
            picam2.stop()
            picam2.close()
        cv2.destroyAllWindows()
        return None
    face_cascade = cv2.CascadeClassifier(cascade_path)
    foto = None
    while True:
        frame = picam2.capture_array("main")
        if frame is None or frame.size == 0:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(frame, "Gezicht gevonden", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.imshow("Camera - SPATIE = foto  /  ESC = annuleren", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            if len(faces) == 0:
                messagebox.showwarning("Geen gezicht", "Geen gezicht gedetecteerd!")
            else:
                x, y, w, h = faces[0]
                face_roi = gray[y:y + h, x:x + w]
                foto = cv2.resize(face_roi, (200, 200))
            break
        if key == 27:
            break
    if picam2:
        picam2.stop()
        picam2.close()
    cv2.destroyAllWindows()
    return foto
def train_model():
    if recognizer is None:
        return
    faces = []
    labels = []
    face_cascade = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
    for naam_map in DATASET_DIR.iterdir():
        if not naam_map.is_dir():
            continue
        naam = naam_map.name
        if naam in name_to_label:
            label = name_to_label[naam]
        else:
            label = len(label_to_name)
            label_to_name[label] = naam
            name_to_label[naam] = label

        for img_path in naam_map.glob("*.jpg"):
            img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            faces.append(img)
            labels.append(label)
    if len(faces) == 0:
        print("Geen foto's om te trainen")
        return
    recognizer.train(faces, np.array(labels))
    recognizer.save(str(RECOGNIZER_FILE))
    with open(LABELS_FILE, "wb") as f:
        pickle.dump(label_to_name, f)
    print(f"Model getraind met {len(faces)} foto's")
def registreer():
    global current_mode
    current_mode = "register"
    clear_screen()
    tk.Label(root, text="Nieuwe account aanmaken", font=("Arial", 36, "bold"),
             fg="white", bg="black").place(relx=0.5, rely=0.25, anchor="center")
    tk.Label(root, text="Je naam:", font=("Arial", 28), fg="white", bg="black")\
        .place(relx=0.5, rely=0.40, anchor="center")
    entry = tk.Entry(root, font=("Arial", 24), width=25, justify="center")
    entry.place(relx=0.5, rely=0.52, anchor="center")
    entry.focus()
    def start_reg():
        naam = entry.get().strip()
        if not naam:
            messagebox.showwarning("Fout", "Vul een naam in")
            return
        if naam in name_to_label:
            messagebox.showwarning("Fout", "Deze naam bestaat al")
            return
        persoon_dir = DATASET_DIR / naam
        persoon_dir.mkdir(exist_ok=True)
        tk.Label(root, text="Kijk in de camera\nDruk SPATIE om foto te maken\n(ESC om annuleren)",
                 font=("Arial", 24), fg="#FF9800", bg="black")\
            .place(relx=0.5, rely=0.70, anchor="center")
        face_img = live_preview_and_capture("register", naam)
        if face_img is not None:
            cv2.imwrite(str(persoon_dir / "face.jpg"), face_img)
            train_model()
            messagebox.showinfo("Gelukt", f"Account '{naam}' aangemaakt!")
            toon_start_scherm()
        else:
            messagebox.showinfo("Geannuleerd", "Geen foto gemaakt")
    tk.Button(root, text="Start camera (of Enter)", font=("Arial", 20, "bold"),
              bg="#FF9800", fg="white", command=start_reg)\
        .place(relx=0.5, rely=0.82, anchor="center")

    entry.bind("<Return>", lambda e: start_reg())
def login():
    global current_mode, gebruikers_naam, GROQ_API_KEY
    current_mode = "login"
    clear_screen()
    tk.Label(root, text="Inloggen", font=("Arial", 36, "bold"),
             fg="white", bg="black").place(relx=0.5, rely=0.25, anchor="center")
    tk.Label(root, text="Je naam:", font=("Arial", 28), fg="white", bg="black")\
        .place(relx=0.5, rely=0.40, anchor="center")
    entry = tk.Entry(root, font=("Arial", 24), width=25, justify="center")
    entry.place(relx=0.5, rely=0.52, anchor="center")
    entry.focus()
    def start_login():
        naam = entry.get().strip()
        if not naam:
            messagebox.showwarning("Fout", "Vul een naam in")
            return
        if naam not in name_to_label:
            messagebox.showerror("Onbekend", "Deze naam kennen we niet")
            return
        tk.Label(root, text="Kijk in de camera\nDruk SPATIE om te scannen\n(ESC om annuleren)",
                 font=("Arial", 24), fg="#2196F3", bg="black")\
            .place(relx=0.5, rely=0.70, anchor="center")
        face_img = live_preview_and_capture("login", naam)
        if face_img is None:
            return
        if recognizer is None:
            messagebox.showerror("Fout", "Gezichtsherkenning niet beschikbaar")
            return
        label, confidence = recognizer.predict(face_img)
        herkende_naam = label_to_name.get(label, "Onbekend")
        print(f"Voorspeld: {herkende_naam} (confidence: {confidence:.1f})")
        if herkende_naam == naam and confidence < 85:
            gebruikers_naam = naam
            GROQ_API_KEY = "API KEY HERE"
            def ga_naar_chat(event=None):
                root.unbind("<Return>")
                root.unbind("<space>")
                start_chat()
            messagebox.showinfo(
                "Ingelogd",
                f"Welkom terug, {naam}!\nJe bent succesvol ingelogd.\n\n"
                "Druk op ENTER of SPATIE om naar de chat te gaan"
            )

            root.bind("<Return>", ga_naar_chat)
            root.bind("<space>", ga_naar_chat)

        else:
            messagebox.showerror("Toegang geweigerd",
                                 f"Geen match\n(herkend als {herkende_naam}, confidence={confidence:.1f})")
    tk.Button(root, text="Start scan (of Enter)", font=("Arial", 20, "bold"),
              bg="#2196F3", fg="white", command=start_login)\
        .place(relx=0.5, rely=0.82, anchor="center")
    entry.bind("<Return>", lambda e: start_login())
def verwijder_account():
    global current_mode
    current_mode = "delete"
    clear_screen()
    tk.Label(root, text="Account verwijderen", font=("Arial", 36, "bold"),
             fg="white", bg="black").place(relx=0.5, rely=0.25, anchor="center")
    tk.Label(root, text="Naam van het account:", font=("Arial", 28), fg="white", bg="black")\
        .place(relx=0.5, rely=0.40, anchor="center")
    entry = tk.Entry(root, font=("Arial", 24), width=25, justify="center")
    entry.place(relx=0.5, rely=0.52, anchor="center")
    entry.focus()
    def start_verwijder():
        naam = entry.get().strip()
        if not naam:
            messagebox.showwarning("Fout", "Vul een naam in")
            return
        if naam not in name_to_label:
            messagebox.showerror("Onbekend", "Dit account bestaat niet")
            return
        persoon_dir = DATASET_DIR / naam
        if persoon_dir.exists():
            shutil.rmtree(persoon_dir)
        if naam in name_to_label:
            del label_to_name[name_to_label[naam]]
            del name_to_label[naam]
        train_model()
        messagebox.showinfo("Gelukt", f"Account '{naam}' verwijderd!")
        toon_start_scherm()
    tk.Button(root, text="Verwijder (of Enter)", font=("Arial", 20, "bold"),
              bg="#FF5252", fg="white", command=start_verwijder)\
        .place(relx=0.5, rely=0.68, anchor="center")
    entry.bind("<Return>", lambda e: start_verwijder())
    tk.Button(root, text="Terug", font=("Arial", 18), command=toon_start_scherm)\
        .place(relx=0.5, rely=0.85, anchor="center")
def clear_screen():
    for widget in root.winfo_children():
        if widget != canvas:
            widget.destroy()
def toon_start_scherm():
    clear_screen()
    tk.Label(root, text="Welkom bij Gezichtsherkenning", font=("Arial", 40, "bold"),
             fg="white", bg="black").place(relx=0.5, rely=0.25, anchor="center")
    tk.Label(root, text="Druk op:", font=("Arial", 32), fg="white", bg="black")\
        .place(relx=0.5, rely=0.40, anchor="center")
    tk.Label(root, text="ENTER → Account aanmaken", font=("Arial", 36, "bold"),
             fg="#4CAF50", bg="black").place(relx=0.5, rely=0.55, anchor="center")
    tk.Label(root, text="SHIFT  → Inloggen", font=("Arial", 36, "bold"),
             fg="#2196F3", bg="black").place(relx=0.5, rely=0.67, anchor="center")
    tk.Label(root, text="- (min) → Account verwijderen", font=("Arial", 36, "bold"),
             fg="#FF5252", bg="black").place(relx=0.5, rely=0.79, anchor="center")
    root.focus_set()
    root.focus_force()
def start_chat():
    root.unbind("<Return>")
    root.unbind("<space>")
    root.unbind("<Shift_L>")
    root.unbind("<Shift_R>")
    root.unbind("-")
    clear_screen()
    tk.Label(root, text=f"Hoi {gebruikers_naam}!", font=("Arial", 36, "bold"),
             fg="white", bg="black").place(relx=0.5, rely=0.08, anchor="center")
    global chat_log
    chat_log = scrolledtext.ScrolledText(
        root, font=("Arial", 15), wrap=tk.WORD,
        bg="#181818", fg="#e0e0e0", insertbackground="white",
        spacing1=6, spacing3=6
    )
    chat_log.place(relx=0.5, rely=0.52, relwidth=0.92, relheight=0.68, anchor="center")
    chat_log.insert(tk.END, f"Welkom terug, {gebruikers_naam}!\nJe kunt nu chatten met de AI.\n\n")
    chat_log.configure(state='disabled')
    invoer_frame = tk.Frame(root, bg="black")
    invoer_frame.place(relx=0.5, rely=0.94, relwidth=0.92, anchor="center")
    global chat_entry
    chat_entry = tk.Entry(
        invoer_frame, font=("Arial", 18),
        bg="#333333", fg="white", insertbackground="white",
        relief="flat"
    )
    chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,8), pady=10)
    chat_entry.focus()
    verstuur_btn = tk.Button(
        invoer_frame, text="Verstuur", font=("Arial", 16, "bold"),
        bg="#2196F3", fg="white", padx=24, pady=10,
        relief="flat", command=verstuur_chat
    )
    verstuur_btn.pack(side=tk.RIGHT, padx=0, pady=10)

    chat_entry.bind("<Return>", lambda e: verstuur_chat())
    def focus_chat(event):
        chat_entry.focus_set()
        return "break"
    root.bind("<space>", focus_chat)
    tk.Button(root, text="← Terug", font=("Arial",14), bg="#444", fg="white",
              command=back_to_start).place(relx=0.04, rely=0.04, anchor="nw")
def verstuur_chat():
    if GROQ_API_KEY is None or not GROQ_API_KEY.strip():
        chat_log.configure(state='normal')
        chat_log.insert(tk.END, "\nFout: Geen geldige Groq API key!\n\n")
        chat_log.configure(state='disabled')
        chat_log.see(tk.END)
        return
    tekst = chat_entry.get().strip()
    if not tekst:
        return
    chat_log.configure(state='normal')
    chat_log.insert(tk.END, f"{gebruikers_naam}: {tekst}\n")
    chat_log.see(tk.END)
    chat_log.configure(state='disabled')
    chat_entry.delete(0, tk.END)
    chat_log.configure(state='normal')
    chat_log.insert(tk.END, "AI denkt...\n")
    chat_log.see(tk.END)
    chat_log.configure(state='disabled')
    root.update()
    try:
        berichten = [
            {"role": "system", "content": "Je bent een vriendelijke, behulpzame assistent. Antwoord altijd in het Nederlands."},
            {"role": "user", "content": tekst}
        ]
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "messages": berichten,
            "model": MODEL,
            "temperature": 0.7,
            "max_tokens": 750
        }
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers, json=data, timeout=30
        )
        r.raise_for_status()
        antwoord = r.json()["choices"][0]["message"]["content"].strip()
        chat_log.configure(state='normal')
        chat_log.delete("end-2l", tk.END)
        chat_log.insert(tk.END, f"AI: {antwoord}\n\n")
        chat_log.configure(state='disabled')
        chat_log.see(tk.END)
    except Exception as e:
        chat_log.configure(state='normal')
        chat_log.delete("end-2l", tk.END)
        chat_log.insert(tk.END, f"\nFout: {str(e)}\n(Controleer internet / API-key)\n\n")
        chat_log.configure(state='disabled')
        chat_log.see(tk.END)
def back_to_start(event=None):
    global gebruikers_naam, GROQ_API_KEY
    gebruikers_naam = ""
    GROQ_API_KEY = None
    root.bind("<Return>", lambda e: registreer())
    root.bind("<Shift_L>", lambda e: login())
    root.bind("<Shift_R>", lambda e: login())
    root.bind("-", lambda e: verwijder_account())
    root.unbind("<space>")
    toon_start_scherm()
root = tk.Tk()
root.title("Gezichtsherkenning & AI Chat")
root.attributes('-fullscreen', True)
root.configure(bg="black")
root.bind("<Escape>", lambda e: root.destroy())
root.bind("<Delete>", back_to_start)
root.bind("<Return>", lambda e: registreer())
root.bind("<Shift_L>", lambda e: login())
root.bind("<Shift_R>", lambda e: login())
root.bind("-", lambda e: verwijder_account())
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
bg_photo = None
try:
    img = Image.open(BACKGROUND_IMAGE_PATH).resize((screen_w, screen_h), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(img)
except Exception as e:
    print("Achtergrond laden mislukt:", e)
canvas = tk.Canvas(root, width=screen_w, height=screen_h, highlightthickness=0)
canvas.pack(fill="both", expand=True)
if bg_photo:
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
toon_start_scherm()
root.focus_set()
root.focus_force()
root.bg_photo = bg_photo
root.mainloop()
