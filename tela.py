import flet as ft
import pygame
import banco
import saida


# Inicializa o mixer do pygame para reprodução de áudio
pygame.mixer.init()

consulta = banco.select_saidas_existentes()

def main(page: ft.Page):
    page.title = "Reprodutor de Áudio"
    page.scroll = "auto"

    def play_audio(e, nome_arquivo):
        try:
            pygame.mixer.music.load(nome_arquivo)
            pygame.mixer.music.play()
        except Exception as err:
            print(f"Erro ao reproduzir {nome_arquivo}: {err}")

    def stop_audio(e):
        pygame.mixer.music.stop()

    def add_container(texto):
        if not texto:
            return
        
        novo_item = saida.gerar_frase_em_ingles(texto)
        
        consulta.append(novo_item)
        
        container = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.ElevatedButton("▶ Play", on_click=lambda e, n=novo_item["nome_arquivo"]: play_audio(e, n)),
                            ft.ElevatedButton("⏹ Stop", on_click=stop_audio)
                        ]
                    ),
                    ft.Text(novo_item["ingles"], color=ft.Colors.BLUE, size=18),
                    ft.Text(novo_item["portugues"], color=ft.Colors.YELLOW, size=18)
                ],
                spacing=5
            ),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY),
            border_radius=5,
            margin=5
        )
        
        lista_containers.controls.append(container)
        page.update()

    entrada_texto = ft.TextField(label="Digite a frase em português", width=300)
    botao_adicionar = ft.ElevatedButton("Adicionar", on_click=lambda e: add_container(entrada_texto.value))
    
    lista_containers = ft.Column()
    
    for item in consulta:
        nome_arquivo = item["nome_arquivo"]
        
        container = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.ElevatedButton("▶ Play", on_click=lambda e, n=nome_arquivo: play_audio(e, n)),
                            ft.ElevatedButton("⏹ Stop", on_click=stop_audio)
                        ]
                    ),
                    ft.Text(item["ingles"], color=ft.Colors.BLUE, size=18),
                    ft.Text(item["portugues"], color=ft.Colors.YELLOW, size=18)
                ],
                spacing=5
            ),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY),
            border_radius=5,
            margin=5
        )
        lista_containers.controls.append(container)
    
    page.add(
        ft.Row([entrada_texto, botao_adicionar]),
        lista_containers
    )
    
    page.update()

# Rodar a aplicação Flet
ft.app(target=main)
