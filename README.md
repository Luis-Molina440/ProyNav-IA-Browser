# 🌐 ProyNav — Navegador Web Nativo (Online y Escritorio)

Un navegador web gráfico, rápido y versátil desarrollado 100% en Python nativo. Diseñado para navegar páginas en internet e inspeccionar archivos HTML locales del escritorio, con motor de red propio, renderizado dinámico de etiquetas e Inteligencia Artificial integrada.

<!-- 📸 FOTO 1: VISTA PRINCIPAL DEL NAVEGADOR -->
<img width="1363" height="767" alt="image" src="https://github.com/user-attachments/assets/c0b22cf4-d78b-49e1-bf9e-54dd7824bf5e" />


## 📌 Contexto Académico

Este software fue construido como proyecto semestral para la asignatura de segundo año **Proyecto de Programación** en la Universidad por un equipo académico de 4 estudiantes. El objetivo principal fue crear un navegador web funcional sin utilizar frameworks web ni librerías externas (como Selenium, PyQt o motores embebidos), programando la lógica de red e interfaz gráfica exclusivamente mediante la biblioteca estándar de Python.

## ✨ Características Principales

* **🌐 Navegación Dual:** Explora sitios web online mediante protocolos HTTP/HTTPS e inspecciona archivos `.html` guardados directamente en el disco duro de tu escritorio.
* **⭐ Gestión de Favoritos:** Guarda tus sitios web preferidos para un acceso instantáneo desde el menú superior.
* **🕒 Historial de Navegación:** Registro temporal de sitios visitados con botones de navegación Atrás/Adelante.
* **🚀 Motor HTTP Propio:** Gestión completa de peticiones TCP, redirecciones en cadena y negociación de certificados SSL nativos.
* **🎨 Motor de Renderizado Estructurado:** Transforma etiquetas HTML crudas (`<h1>`, `<p>`, `<table>`, `<a>`) en componentes gráficos nativos de escritorio en tiempo real.
* **📑 Interfaz Multi-Pestaña:** Sistema multi-pestaña con pantalla de bienvenida central estructurada, barra de direcciones omnibox e indicadores de estado.
* **🤖 Asistente IA Integrado:** Panel flotante lateral inteligente para consultar dudas o resumir el contenido de la página actual.
* **🌓 Temas Visuales:** Paletas adaptativas con modos Noche, Claro, Sepia y Slate.

## 💻 Mi Contribución Técnica

Dentro del equipo de trabajo de 4 integrantes, estuve a cargo de diseñar y programar **toda la lógica central de extracción, red y visualización del contenido HTML**:

1. **Clase `ClienteHTTP` (Capa de Red):**
   * Programación del cliente de conexión HTTP/HTTPS nativo con `http.client` y `urllib.parse`.
   * Algoritmo de control y seguimiento automático de redirecciones web.
   * Soporte multi-puerto (`80`, `443`, `8080`, `3000`, `5173`) y envoltorio de seguridad `ssl`.

2. **Clase `RenderAvanzado` (Capa de Transformación Visual):**
   * Lógica de extracción de código HTML crudo proveniente de servidores web online o documentos locales del computador.
   * Análisis sintáctico con `HTMLParser` para descomponer jerarquías de etiquetas, textos y atributos sintácticos.
   * Creación y posicionamiento dinámico de widgets de escritorio (`tk.Label`, `tk.Text`, botones y tablas) aplicando adaptaciones proporcionales y paletas de color en pantalla.

<!-- 📸 FOTO 2: DEMOSTRACIÓN DE RENDERING DE TABLAS Y HTML -->
<img width="1363" height="767" alt="image" src="https://github.com/user-attachments/assets/44744b6f-b47f-4bce-9f2e-3d4f6472a0be" />

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.13
* **Interfaz Gráfica:** `tkinter` / `tkinter.ttk`
* **Redes y Protocolos:** `http.client`, `urllib.parse`, `ssl`, `socket`
* **Parser HTML:** `html.parser.HTMLParser`

## 🚀 Cómo Ejecutar el Proyecto

Al estar construido con módulos de la biblioteca estándar de Python, no requiere instalaciones con `pip`.

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/proynav.git
   ```
2. Accede a la carpeta:
   ```bash
   cd proynav
   ```
3. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```
