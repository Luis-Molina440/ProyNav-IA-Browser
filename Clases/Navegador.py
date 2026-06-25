import os
import tempfile
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from urllib.parse import urljoin, urlparse, unquote
from Clases.Pestaña import Pestana
from Clases.Historial import Historial
from Clases.Favoritos import Favoritos
from Clases.MotordeBusqueda import MotordeBusqueda

class MiNavegador:
    def __init__(self, root):
        self.root = root
        self.root.title("Navegador")
        self.root.attributes('-alpha', 0.0)
        self.root.geometry("0x0+0+0")
        self.color_bg_actual = "#1e1e1e"
        self.color_fg_actual = "#dcdcdc"
        
        self.app = tk.Toplevel(self.root)
        self.app.geometry("900x650")
        self.app.minsize(450, 350)

        self.modo_offline = tk.BooleanVar(value=False)

        # quita los bordes de cerrar, minimizar y maximizar
        self.app.overrideredirect(True)
        self.offset_x = 0
        self.offset_y = 0
        self.root.bind("<Unmap>", self.al_minimizar_desde_barra)
        self.root.bind("<Map>", self.al_restaurar_desde_barra)
        self.favoritos = Favoritos()
        self.app.bind("<Control-Tab>", self.siguiente_pestana)
        self.app.bind("<Control-Shift-Tab>", self.pestana_anterior)
        self.app.bind("<Control-w>", lambda e: self.cerrar_pestana_actual())
        self.app.bind("<Control-z>", lambda e: self.nueva_pestana())
        for i in range(1, 10):
            self.app.bind(f"<Control-Key-{i}>", lambda e, idx=i-1: self.ir_a_pestana(idx))
            
        self.crear_barra_titulo()
        self.crear_barra_navegacion()
        self.crear_area_contenido()
        self.crear_barra_estado()
        
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.menu_historial = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Historial", menu=self.menu_historial)
        
        self.menu_fav = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Favoritos", menu=self.menu_fav)

        self.actualizar_menu_historial()
        self.actualizar_menu_fav()

        # Inicializar paleta visual moderna
        self.cambiar_color_fondo("#1e1e1e", "#dcdcdc")

    def obtener_paleta(self, bg):
        paletas = {
            "white": {
                "bg_app": "#ffffff", "bg_header": "#f8fafc", "fg_text": "#0f172a",
                "bg_btn": "#e2e8f0", "hover_btn": "#cbd5e1", "fg_btn": "#1e293b",
                "notebook_bg": "#ffffff", "tab_bg": "#f1f5f9", "tab_selected": "#ffffff"
            },
            "#f4ecd8": {
                "bg_app": "#fdf6e3", "bg_header": "#eee8d5", "fg_text": "#5b4636",
                "bg_btn": "#e5ddd0", "hover_btn": "#d8cfc0", "fg_btn": "#5b4636",
                "notebook_bg": "#fdf6e3", "tab_bg": "#eee8d5", "tab_selected": "#fdf6e3"
            },
            "#A9A9A9": {
                "bg_app": "#e2e8f0", "bg_header": "#cbd5e1", "fg_text": "#0f172a",
                "bg_btn": "#94a3b8", "hover_btn": "#64748b", "fg_btn": "#ffffff",
                "notebook_bg": "#e2e8f0", "tab_bg": "#cbd5e1", "tab_selected": "#f1f5f9"
            },
            "#1e1e1e": {
                "bg_app": "#18181b", "bg_header": "#27272a", "fg_text": "#f4f4f5",
                "bg_btn": "#3f3f46", "hover_btn": "#52525b", "fg_btn": "#f4f4f5",
                "notebook_bg": "#18181b", "tab_bg": "#27272a", "tab_selected": "#3f3f46"
            }
        }
        return paletas.get(bg, paletas["#1e1e1e"])

    def crear_barra_titulo(self):
        self.barra_titulo = tk.Frame(self.app, bg="#27272a", height=36)
        self.barra_titulo.pack(fill="x", side="top")
        self.lbl_titulo = tk.Label(self.barra_titulo, text="🌐  ProyNav AI Browser", 
                              bg="#27272a", fg="#f4f4f5", font=("Segoe UI", 10, "bold"))
        self.lbl_titulo.pack(side="left", padx=14)

        # para arrastrar la ventana
        self.barra_titulo.bind("<Button-1>", self.get_pos)
        self.barra_titulo.bind("<B1-Motion>", self.mover_ventana)

        def aplicar_hover(btn, color_normal, color_hover):
            btn.bind("<Enter>", lambda e: btn.config(bg=color_hover))
            btn.bind("<Leave>", lambda e: btn.config(bg=color_normal))

        btn_cerrar = tk.Button(
            self.barra_titulo, text="✕", bg="#27272a", fg="#ef4444",
            command=self.confirmar_cierre, bd=0, relief="flat",
            padx=14, pady=6, font=("Segoe UI", 10), cursor="hand2",
            activebackground="#ef4444", activeforeground="white"
        )
        btn_cerrar.pack(side="right")
        aplicar_hover(btn_cerrar, "#27272a", "#ef4444")

        btn_max = tk.Button(
            self.barra_titulo, text="□", bg="#27272a", fg="#f4f4f5",
            command=self.alternar_maximizacion, bd=0, relief="flat",
            padx=14, pady=6, font=("Segoe UI", 10), cursor="hand2",
            activebackground="#3f3f46", activeforeground="white"
        )
        btn_max.pack(side="right")
        aplicar_hover(btn_max, "#27272a", "#3f3f46")

        btn_min = tk.Button(
            self.barra_titulo, text="—", bg="#27272a", fg="#f4f4f5",
            command=self.minimizar, bd=0, relief="flat",
            padx=14, pady=6, font=("Segoe UI", 10), cursor="hand2",
            activebackground="#3f3f46", activeforeground="white"
        )
        btn_min.pack(side="right")
        aplicar_hover(btn_min, "#27272a", "#3f3f46")

        self.titulo_btns = [btn_cerrar, btn_max, btn_min]

    def crear_barra_navegacion(self):
        self.frame_nav = tk.Frame(self.app, bg="#27272a", pady=8, padx=12)
        self.frame_nav.pack(fill="x")

        frame_left = tk.Frame(self.frame_nav, bg="#27272a")
        frame_left.pack(side="left")

        frame_right = tk.Frame(self.frame_nav, bg="#27272a")
        frame_right.pack(side="right")

        self.btn_atras = tk.Button(frame_left, text="❮", width=3, command=self.retroceder_pag, state="disabled", bd=0, relief="flat", font=("Segoe UI", 11, "bold"), cursor="hand2")
        self.btn_atras.pack(side="left", padx=2)

        self.btn_adelante = tk.Button(frame_left, text="❯", width=3, command=self.avanzar_pag, state="disabled", bd=0, relief="flat", font=("Segoe UI", 11, "bold"), cursor="hand2")
        self.btn_adelante.pack(side="left", padx=2)

        self.btn_refresh = tk.Button(frame_left, text="↻", width=3, command=self.ejecutar_refresh, bd=0, relief="flat", font=("Segoe UI", 11, "bold"), cursor="hand2")
        self.btn_refresh.pack(side="left", padx=2)

        self.btn_estrella_fav = tk.Button(frame_left, text="☆", width=3, command=self.guardar_en_fav, bg="#ffcc00", fg="#000000", bd=0, relief="flat", font=("Segoe UI", 12), cursor="hand2")
        self.btn_estrella_fav.pack(side="left", padx=(8, 2))

        self.btn_memefinder = tk.Button(frame_left, text="🚀 MemeFinder", command=self.abrir_memefinder, bg="#8b5cf6", fg="white", bd=0, relief="flat", font=("Segoe UI", 9, "bold"), padx=10, pady=4, cursor="hand2")
        self.btn_memefinder.pack(side="left", padx=8)

        self.btn_nueva = tk.Button(frame_right, text="＋", width=3, command=self.nueva_pestana, bd=0, relief="flat", font=("Segoe UI", 11, "bold"), cursor="hand2")
        self.btn_nueva.pack(side="right", padx=2)

        btn_cerrar_tab = tk.Button(frame_right, text="✕", width=3, command=self.cerrar_pestana_actual, bd=0, relief="flat", font=("Segoe UI", 10, "bold"), bg="#ef4444", fg="white", cursor="hand2")
        btn_cerrar_tab.pack(side="right", padx=2)
        self.cambio_color(btn_cerrar_tab, "#dc2626", "#ef4444")

        self.btn_menu_color = tk.Menubutton(frame_right, text="🎨 Colores", relief="flat", bd=0, font=("Segoe UI", 9, "bold"), padx=8, pady=4, cursor="hand2")
        self.menu_colores = tk.Menu(self.btn_menu_color, tearoff=0, font=("Segoe UI", 9), bd=1)
        self.menu_colores.add_command(label="⚪ Modo Claro", command=lambda: self.cambiar_color_fondo("white", "black"))
        self.menu_colores.add_command(label="🟤 Modo Sepia", command=lambda: self.cambiar_color_fondo("#f4ecd8", "#5b4636"))
        self.menu_colores.add_command(label="🔘 Modo Slate", command=lambda: self.cambiar_color_fondo("#A9A9A9", "black"))
        self.menu_colores.add_command(label="⚫ Modo Noche", command=lambda: self.cambiar_color_fondo("#1e1e1e", "#dcdcdc"))
        self.btn_menu_color["menu"] = self.menu_colores
        self.btn_menu_color.pack(side="right", padx=6)

        self.btn_menu_principal = tk.Menubutton(frame_right, text="☰ Menú", relief="flat", bd=0, font=("Segoe UI", 9, "bold"), padx=8, pady=4, cursor="hand2")
        self.menu_principal = tk.Menu(self.btn_menu_principal, tearoff=0, font=("Segoe UI", 9), bd=1)
        self.btn_menu_principal["menu"] = self.menu_principal

        self.menu_fav_principal = tk.Menu(self.menu_principal, tearoff=0, font=("Segoe UI", 9))
        self.menu_principal.add_cascade(label="★ Favoritos", menu=self.menu_fav_principal)

        self.menu_hist_principal = tk.Menu(self.menu_principal, tearoff=0, font=("Segoe UI", 9))
        self.menu_principal.add_cascade(label="🕒 Historial", menu=self.menu_hist_principal)
        self.btn_menu_principal.pack(side="right", padx=6)

        self.chk_offline = tk.Checkbutton(frame_right, text="⚡ Offline", variable=self.modo_offline, onvalue=True, offvalue=False, command=self.notificar_cambio_modo, font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2")
        self.chk_offline.pack(side="right", padx=8)

        self.nav_subframes = [frame_left, frame_right]

    def ejecutar_refresh(self):
        self.estado.config(text="↻ Recargando...")
        self.btn_refresh.config(state="disabled")
        self.app.config(cursor="watch")
        self.app.update_idletasks()
        self.root.after(1000, self.finalizar_refresh)

    def finalizar_refresh(self):
        self.recargar_pestana()
        self.estado.config(text="✓ Página actualizada")
        self.btn_refresh.config(state="normal")
        self.app.config(cursor="")
        self.root.after(2000, lambda: self.estado.config(text="Listo"))

    def abrir_memefinder(self):
        """Crea una nueva pestaña interna y carga la página principal del Motor de Búsqueda."""
        try:
            self.nueva_pestana("Super Meme Finder")
            pestana = self.obtener_pestana_actual()
            motor = MotordeBusqueda()
            html = motor.obtener_pagina_principal()
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8')
            tmp.write(html)
            tmp.close()
            path = tmp.name.replace('\\', '/')
            file_url = f'file:///{path}'
            pestana.url_var.set(file_url)
            pestana.cargar()
            self.notebook.tab(pestana.frame, text="Super Meme Finder")
            self.estado.config(text="MemeFinder abierto en nueva pestaña")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir MemeFinder: {e}")
            self.estado.config(text="Error al abrir MemeFinder")

    def cambiar_color_fondo(self, bg, fg):
        self.color_bg_actual = bg
        self.color_fg_actual = fg
        pal = self.obtener_paleta(bg)

        if hasattr(self, "barra_titulo"):
            self.barra_titulo.config(bg=pal["bg_header"])
            self.lbl_titulo.config(bg=pal["bg_header"], fg=pal["fg_text"])
            for btn in getattr(self, "titulo_btns", []):
                if btn.cget("text") != "✕":
                    btn.config(bg=pal["bg_header"], fg=pal["fg_text"])
                else:
                    btn.config(bg=pal["bg_header"])

        if hasattr(self, "frame_nav"):
            self.frame_nav.config(bg=pal["bg_header"])
            for subf in getattr(self, "nav_subframes", []):
                subf.config(bg=pal["bg_header"])

            for btn in [self.btn_atras, self.btn_adelante, self.btn_refresh, self.btn_nueva, self.btn_menu_color, self.btn_menu_principal]:
                btn.config(bg=pal["bg_btn"], fg=pal["fg_btn"], activebackground=pal["hover_btn"], activeforeground=pal["fg_btn"])
            self.chk_offline.config(bg=pal["bg_header"], fg=pal["fg_text"], activebackground=pal["bg_header"], activeforeground=pal["fg_text"], selectcolor=pal["bg_btn"])

        style = ttk.Style()
        style.configure('TNotebook', background=pal["notebook_bg"])
        style.configure('TNotebook.Tab', background=pal["tab_bg"], foreground=pal["fg_text"])
        style.map('TNotebook.Tab', background=[('selected', pal["bg_app"])], foreground=[('selected', pal["fg_text"])])

        for pestana in getattr(self, "pestanas", []):
            pestana.aplicar_color(bg, fg)

        if hasattr(self, "frame_inferior"):
            self.frame_inferior.config(bg=pal["bg_header"])
            self.estado.config(bg=pal["bg_header"], fg=pal["fg_text"])
            self.grip.config(bg=pal["bg_header"], fg=pal["fg_text"])

        if hasattr(self, "estado"):
            self.estado.config(text="Esquema de color actualizado")

    def cambio_color(self, boton, nuevoColor, colorOriginal=None):
        if colorOriginal is None:
            colorOriginal = boton.cget("bg")
        boton.bind("<Enter>", lambda e: boton.config(bg=nuevoColor))
        boton.bind("<Leave>", lambda e: boton.config(bg=colorOriginal))

    def validar_entrada(self, *args):
        pass

    def crear_barra_estado(self):
        self.frame_inferior = tk.Frame(self.app, bg="#27272a", height=28)
        self.frame_inferior.pack(side="bottom", fill="x")
        self.estado = tk.Label(self.frame_inferior, text="Listo", bd=0, relief="flat", anchor="w", bg="#27272a", fg="#a1a1aa", font=("Segoe UI", 9), padx=12, pady=4)
        self.estado.pack(side="left", fill="x", expand=True)
        self.grip = tk.Label(self.app, text="⠿", cursor="size_nw_se", bg="#27272a", fg="#71717a", width=3, font=("Segoe UI", 9))
        self.grip.place(relx=1.0, rely=1.0, anchor="se")
        self.grip.bind("<Button-1>", self.grip_inicio)
        self.grip.bind("<B1-Motion>", self.grip_arrastrar)

    def grip_inicio(self, event):
        self.grip_x = event.x_root
        self.grip_y = event.y_root
        self.ancho_inicial = self.app.winfo_width()
        self.alto_inicial = self.app.winfo_height()

    def grip_arrastrar(self, event):
        ancho = self.ancho_inicial + (event.x_root - self.grip_x)
        alto = self.alto_inicial + (event.y_root - self.grip_y)
        ancho = max(400, ancho)
        alto = max(300, alto)
        self.app.geometry(f"{ancho}x{alto}")
    def get_pos(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def mover_ventana(self, event):
        x = self.app.winfo_x() + event.x - self.offset_x
        y = self.app.winfo_y() + event.y - self.offset_y
        self.app.geometry(f"+{x}+{y}")

    def alternar_maximizacion(self):
        if self.app.state() == 'normal':
            self.app.state('zoomed')
        else:
            self.app.state('normal')

    def minimizar(self):
        self.root.iconify()

    def al_minimizar_desde_barra(self, event):
        if event.widget == self.root:
            self.app.withdraw()

    def al_restaurar_desde_barra(self, event):
        if event.widget == self.root:
            self.app.deiconify()


    def abrir_link(self, url, nueva_pestana=False):
        if nueva_pestana:
            pestana = self.nueva_pestana()
            self.notebook.select(pestana.frame)
            self.app.update_idletasks()
        else:
            pestana = self.obtener_pestana_actual()
        if not pestana:
            return

        parsed = urlparse(url)
        if parsed.scheme == "search":
            termino = unquote(parsed.netloc + parsed.path).lstrip('/')
            self.cargar_busqueda_en_pestana(termino, pestana)
            return

        if not parsed.scheme:
            current_url = pestana.obtener_url()
            if current_url.startswith("http"):
                url = urljoin(current_url, url)
            elif current_url.startswith("file:///"):
                ruta_base = os.path.dirname(current_url.replace("file:///", ""))
                ruta_rel = os.path.normpath(os.path.join(ruta_base, url))
                url = f"file:///{ruta_rel.replace('\\', '/') }"

        pestana.url_var.set(url)
        pestana.frame.update_idletasks()
        pestana.cargar()

    def cargar_busqueda_en_pestana(self, termino, pestana=None):
        motor = MotordeBusqueda()
        html = motor.obtener_resultados_busqueda(termino)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8')
        tmp.write(html)
        tmp.close()
        path = tmp.name.replace('\\', '/')
        file_url = f'file:///{path}'

        if pestana is None:
            pestana = self.obtener_pestana_actual()
        pestana.es_pagina_busqueda = True
        pestana.url_var.set(file_url)
        pestana.cargar()

    def confirmar_cierre(self):
        if messagebox.askokcancel("Confirmar", "¿Seguro que quieres cerrar el navegador?"):
            self.root.destroy()

    def cambio_color(self, boton, nuevoColor, colorOriginal=None):
        if colorOriginal is None:
            colorOriginal = boton.cget("bg")

        boton.bind("<Enter>", lambda e: boton.config(bg=nuevoColor))
        boton.bind("<Leave>", lambda e: boton.config(bg=colorOriginal))

    def crear_area_contenido(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', borderwidth=0)
        style.configure('TNotebook.Tab', font=('Segoe UI', 10), padding=[16, 8], borderwidth=0)
        style.map('TNotebook.Tab', font=[('selected', ('Segoe UI', 10, 'bold'))])

        self.notebook = ttk.Notebook(self.app)
        self.notebook.pack(fill="both", expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: (self.actualizar_menu_historial(), self.actualizar_menu_fav(), self.actualizar_estrella(), self.actualizar_botones_navegacion()))

        self.pestanas = []
        self.nueva_pestana()

    def actualizar_menu_historial(self):
        
        menus = [self.menu_historial]
        if hasattr(self, "menu_hist_principal"):
            menus.append(self.menu_hist_principal)

        for menu in menus:
            menu.delete(0, tk.END)
        
        #obbtener el historial de la pestaña activa
        pestana = self.pestana_actual()
        entradas = pestana.historial.obtener_historial()
        
        if not entradas:
            for menu in menus:
                menu.add_command(label="Historial vacio", state="disabled")
        else:
            for menu in menus:
                for url, titulo in reversed(entradas):
                    display_url = f"{url[:35]}..." if len(url) > 35 else url
                    menu.add_command(
                        label=f"{titulo} - {display_url}", command=lambda u=url: self.cargar_desde_historial(u))

    
    
    def recargar_pestana(self):
        pestana = self.obtener_pestana_actual()
        if pestana:
            pestana.recargar()

    def cargar_desde_historial(self, url):
        pestana = self.obtener_pestana_actual()
        if not pestana:
            return
        pestana.url_var.set(url)
        pestana.cargar()


    def cargar_archivo(self):
        pestana = self.obtener_pestana_actual()
        if pestana:
            pestana.cargar()


    def guardar_en_fav(self):
        pestana = self.obtener_pestana_actual()
        if not pestana:
            return

        url = pestana.obtener_url()
        if not url:
            self.estado.config(text="No hay URL para guardar")
            return

        tab_text = self.notebook.tab(self.notebook.select(), "text")
        titulo = tab_text if tab_text and tab_text != "Nueva pestaña" else pestana.obtener_nombre_archivo(url)

        if self.favoritos.contiene(url):
            self.favoritos.eliminar(url)
            self.btn_estrella_fav.config(text="☆")
            self.estado.config(text="Favorito eliminado")
        else:
            self.favoritos.agregar(url, titulo)
            self.btn_estrella_fav.config(text="★")
            self.estado.config(text="Agregado a favoritos ★")
        self.actualizar_estrella()
        self.actualizar_menu_fav()

    def actualizar_estrella(self):
        pestana = self.obtener_pestana_actual()
        if not pestana:
            return
        url = pestana.obtener_url()
        if self.favoritos.contiene(url):
            self.btn_estrella_fav.config(text="★")
        else:
            self.btn_estrella_fav.config(text="☆")


    def actualizar_menu_fav(self):
        # Limpiar el menú de favoritos
        menus = [self.menu_fav]
        if hasattr(self, "menu_fav_principal"):
            menus.append(self.menu_fav_principal)

        for menu in menus:
            menu.delete(0, tk.END)

        favoritos = self.favoritos.obtener_favoritos()

        if not favoritos:
            for menu in menus:
                menu.add_command(
                    label="No hay favoritos",
                    state="disabled"
                )
            return

        for url, titulo in favoritos:
            for menu in menus:
                menu.add_command(
                    label=url,
                    command=lambda u=url: self.cargar_desde_fav(u)
                )




    def cargar_desde_fav(self, url):
        pestana = self.obtener_pestana_actual()
        if not pestana:
            return
        pestana.url_var.set(url)
        pestana.cargar()
     
    def eliminar_favorito_actual(self):
        pestana = self.obtener_pestana_actual()
        if not pestana:
            return
        url = pestana.obtener_url()
        if not url:
            self.estado.config(text="No hay URL actual para eliminar")
            return
        self.favoritos.eliminar(url)
        self.actualizar_menu_fav()
        self.estado.config(text="Favorito eliminado")

    def nueva_pestana(self, titulo="Nueva pestaña"):
        
        pestana = Pestana(
            self.notebook,
            self.abrir_link,
            titulo=titulo,
            bg=self.color_bg_actual,
            fg=self.color_fg_actual,
            on_historial_update=self.actualizar_menu_historial,
            on_navegacion=self.actualizar_estrella,
            navegador=self
        )

        self.pestanas.append(pestana)
        return pestana

    def siguiente_pestana(self, event=None):
        total = len(self.pestanas)
        if total <=1:
            return
        actual = self.notebook.index(self.notebook.select())
        siguiente = (actual + 1)%total
        self.notebook.select(siguiente)

    def pestana_anterior(self, event=None):
        total = len(self.pestanas)
        if total <=1:
            return
        actual = self.notebook.index(self.notebook.select())
        anterior = (actual - 1)%total
        self.notebook.select(anterior)

    def ir_a_pestana(self, indice, event=None):
        if indice < len(self.pestanas):
            self.notebook.select(indice)   
    
    def obtener_pestana_actual(self):
        index = self.notebook.index(self.notebook.select())
        return self.pestanas[index]

    def pestana_actual(self):
        indice = self.notebook.index(self.notebook.select())
        return self.pestanas[indice]

    def cerrar_pestana_actual(self):
        indice_seleccion = self.notebook.index(self.notebook.select())
        indice_mas_reciente = len(self.pestanas) - 1
        # si hay solo una no se cierra
        if len(self.pestanas) <= 1:
            self.estado.config(text="No se puede cerrar")
            return
        
        if indice_seleccion == indice_mas_reciente:
            self.estado.config(text="No se puede cerrar la mas reciente")
            return
        
        pestana = self.pestanas.pop(indice_seleccion)
        pestana.cerrar()
        self.estado.config(text="Pestaña cerrada")

    def retroceder_pag(self):
        pestana = self.obtener_pestana_actual()
        if pestana:
            pestana.ir_atras()
            self.actualizar_botones_navegacion()

    def avanzar_pag(self):
        pestana = self.obtener_pestana_actual()
        if pestana:
            pestana.ir_adelante()
            self.actualizar_botones_navegacion()

    def actualizar_botones_navegacion(self):
        pestana = self.obtener_pestana_actual()
        if not pestana:
            self.btn_atras.config(state="disabled")
            self.btn_adelante.config(state="disabled")
            return
        if pestana.historial_atras:
            self.btn_atras.config(state="normal")
        else:
            self.btn_atras.config(state="disabled")
        if pestana.historial_adelante:
            self.btn_adelante.config(state="normal")
        else:
            self.btn_adelante.config(state="disabled")

    def notificar_cambio_modo(self):
        if self.modo_offline.get():
            self.estado.config(text="⚡ Navegador en MODO OFFLINE", fg="#ef4444")
        else:
            self.estado.config(text="🌐 Navegador en MODO ONLINE", fg="#10b981")
        for pestana in self.pestanas:
            pestana.actualizar_estado_ia_por_offline()
        self.actualizar_botones_navegacion()