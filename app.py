import sys
from models.chatgpt import ChatGpt

def main():
    chatgpt = ChatGpt()

    if chatgpt.preference is None:
        chatgpt.cambiar_preferencia()

    while True:
        if chatgpt.preference == 'e':
            prompt = input('Prompt (S=Salir): ')
            if prompt.lower() == "s":
                chatgpt.cerrar()
                sys.exit()
            else:
                respuesta = chatgpt.chatear(prompt)
                print(f'{respuesta}\n')
        elif chatgpt.preference == 'h':
            prompt = chatgpt.escuchar()
            if prompt:
                respuesta = chatgpt.chatear(prompt)
                print(f'{respuesta}\n')
        else:
            print("La preferencia es inválida o no se ha establecido correctamente.")
            chatgpt.cambiar_preferencia()

if __name__ == "__main__":
    main()
