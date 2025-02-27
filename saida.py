
from googletrans import Translator
from dotenv import load_dotenv
from datetime import datetime
import requests
import asyncio
import banco
import os



load_dotenv()



subscription_key    = os.getenv("subscription_key")
endpoint            = os.getenv("endpoint")



def traduzir(texto_original):
    async def trans_google(texto_original):
        translator = Translator()
        try:
            traducao = await translator.translate(texto_original, src="pt", dest="en")      # Aguarda a resposta
            return traducao.text                                                            # Retorna a tradução
        except Exception as e:
            print("Erro ao traduzir:", e)
            return None                                                                     # Retorna None em caso de erro
    async def main(texto_original):
        traducao = await trans_google(texto_original)
        if traducao: 
            # print(traducao)
            return traducao
    return asyncio.run(main(texto_original))                                                # Executa a função assíncrona



def texto_para_som(texto):

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm"
    }

    # ssml = f"""
    # <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='pt-BR'>
    #     <voice name='pt-BR-FranciscaNeural'>{texto}</voice>
    # </speak>
    # """
    
    # en-US-DavisNeural
    # en-US-GuyNeural
    # en-US-JasonNeural

    ssml = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
        <voice name='en-US-JasonNeural'>{texto}</voice>
    </speak>
    """

    response = requests.post(endpoint, headers=headers, data=ssml.encode('utf-8'))

    nome_arquivo = "saida/" + datetime.now().strftime('%Y%m%d%H%M%S') + ".wav"

    if response.status_code == 200:
        with open(nome_arquivo, "wb") as file:
            file.write(response.content)
        # print("Arquivo de áudio salvo como 'output.wav'")
        return nome_arquivo
    else:
        # print("Erro:", response.text)
        return 'erro'



def gerar_frase_em_ingles(frase_em_portugues):
    
    frase_em_ingles = traduzir(frase_em_portugues)
    # print(frase_em_ingles)
    audio_em_ingles = texto_para_som(frase_em_ingles)

    banco.insert_nova_saida(
      nome_arquivo = audio_em_ingles
    , portugues = frase_em_portugues
    , ingles = frase_em_ingles
    )
    return {
      'nome_arquivo'    : audio_em_ingles
    , 'portugues'       : frase_em_portugues
    , 'ingles'          : frase_em_ingles
    }
    # retornar dicionario



def retornar_existentes():
    
    pass



if __name__ == "__main__":
    # traduzir('olá bom dia tudo bom?')
    # texto = f"""Hello, this is a brief voice test for using a program."""
    # texto_para_som(texto)
    # frase = gerar_frase_em_ingles('É um prazer estar aqui!')
    # print(frase)
    pass