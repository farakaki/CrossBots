import random
import time
saldo = 0

def main():
    global saldo
    while True:
        print("1. Blackjack\n2. Roleta\n3. Caça níquel\n4. Dinheiro\n5. Fechar o cassino") #Menu de opção principal
        opc = int(input("Escolha uma opção: "))
        if opc == 1:
            blackjack()
        elif opc == 2:
            roleta()
        elif opc == 3:
            caçaniquel()
        elif opc == 4:
            dinheiro()
        elif opc == 5: #Fechar o programa
            return 0
        else: #Tratar caso o usuário não digite um número das opções
            print("Não é uma opção")
            return 0

def dinheiro():
    global saldo
    while True:
        print("1. Adicionar saldo\n2. Remover Saldo\n3. Saldo\n4. Voltar ao menu de jogos") #Menu da função dinheiro()
        opc = int(input("Qual opção você deseja? "))
        if opc == 1:
            valor = int(input("Quantos créditos você deseja adcionar? "))
            saldo += valor
        elif opc == 2:
            valor = int(input("Quantos créditos você deseja remover? "))
            saldo -= valor
        elif opc == 3:
            print(f"Seu saldo atual é {saldo}")
        elif opc == 4: 
            return 0
        else: #Traatar caso o usuário erre
            print("Essa opção não é válida")

def blackjack():
    global saldo
    naipe_cartas = ["♥", "♦", "♣",  "♠"]
    valor_cartas = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def escolher_carta():
        carta_naipe = naipe_cartas[random.randint(0, 3)] #Escolhe o naipe 
        numero_valor = random.randint(0, 12) #Escolhe o valor da carta
        carta_valor = valor_cartas[numero_valor] 
        carta_escolhida = carta_valor + carta_naipe


        if numero_valor >= 9:  #Esse if serve para as cartas de símbolo terem valor = 10
            valor = 10
        else:
            valor = numero_valor + 1  #Esse else serve para que o valores da cartas sejam seus próprios números(antes eram os índices da lista)

        return [carta_escolhida, valor]

    def carta_igual(carta, cartas_usadas): #Não permitir que uma carta saia repetida
        if carta[0] in cartas_usadas:
            nova_carta = escolher_carta()
            return carta_igual(nova_carta, cartas_usadas)
        else:
            return carta #função recursiva

    def imprimir_cartas(cartas_dealer, cartas_jogador): #Ganhar tempo e não ter que digitar essa impressão toda vez
        print("\nCartas Jogador: ")
        for carta in cartas_jogador:
            print(carta)
        print("\nCartas Dealer: ")
        for carta in cartas_dealer:
            print(carta)

    while True:
        soma_dealer = 0 #soma das cartas recebidas pelo dealer
        soma_jogador = 0 #soma das cartas recebidas pelo jogador
        cartas_jogador = [] #lista com todas as cartas já saídas, será usada na função carta_igual()
        cartas_dealer = [] #Lista que será adicionado as cartas que o dealer recebeu
        cartas_usadas = [] #Lista que será adicionado as cartas que o jogador recebeu

        print(f"\nSaldo atual: {saldo}")
        print("Você está jogando BLACKJACK")
        print("Valor mínimo de aposta: 50 créditos")
        decisao = input("Deseja jogar? (s/n): ")
        
        if decisao == 's':
            aposta = int(input("Quanto você deseja apostar? "))
            
            if aposta <= saldo:
                saldo -= aposta
                
                j0 = escolher_carta()
                soma_jogador += j0[1]
                cartas_usadas.append(j0[0])
                cartas_jogador.append(j0[0])

                d0 = escolher_carta()
                soma_dealer += d0[1]
                cartas_usadas.append(d0[0])
                cartas_dealer.append(d0[0])

                imprimir_cartas(cartas_dealer, cartas_jogador)

                while True:
                    escolha = int(input("\nVocê deseja:\n1. Parar\n2. Pedir carta\n")) #Escolha se o jogador quer comprar mais carta ou não
                    
                    if escolha == 1:
                        print("\nCartas Dealer:\n")
                        while soma_dealer < 17: #Estratégia do dealer, sempre pedir até chegar no mínimo em 17
                            d = carta_igual(escolher_carta(), cartas_usadas)
                            cartas_dealer.append(d[0])
                            cartas_usadas.append(d[0])
                            soma_dealer += d[1]
                            imprimir_cartas(cartas_dealer, cartas_jogador)
                            time.sleep(3) #Deixar o jogo com mais suspense e não imprimir um monte de informação no terminal de uma vez
                            if soma_dealer > 21: #Caso o dealer passe de 21
                                print("O dealer estourou! Você venceu!")
                                saldo += aposta * 2
                                break
                        break 
                    
                    elif escolha == 2: #Usuário pedindo mias carta
                        j = carta_igual(escolher_carta(), cartas_usadas)
                        cartas_jogador.append(j[0])
                        cartas_usadas.append(j[0])
                        soma_jogador += j[1]
                        imprimir_cartas(cartas_dealer, cartas_jogador)
                        
                        if soma_jogador > 21: #Caso usuário estoure
                            print("Você estourou! Dealer venceu!")
                            break

                if soma_jogador <= 21: #Condições para ver quem venceu(quem tem maior soma sem estourar)
                    if soma_dealer <= 21:
                        if soma_jogador > soma_dealer:
                            print("Parabéns, você venceu!")
                            saldo += aposta * 2
                        elif soma_jogador < soma_dealer:
                            print("Você perdeu HAHAHA")
                        else:
                            print("Empate! Não perde nem ganha")
                            saldo += aposta

            else:
                print("Esse valor excede seu saldo, adicione saldo.")
        elif decisao == 'n':
            print("Você saiu do jogo.")
            break
        else:
            print("Opção inválida! Digite 's' ou 'n'.")

def roleta():
    global saldo
    lucro = 0
    teste = False #Caso a aposta escolhida seja sortesado teste receberá True
    num_vermelho = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]#Como números pretos e vermelhos não tem uma lógica esrevi uma lista com eles
    num_preto = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    while True:
        print(f"Seu saldo atual é {saldo}")
        print("Você esá jogando ROLETA")
        escolha = input("Você deseja jogar? (s/n) ")
        if escolha == 's':
            valor_aposta = int(input(f"Quanto você deseja apostar? "))
            if valor_aposta <= saldo:
                saldo -= valor_aposta
                print("""1. Número
2. Vermelho
3. Preto
4. Par
5. Ímpar
6. Rua
7. Coluna
8. Dúzia""")#Menu com opções de aposta
                opc = int(input("Onde você deseja apostar? "))
                numero = random.randint(0, 36)
                if opc == 1:
                    num_escolhido = int(input("Digite um número entre 1 e 36 "))
                    if numero == num_escolhido:
                        teste = True
                        lucro = 35*valor_aposta
                elif opc == 2:
                    if numero in num_vermelho:
                        teste == True
                        lucro = 2*valor_aposta
                elif opc == 3:
                    if numero in num_preto:
                        teste = True
                        lucro = 2*valor_aposta
                elif opc == 4:
                    if numero % 2 == 0:
                        teste = True
                        lucro = 2*valor_aposta
                elif opc == 5:
                    if numero % 2 != 0:
                        teste = True
                        lucro = 2*valor_aposta
                elif opc == 6:
                    print("Cada rua possui 3 números")
                    linha = int(input("Escolha uma linha entre 1 e 12: "))
                    if linha * 3 == numero or (linha * 3) - 1 == numero or (linha * 3) - 2 == numero:
                        teste = True
                        lucro = 11*valor_aposta
                elif opc == 7:
                    coluna = int(input("Escolha entre a coluna 1, 2, 3: "))
                    if coluna == 1 and numero % 3 == 1:
                        teste == True
                        lucro = 4*valor_aposta
                    if coluna == 2 and numero % 3 == 2:
                        teste == True
                        lucro = 4*valor_aposta          
                    if coluna == 3 and numero % 3 == 0:
                        teste == True
                        lucro = 4*valor_aposta
                elif opc == 8:
                    duzia = int(input("Escolha entre a primeira, segunda e terceira dúzia: "))
                    if duzia == 1 and 1 <= numero <= 12:
                        teste == True
                        lucro = 4*valor_aposta                         
                    if duzia == 2 and 13 <= numero <= 24:
                        teste == True
                        lucro = 4*valor_aposta
                    if duzia == 3 and 25 <= numero <= 36:
                        teste == True
                        lucro = 4*valor_aposta

                print("\nEscolhendo o número!!")
                time.sleep(4) #Causar impressaõ visual melhor no código
                print("O número escolhido foi...")
                time.sleep(2)
                print(numero)
                if teste == True:
                    print("\nParabéns!! Você ganhou")
                    print(f"Prêmio de {lucro}\n")
                    saldo += lucro
                    time.sleep(2)
                elif teste == False:
                    if numero == 0:
                        print("\nA banca leva tudo!!\n")
                        time.sleep(2)
                    else:
                        print("\nVocê perdeu HAHAH\n")
                        time.sleep(2)
                    
                
            else:
                print("Seu saldo atual não é suficiente, adicione créditos")
                break
        elif escolha == 'n':
            break
        else: 
            print("Você não sigitou nem 's' ou 'n'")
            continue
        
def caçaniquel():
    global saldo 
    lista_simbolo = ["!", "@", "#", "$", "%", "&", "*", "|"] # essa lista são os símbolos possíveis de escolha
    simbolo_escolhido = []
    while True:
        print("Você está jogando caça-níquel")
        print("Valor único de aposta 100 créditos")
        apostar = input("Deseja apostar?(s/n)\n")
        if apostar == 's':
            if saldo >= 100:
                print("VAMOS COMEÇAR O JOGO!")
                for i in range(3):
                    simbolo_escolhido.append(random.choice(lista_simbolo))#Escolha aleatória de 3 símbolos
                    time.sleep(3)
                    print(simbolo_escolhido[i])
                if simbolo_escolhido[0] == simbolo_escolhido[1] == simbolo_escolhido[2]:
                    print("VOCÊ GANHOU O JACKPOT!!")
                    print("PRÊMIO: 100.000")
                    saldo += 100000
                else:
                    print("Não foi dessa vez!")
                    saldo -= 100
                    resposta = input("Deseja jogar novamente? (s/n)")
                    if resposta == 's':
                        continue
                    else:
                        return 0
            else: 
                print("Você não tem créditos suficientes, volte no menu principal e adcione créditos")
                return 0
        elif apostar == 'n':
            return 0
        else:
            print("Você não digitou 's' ou 'n'")

main()