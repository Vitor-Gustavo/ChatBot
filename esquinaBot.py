import requests
import time
import json
import os


# Ler as mensagens que estão chegando
class TelegramBot:
    def __init__(self):
        token = '1719474905:AAGZkleGFwkVywKaSPXOD7khnVGa47PbCW0'
        self.url_base = f'https://api.telegram.org/bot{token}/'

    # iniciar o bot
    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_mensagens(update_id)
            mensagens = atualizacao['result']
            if mensagens:
                for mensagem in mensagens:
                    update_id = mensagem['update_id']
                    chat_id = mensagem['message']['from']['id']
                    eh_primeira_msg = mensagem['message']['message_id'] == 1
                    resposta = self.criar_resposta(mensagem,eh_primeira_msg)
                    self.responder(resposta,chat_id)

    # obter mensagens
    def obter_mensagens(self,update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    # criar uma resposta
    def criar_resposta(self,mensagem,eh_primeira_msg):
        mensagem = mensagem['message']['text']
        if eh_primeira_msg == True or mensagem.lower() == 'menu':
            return f'''Olá bem vindo a nossa hamburgueria. Digite o número do seu hamburguer que gostaria de pedir:
            {os.linesep} 1 - TRIPLO CHEDDAR{os.linesep} 2 - DUPLO BACON{os.linesep} 3 - QUARTETO FANTASTICO{os.linesep} 4 - SUPER DO CHEF{os.linesep} 5 - FRANGO X'''
        if mensagem == '1':
            return f'''TRIPLO CHEDDAR - R$20,00{os.linesep}Confirmar pedido(s/n)'''
        if mensagem == '2':
            return f'''DUPLO BACON - R$15,00{os.linesep}Confirmar pedido(s/n)'''
        if mensagem == '3':
            return f'''QUARTETO FANTASTICO - R$28,00{os.linesep}Confirmar pedido(s/n)'''
        if mensagem == '4':
            return f'''SUPER DO CHEF - R$21,00{os.linesep}Confirmar pedido(s/n)'''
        if mensagem == '5':
            return f'''FRANGO X - R$10,00{os.linesep}Confirmar pedido(s/n)'''
        
        if mensagem.lower() in ('s','sim'):
            return 'Pedido confirmado com sucesso!'
        else:
           return 'Gostaria de acessar o menu? Digite "menu"'
        
    # responder as mensagens
    def responder(self,resposta,chat_id):
        link_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_envio)


bot = TelegramBot()
bot.Iniciar()