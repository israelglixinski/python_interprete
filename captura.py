
from googletrans import Translator
from datetime import datetime
from threading import Thread
import sounddevice as sd
import soundfile as sf
from time import sleep
import numpy as np
import asyncio
import whisper
import shutil
import os



# Modelo "base" é equilibrado entre velocidade e qualidade
model = whisper.load_model("base")  



# Configurações de áudio
DURATION        = 5             # Duração total da gravação em segundos
SAMPLERATE      = 44100
DEVICE_INDEX    = 27            # Ajuste para o seu dispositivo
OVERLAP         = 4             # Tempo entre cada volta
# Funciona da seguinte forma: a cada {OVERLAP} segundos pega os ultimos {DURATION} segundos de gravação



# Define os códigos ANSI para cores
BRANCO      = "\033[97m"    # Branco
AMARELO     = "\033[93m"    # Amarelo
CINZA       = "\033[90m"    # Cinza
RESET       = "\033[0m"     # Reseta para a cor padrão do terminal



def apagar_arquivo(nome_arquivo):
    tentativas = 4
    sleep(4)
    while tentativas > 0:
        try: 
            os.remove(nome_arquivo)
            break
        except:
            sleep(1)
            tentativas -=1
    pass



def esvazia_pasta(pasta):
    if os.path.exists(pasta):
        for item in os.listdir(pasta):
            caminho_completo = os.path.join(pasta, item)
            try:
                if os.path.isfile(caminho_completo) or os.path.islink(caminho_completo):
                    os.unlink(caminho_completo)
                elif os.path.isdir(caminho_completo):
                    shutil.rmtree(caminho_completo)
            except Exception as e:
                print(f"{CINZA}Não foi possível remover {caminho_completo}. Motivo: {e}{RESET}")
    else:
        print(f"{CINZA}A pasta '{pasta}' não existe.{RESET}")
    # deixa um arquivo de toque para não apagar a pasta ao fazer o clone do repositorio.
    arquivo_de_toque = open(f'{pasta}/toque.txt','a')
    arquivo_de_toque.write('.')
    arquivo_de_toque.close()


def traduzir(texto_original):
    async def trans_google(texto):
        translator = Translator()
        try:
            traducao = await translator.translate(texto, src="en", dest="pt")               # Aguarda a resposta
            return traducao.text                                                            # Retorna a tradução
        except Exception as e:
            print(f"{CINZA}Erro ao traduzir:{RESET}", e)
            return None                                                                     # Retorna None em caso de erro
    async def main(texto_original):
        traducao = await trans_google(texto_original)
        if traducao:
            print(f'{AMARELO}{traducao}{RESET}')
    asyncio.run(main(texto_original))                                                       # Executa a função assíncrona



def transcrever(filename="gravacao_sistema.wav"):
    print('\n')

    try: 
        result = model.transcribe(filename)
        print(f'{BRANCO}{result["text"]}{RESET}')
        Thread(target=lambda:traduzir(result["text"])).start()
    except: 
        print(f"{CINZA}Não foi possivel transcrever{RESET} \n")

    Thread(target=lambda:apagar_arquivo(filename)).start()



def captura_som():
    """
    Captura áudio continuamente e salva em arquivos sobrepostos.
    """
    # Obtém informações do dispositivo
    device_info = sd.query_devices(DEVICE_INDEX)
    max_channels = device_info['max_input_channels']                                        # Número de canais suportados
    num_channels = 2 if max_channels >= 2 else 1                                            # Usa 2 canais se possível

    # Buffer para armazenar os últimos 6 segundos de áudio
    buffer_size = DURATION * SAMPLERATE
    audio_buffer = np.zeros((buffer_size, num_channels), dtype=np.float32)

    # Callback para captura contínua
    def callback(indata, frames, time, status):
        if status:
            print(f"{CINZA}Erro na gravação: {status}{RESET}")
        nonlocal audio_buffer
        # Desloca o buffer para trás e adiciona os novos frames no final
        audio_buffer = np.roll(audio_buffer, -frames, axis=0)
        audio_buffer[-frames:] = indata

    # Inicia a captura contínua
    with sd.InputStream(samplerate=SAMPLERATE, channels=num_channels,
                        dtype="float32", device=DEVICE_INDEX, callback=callback):
        while True:
            nome_arquivo = "captura/" + datetime.now().strftime('%Y%m%d%H%M%S') + ".wav"
            sf.write(nome_arquivo, audio_buffer, SAMPLERATE)  # Salva o áudio
            
            # print(f"Salvo: {nome_arquivo}")
            Thread(target=lambda:transcrever(nome_arquivo)).start()

            sd.sleep(OVERLAP * 1000)                                                        # Espera 3 segundos antes de salvar o próximo trecho



# Inicia a gravação contínua em uma thread
if __name__ == '__main__':
    esvazia_pasta('captura')
    Thread(target=captura_som, daemon=True).start()
    input("Pressione ENTER para sair...\n")                                                 # Mantém o programa rodando
