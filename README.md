# Interprete de Audio com Tradução Automática

Este é um projeto Python que captura áudio do sistema, transcreve palavras em inglês e traduz automaticamente para o português. Também permite gerar áudio em inglês a partir de textos em português e salva as informações em um banco de dados.

## Funcionalidades

- Captura de áudio do sistema e transcrição para inglês.
- Tradução automática para português.
- Tradução de texto do português para inglês e geração de áudio.
- Armazenamento das informações em um banco de dados.
- Interface para visualizar e gerar novos áudios.

## Estrutura do Projeto

- `captura.py` - Escuta o som do sistema, transcreve para inglês e traduz para português.
- `saida.py` - Traduz textos do português para inglês, gera áudio e salva no banco de dados.
- `banco.py` - Gerencia o banco de dados.
- `tela.py` - Interface para visualizar e gerar novos áudios.
- `captura/` - Pasta onde são armazenados os áudios capturados.
- `saida/` - Pasta onde são armazenados os áudios gerados.
- `.env` - Arquivo de configuração com credenciais.
- `requirements.txt` - Dependências do projeto.

## Requisitos

Para executar este projeto, é necessário:

- Python 3.8+
- Conta no Azure Speech Service
- Opcional, mas recomendado - VB-Audio Virtual Cable
- Opcional, mas recomendado - Voicemeeter Banana

Instale as dependências com:
```sh
pip install -r requirements.txt
```

## Como Usar

1. Configure suas credenciais no arquivo `.env` (veja `.env_example`).
2. Execute o `captura.py` para iniciar a captura de áudio e tradução.
```sh
python captura.py
```
3. Para gerar novos áudios a partir de textos em português, execute:
```sh
python tela.py
```

## Licença

Este projeto está licenciado sob a MIT License.
