import flet as ft
import requests
import asyncio
import os

async def fetch_lyrics(artista, titulo):
        """Consulta la letra

        Args:
            artista (string): Nombre del artista
            titulo (string): Canción

        Returns:
            json: Retorna la letra o error resultante.
        """
        try:
            url = f"https://api.lyrics.ovh/v1/{artista}/{titulo}"
            # asyncio.to_thread Ejecuta consultas (no asíncrono) en un hilo separado. Sin bloquear la UI
            # timeout = 10 previene espera eterna si hau problemas de red.
            response = await asyncio.to_thread(requests.get, url, timeout = 10)
            if(response.status_code == 200):
                return response.json()
            return {"error": "Canción no encontrada"}
        except Exception as ex:
            # Error sin crashear de la app. Para controlar
            error = f"Error de conexión. Verifica tu internet.\n Detalle\n{str(ex)}"
            return {"error": error}
    
    
async def main(page: ft.Page):
    # print("✅ App iniciada correctamente")  # 👈 Línea de depuración
    page.title = "Letra de tu música"
    page.theme_mode = ft.ThemeMode.DARK
    # ruta relativa a tu archivo .py
    # page.window.icon = r"E:\Documentos\...\src\assets\icon.ico"
    page.window.icon = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
    
    page.padding = 20
    page.bgcolor = ft.Colors.GREY_900
    # Scroll en la pagina
    # page.scroll = ft.ScrollMode.AUTO
    # page.vertical_alignment = ft.CrossAxisAlignment.START
    # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 830
    page.window.height = 730
    
    artist_field = ft.TextField(
        # Texto flotante que se eleva al enfocar
        label = "Artista",
        # Placeholder, texto de ayuda
        hint_text = "Ej.: Julio Iglesias",
        # Estilos
        border_color = ft.Colors.PURPLE_400,
        focused_border_color = ft.Colors.PURPLE_300,
        cursor_color = ft.Colors.PURPLE_300,
        text_size = 16,
        filled = True,
        bgcolor = ft.Colors.GREY_800,
        border_radius = 12
    )
    
    title_field = ft.TextField(
        # Texto flotante que se eleva al enfocar
        label = "Canción",
        # Placeholder, texto de ayuda
        hint_text = "Ej.: Hola",
        # Estilos
        border_color = ft.Colors.PURPLE_400,
        focused_border_color = ft.Colors.PURPLE_300,
        cursor_color = ft.Colors.PURPLE_300,
        text_size = 16,
        filled = True,
        bgcolor = ft.Colors.GREY_800,
        border_radius = 12
    )
    
    search_btn = ft.Button(
        content = "Buscar letra",
        icon = ft.Icons.SEARCH,
        style = ft.ButtonStyle(
            color = ft.Colors.WHITE,
            bgcolor = ft.Colors.DEEP_PURPLE_600,
            padding = 15,
            shape = ft.RoundedRectangleBorder(radius=10),
        ),
        # on_click=search_click,  # Añadir evento de click
        visible = True  # Cambiado a True para probar
    )
    
    loading = ft.ProgressRing(width=25, height=25, stroke_width=5, color=ft.Colors.PURPLE_400, visible=False)
    result_text = ft.Text(value="", selectable=True, size=15, color=ft.Colors.WHITE)
    
    copy_btn = ft.Button(
        content = "Copiar letra",
        icon = ft.Icons.COPY,
        style = ft.ButtonStyle(
            color = ft.Colors.WHITE,
            bgcolor = ft.Colors.DEEP_PURPLE_600,
            padding = 15,
            shape = ft.RoundedRectangleBorder(radius=10),
        ),
        visible = False
    )
    
    # Ejemplos clickeables
    labelEjemplos = ft.Text(value="Ejemplos populares:", size=15, color=ft.Colors.WHITE)
    ejemploA_btn = ft.Button(
        content = "Enrique Iglesias - Lloro por ti",
        style = ft.ButtonStyle(
            color = ft.Colors.WHITE,
            bgcolor = ft.Colors.DEEP_PURPLE_400,
            padding = 15,
            shape = ft.RoundedRectangleBorder(radius=10),
        ),
        visible = True,
        tooltip = "Da clic"
    )
    
    ejemploB_btn = ft.Button(
        content = "Nanpa Básico  - Aprendí",
        style = ft.ButtonStyle(
            color = ft.Colors.WHITE,
            bgcolor = ft.Colors.DEEP_PURPLE_400,
            padding = 15,
            shape = ft.RoundedRectangleBorder(radius=10),
        ),
        visible = True,
        tooltip = "Da clic"
    )
    
    ejemploC_btn = ft.Button(
        content = "Miguel Bosé - Morena mía",
        style = ft.ButtonStyle(
            color = ft.Colors.WHITE,
            bgcolor = ft.Colors.DEEP_PURPLE_400,
            padding = 15,
            shape = ft.RoundedRectangleBorder(radius=10),
        ),
        visible = True,
        tooltip = "Da clic"
    )
    
    async def search_click(e):
        # 1. Validacion
        if not artist_field.value or not title_field.value.strip():
            result_text.value = "❌ Por favor ingresa artista y canción."
            result_text.color = ft.Colors.RED_300
            copy_btn.visible = False
            page.update()
            return
            
        # 2. Estado de carga
        search_btn.disabled = True
        loading.visible = True
        result_text.value = "Buscando la letra..."
        result_text.color = ft.Colors.PURPLE_300
        copy_btn.visible = False
        page.update()
        
        # 3. Llamada a la API
        data = await fetch_lyrics(artist_field.value.strip(), title_field.value.strip())
        
        # 4. Actualizar UI con resultado
        if "error" in data:
            result_text.value = f"❌ {data['error']}"
            result_text.color = ft.Colors.RED_300
            copy_btn.visible = False
        else:
            # json[lyrics: 'letra']
            result_text.value = data.get("lyrics", "No se encontró la letra")
            result_text.color = ft.Colors.WHITE
            copy_btn.visible = True
        
        search_btn.disabled = False
        loading.visible = False
        page.update()    
    
    async def copy_click(e):
        # set copia texto al portapapeles
        await ft.Clipboard().set(result_text.value)
        # set_clipboard confirma la acción visualmente (elimina la incertidumbre al usuario) sabe que hace
        snack_bar = ft.SnackBar(content=ft.Text("Letra copiada"))
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
    
    # 2. Definir la función que maneja el clic
    async def btnExtraeTexto_click(e):
        # Obtener texto del botón
        texto = e.control.content
        # Separar por el delimitador
        partes = texto.split(" - ")
        # artista = cancion = ""
        # Validar por seguridad
        if len(partes) == 2:
            artista, cancion = partes
        else:
            artista = texto
            cancion = ""
        # Asignar valores .await 
        artist_field.value = artista
        title_field.value = cancion
        page.update()
        await search_click(e)
        
    search_btn.on_click = search_click
    copy_btn.on_click = copy_click
    
    # Ejemplos clickeables
    ejemploA_btn.on_click = btnExtraeTexto_click
    ejemploB_btn.on_click = btnExtraeTexto_click
    ejemploC_btn.on_click = btnExtraeTexto_click
    
    # Apila elementos verticalmente
    # Ideal para formularios, listas
    cabecera = ft.Column([
        ft.Icon(ft.Icons.MUSIC_NOTE, size=45, color=ft.Colors.PURPLE_300),
        ft.Text("Letra encontrada", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        ft.Text("Encuentra las letras de tus canciones favoritas", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)
    
    resultados = ft.Column(
        [result_text],
        scroll=ft.ScrollMode.AUTO,
    )
    
    # UI Principal
    page.add(
        ft.Container(
            content = ft.Column([
                # Cabecera con gradiante
                ft.Container(
                    content = cabecera,
                    padding = 30,
                    # degradado
                    gradient = ft.LinearGradient(
                        begin = ft.Alignment.TOP_LEFT,
                        end = ft.Alignment.BOTTOM_RIGHT,
                        colors = [ft.Colors.PURPLE_900, ft.Colors.DEEP_PURPLE_500, ft.Colors.PURPLE_900]
                    ),
                    shadow = ft.BoxShadow(
                        spread_radius = 1,
                        blur_radius = 15,
                        color = ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                    ),
                    border_radius = 20,
                    width = 750,
                ),
                
                # Campos de entrada
                ft.Container(content=artist_field, width=750),
                ft.Container(content=title_field, width=750),
                
                # Botón de búsqueda
                ft.Row([search_btn, loading], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                
                # Ejemplos para uso
                ft.Row([labelEjemplos], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                ft.Row([ejemploA_btn, ejemploB_btn, ejemploC_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                
                # Resultados
                ft.Container(
                    content = resultados,
                    bgcolor = "#1A1A1A",
                    border = ft.Border.all(width=2, color=ft.Colors.PURPLE_800),
                    border_radius = 15,
                    padding = 20,
                    width = 750,
                    height = 150,
                    # expand = True,
                    # degradado
                    gradient = ft.LinearGradient(
                        begin = ft.Alignment.TOP_LEFT,
                        end = ft.Alignment.BOTTOM_RIGHT,
                        colors = [ft.Colors.PURPLE_900, ft.Colors.DEEP_PURPLE_500, ft.Colors.PURPLE_900]
                    ),
                    shadow = ft.BoxShadow(
                        spread_radius = 1,
                        blur_radius = 15,
                        color = ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                        offset = ft.Offset(0, 4),
                    ),
                ),
                
                # Botón copiar
                ft.Row([copy_btn], alignment=ft.MainAxisAlignment.CENTER),
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
            expand = True
        ),
    )
    # print("🟢 UI cargada")
    await page.window.center()
    page.update()

# Programación asíncrona
# async/await permite que la UI siga respondiendo
# La petición se ejecuta sin bloquear
# Experiencia de usuario profesional
ft.run(main)
