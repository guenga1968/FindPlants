import flet as ft
import requests
import base64
from PIL import Image
import io

# API Key de Plant.id (regístrate en https://plant.id/api)
API_KEY = "TU_API_KEY_DE_PLANT.ID"  # Reemplaza esto con tu API Key

def main(page: ft.Page):
    page.title = "Identificador de Plantas 🌿"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor= ft.Colors.BLUE_GREY_800
    
    

    def pick_image(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]
            img_path = selected_file.path
            img = Image.open(img_path)
            
            imagen= ft.Image(src=img_path, width=300, height=300)
            page.add(imagen)
            page.update()
            
            # Redimensionar imagen para que no sea demasiado grande
            img.thumbnail((500, 500))
            
            # Convertir imagen a base64 (requerido por Plant.id)
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            # Llamar a la API de Plant.id
            response = identify_plant(img_base64)
            
            if response:
                plant_name = response.get("suggestions", [{}])[0].get("plant_name", "Desconocido")
                probability = response.get("suggestions", [{}])[0].get("probability", 0) * 100
                
                result_text.value = (
                    f"🌱 **Planta identificada:** {plant_name}\n"
                    f"📊 **Probabilidad:** {probability:.2f}%"
                )
            else:
                result_text.value = "❌ No se pudo identificar la planta."
            
            page.update()

    def identify_plant(image_base64):
        url = "https://api.plant.id/v2/identify"
        headers = {"Api-Key": API_KEY}
        payload = {
            "images": [image_base64],
            "modifiers": ["crops_fast", "similar_images"],
            "plant_language": "es"  # Opcional: idioma español
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            print(f"Error al llamar a la API: {e}")
            return None

    # Componentes de la UI
    file_picker = ft.FilePicker(on_result=pick_image)
    result_text = ft.Text("Sube una foto de una planta para identificarla.", size=18)
    
    page.overlay.append(file_picker)
    page.add(
        ft.AppBar(
            center_title=True,
            leading=ft.Icon(name=ft.Icons.NATURE),
            title=ft.Text("Identificador de Plantas", size=24, weight=ft.FontWeight.BOLD),
            bgcolor="green",
            color="white",),
            
        ft.Column( 
            [
                
                ft.ElevatedButton(
                    "Subir Foto",
                    icon=ft.Icons.PHOTO_CAMERA,
                    on_click=lambda _: file_picker.pick_files(
                        allowed_extensions=["jpg", "jpeg", "png"],
                        dialog_title="Selecciona una foto de planta",
                   
                    ),
                    style=ft.ButtonStyle(padding=20, shape=ft.RoundedRectangleBorder(radius=10), bgcolor="green", color="white"),
                ),
                result_text,
            ],
            spacing=50,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
           
        )
    )

ft.app(target=main, upload_dir="uploads")