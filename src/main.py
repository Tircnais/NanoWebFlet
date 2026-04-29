import flet as ft
import httpx
import os
import platform

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
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10)
            if(response.status_code == 200):
                return response.json()
            return {"error": "Canción no encontrada"}
        except Exception as ex:
            # Error sin crashear de la app. Para controlar
            error = f"Error de conexión. Verifica tu internet.\n Detalle\n{str(ex)}"
            return {"error": error}
    
    
async def main(page: ft.Page):
    dialog_open = {"value": False}

    # 🔑 función única para mostrar diálogo
    def show_exit_dialog():
        if not dialog_open["value"]:
            dialog_open["value"] = True
            page.show_dialog(confirm_dialog)

    # 🔑 confirmar salida
    def handle_yes_click(e):
        dialog_open["value"] = False

        # Desktop
        if page.platform in [
            ft.PagePlatform.WINDOWS,
            ft.PagePlatform.LINUX,
            ft.PagePlatform.MACOS,
        ]:
            page.window.prevent_close = False
            page.run_task(close_app)
        else:
            # Móvil / Web
            page.window.destroy()  # fallback seguro

    # 🔑 cancelar
    def handle_no_click(e):
        dialog_open["value"] = False
        page.pop_dialog()

    # 🔑 cierre async (desktop moderno)
    async def close_app():
        await page.window.close()

    # 🔑 evento ventana (desktop)
    def window_event(e: ft.WindowEvent):
        if e.type == ft.WindowEventType.CLOSE:
            show_exit_dialog()

    # 🔑 botón back (Android / navegación)
    def on_view_pop(e):
        show_exit_dialog()

    # 🔧 configurar eventos según plataforma
    if page.platform in [
        ft.PagePlatform.WINDOWS,
        ft.PagePlatform.LINUX,
        ft.PagePlatform.MACOS,
    ]:
        page.window.prevent_close = True
        page.window.on_event = window_event
    else:
        page.on_view_pop = on_view_pop

    # 🔑 diálogo
    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Por favor, confirme"),
        content=ft.Text("¿De verdad quieres salir de esta aplicación?"),
        actions=[
            ft.Button("Sí", on_click=handle_yes_click),
            ft.OutlinedButton("No", on_click=handle_no_click),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    # print("✅ App iniciada correctamente")  # 👈 Línea de depuración
    page.title = "Letra de tu música"
    page.theme_mode = ft.ThemeMode.DARK
    
    # ruta relativa a tu archivo .py
    # page.window.icon = r"E:\Documentos\...\src\assets\icon.ico"
    page.window.icon = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
    
    page.padding = 20
    page.bgcolor = ft.Colors.GREY_900
    # Scroll en la pagina
    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.CrossAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # Tamaño predeterminado para plataforma
    if page.platform == ft.PagePlatform.WINDOWS:
        page.window.width = 830
        page.window.height = 730
    
    artist_field = ft.TextField(
        # Texto flotante que se eleva al enfocar
        label = "Artista",
        # Placeholder, texto de ayuda
        hint_text = "Ej.: Rels B",
        # Estilos
        border_color = ft.Colors.PURPLE_400,
        focused_border_color = ft.Colors.PURPLE_300,
        cursor_color = ft.Colors.PURPLE_300,
        text_size = 16,
        filled = True,
        bgcolor = ft.Colors.GREY_800,
        border_radius = 12
    )
    
    song_field = ft.TextField(
        # Texto flotante que se eleva al enfocar
        label = "Canción",
        # Placeholder, texto de ayuda
        hint_text = "Ej.: La Última Canción",
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
        visible = True  # Cambiado a True para probar
    )
    
    eraser_btn = ft.Button(
        content = "Borrar campos",
        icon = ft.Icons.CLEANING_SERVICES,
        style = ft.ButtonStyle(
            color = ft.Colors.WHITE,
            bgcolor = ft.Colors.DEEP_PURPLE_600,
            padding = 15,
            shape = ft.RoundedRectangleBorder(radius=10),
        ),
        visible = True
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
        tooltip = "Da clic",
        col={ft.ResponsiveRowBreakpoint.MD: 4},
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
        tooltip = "Da clic",
        col={ft.ResponsiveRowBreakpoint.MD: 4},
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
        tooltip = "Da clic",
        col={ft.ResponsiveRowBreakpoint.MD: 4},
    )
    
    async def search_click(e):
        # 1. Validacion
        if not artist_field.value or not song_field.value.strip():
            result_text.value = "❌ Por favor ingresa artista y canción."
            result_text.color = ft.Colors.RED_300
            copy_btn.visible = False
            page.update()
            return
            
        # 2. Estado de carga
        search_btn.disabled = True
        eraser_btn.disabled = True
        loading.visible = True
        result_text.value = "Buscando la letra..."
        result_text.color = ft.Colors.PURPLE_300
        copy_btn.visible = False
        page.update()
        
        # 3. Llamada a la API
        data = await fetch_lyrics(artist_field.value.strip(), song_field.value.strip())
        
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
        eraser_btn.disabled = False
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
        
    async def eraser_click(e):
        artist_field.value = ""
        song_field.value = ""
        result_text.value = ""
        copy_btn.visible = False
        snack_bar = ft.SnackBar(content=ft.Text("🧹 Se borró el artista y canción."))
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
        song_field.value = cancion
        page.update()
        await search_click(e)
        
    search_btn.on_click = search_click
    eraser_btn.on_click = eraser_click
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
                ft.ResponsiveRow(
                    run_spacing={ft.ResponsiveRowBreakpoint.XS: 10},
                    controls=[
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
                            # Disposicion por tamaño
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 12,
                                ft.ResponsiveRowBreakpoint.LG: 12,
                            },
                        ),
                    ],
                ),
                
                ft.ResponsiveRow(
                    run_spacing={ft.ResponsiveRowBreakpoint.XS: 10},
                    controls=[
                        # Campos de entrada
                        ft.Container(
                            content=artist_field, width=750,
                            # Disposicion por tamaño
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 12,
                                ft.ResponsiveRowBreakpoint.LG: 12,
                            }
                        ),
                        ft.Container(
                            content=song_field, width=750,
                            # Disposicion por tamaño
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 12,
                                ft.ResponsiveRowBreakpoint.LG: 12,
                            }
                        ),
                    ],
                ),
                
                ft.ResponsiveRow(
                    run_spacing={ft.ResponsiveRowBreakpoint.XS: 10},
                    controls=[
                        # Botón de búsqueda
                        ft.Row([search_btn, loading, eraser_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=15,
                               col={ft.ResponsiveRowBreakpoint.MD: 12},),
                    ],
                ),
                
                ft.ResponsiveRow(
                    run_spacing={ft.ResponsiveRowBreakpoint.XS: 10},
                    controls=[
                        # Ejemplos para uso
                        ft.Row([labelEjemplos], alignment=ft.MainAxisAlignment.CENTER, spacing=15,
                               col={ft.ResponsiveRowBreakpoint.MD: 12}),
                        # Lista de ejemplos con responsive
                        ft.ResponsiveRow(
                            run_spacing={ft.ResponsiveRowBreakpoint.XS: 10},
                            controls=[
                                ejemploA_btn, ejemploB_btn, ejemploC_btn
                            ],
                        ),
                    ],
                ),
                
                ft.ResponsiveRow(
                    run_spacing={ft.ResponsiveRowBreakpoint.XS: 10},
                    controls=[
                        # Resultados
                        ft.Container(
                            content = resultados,
                            bgcolor = "#1A1A1A",
                            border = ft.Border.all(width=2, color=ft.Colors.PURPLE_800),
                            border_radius = 15,
                            padding = 20,
                            width = 750,
                            height = 150,
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
                            # Disposicion por tamaño
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 12,
                                ft.ResponsiveRowBreakpoint.LG: 12,
                            },
                        ),
                    ],
                ),
                
                ft.ResponsiveRow(
                    run_spacing={ft.ResponsiveRowBreakpoint.XS: 10},
                    controls=[
                        # Botón copiar
                        ft.Row([copy_btn], alignment=ft.MainAxisAlignment.CENTER,
                               # Disposicion por tamaño
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 12,
                                ft.ResponsiveRowBreakpoint.LG: 12,
                            }),
                    ],
                ),
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
            expand = True
        ),
    )
    # print("🟢 UI cargada")
    """
    if platform.system() != "Android":
        await page.window.center()
    """
    if page.platform in [ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX, ft.PagePlatform.MACOS]:
        await page.window.center()
    page.update()

# Programación asíncrona
# async/await permite que la UI siga respondiendo
# La petición se ejecuta sin bloquear
# Experiencia de usuario profesional
if __name__ == "__main__":
    ft.run(main)
ft.run(main)
