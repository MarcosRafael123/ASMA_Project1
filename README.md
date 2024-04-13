# ASMA_Project1


Create the following users on the server:

center1 center1
center2 center2

drone1 drone1
drone2 drone2
drone3 drone3
drone4 drone4



- No drone, criar o algoritmo para o drone escolher a partir das orders disponíveis um percurso de entrega de orders. Deve-se também criar uma variação desse algoritmo, mas que receba uma lista de orders que têm que ser incluídas obrigatoriamente no percurso.
    - Deve-se maximizar nº de entregas e minimizar tempo de entrega.
    - Lembrar que os drones podem recarregar nos centros.
    - Criar várias heuristicas/metodos para serem testados e avaliados.
    - Exemplo de percurso: center1 - order1_3 - order1_4 - center2 - order2_7 - order1_2 - center3


- Protocolo em caso de negociação (para casos em que mais que um drone está interessado numa mesma order) (se os mesmos drones estao interessados nas mesmas duas (ou mais) orders -> começa-se por negociar a order com menor ID -> Indicar ao centro que quer começar negociação) (se um drone sofrer timeout perde a negociação)

- Avaliação da eficiencia do sistema de entrega -> Cada drone possuirá no fim da execução uma lista completa do percurso que realizou.
    - ex: center1 - order1_3 - order1_4 - center2 - order2_7 - order1_2 - center1
    - Calcular quanto tempo cada drone demorou, quantas entregas entregou, quanta distancia percorreu, quantos kilos carregou.
    Fazer estatisticas gerais para o sistema (para todos os drones) (media,  mediana)
    - Enunciado: "tempo de
entrega (pode ser medido em distância percorrida) total, médio, mínimo e máximo, taxa de
ocupação de drones e consumo de energia"


Flow proposto:

Drones e centros são iniciados

 1. Drones pedem as orders aos centros (que conseguem alcançar, tendo em conta a sua autonomia)
 2. Centros enviam as suas orders para os drones que as pediram
 3. Drones escolhem as orders que pretendem entregar (de uma só vez, antes de voltar a um centro) (Definem um percurso inicial) -> Heuristica
 4. Enviam para os centros as orders que estão interessados.
 5. Centros esperam um certo tempo por mais interessados. Depois enviam para cada interessado as orders que lhe foram atribuídas e as orders que outros drones também querem (negotiation needed).
 6. Em caso de Negotiation (1 offer sealed bid auction):
    1. Cada drone envia para o center a sua proposta.
    2. Centro recebe as propostas, escolhe a melhor e envia decisão para os drones participantes.
    - Em caso de empate -> random
    - Propostas podem ser: Tempo de desvio para entregar a order, quanto tempo vão demorar a mais se não ficarem com aquela order(recalcular percurso, mas com orders que devem ser incluidas), capacidade disponivel do drone, etc...
7. Caso um drone perca a negociação, é preciso voltar a pedir aos centros as orders disponíveis, recalcular o percurso, mas agora devem ser incluídas as orders aceites anteriormente.
8. Tendo os Drones todas as orders aceites, "entregam" as orders e repete-se a execução.
9. A execução termina quando todos os drones não tiverem mais orders para entregarUm drone termina a sua execução quando nao tiver mais orders para entregar.
