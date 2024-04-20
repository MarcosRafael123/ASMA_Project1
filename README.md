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
 5. Centros esperam um certo tempo por mais interessados. Depois enviam para cada interessado as orders que lhe foram atribuídas e as orders que outros drones também querem (negotiation needed). Centros podem recusar orders a um drone caso, já tenham sido atribuidas.
 6. Em caso de Negotiation (1 offer sealed bid auction):
    1. Cada drone envia para o center a sua proposta.
    2. Centro recebe as propostas, escolhe a melhor e envia decisão para os drones participantes.
    - Em caso de empate -> random
    - Propostas podem ser: Tempo de desvio para entregar a order, quanto tempo vão demorar a mais se não ficarem com aquela order(recalcular percurso, mas com orders que devem ser incluidas), capacidade disponivel do drone, etc...
7. Caso um drone perca a negociação, é preciso voltar a pedir aos centros as orders disponíveis, recalcular o percurso, mas agora devem ser incluídas as orders aceites anteriormente.
8. Tendo os Drones todas as orders aceites, "entregam" as orders e repete-se a execução.
9. A execução termina quando todos os drones não tiverem mais orders para entregarUm drone termina a sua execução quando nao tiver mais orders para entregar.





flow:

center manda "order_offer" para todos os drones
drone manda "order_proposal" para os centros que lhe mandaram propostas
center manda "decision" para os drones

quando acabam as orders envia "end"



short path with acceptance at 75% of capacity

drone1 : ----------STATS-----------
drone1 : Record: ['center1', 'center1', 'order1_1', 'center1', 'center1', 'order1_4', 'order1_5', 'center1', 'center1', 'order2_5', 'center1', 'center1', 'order1_6', 'center1', 'center1', 'order2_6', 'center1', 'center1', 'order2_9', 'center1', 'center1', 'order2_11', 'center1', 'center1', 'order2_12', 'order2_14', 'center1', 'center1', 'order2_17', 'center1', 'center1', 'order2_18', 'order2_19', 'center1', 'center1', 'order1_18', 'order1_19', 'center1', 'center1', 'order1_22', 'center1', 'center1', 'order1_23', 'order2_20', 'center1', 'center1', 'order2_23', 'order1_27', 'center1', 'center1', 'order2_25', 'center1', 'center1', 'order2_28', 'center1', 'center1', 'order2_29', 'center1', 'center1', 'order2_30', 'center1', 'center1', 'order2_31', 'center1', 'center1', 'order1_28', 'order2_33', 'center1', 'center1', 'order1_32', 'center1', 'center1', 'order2_36', 'center1', 'center1', 'order2_37', 'center1', 'center1', 'order2_39', 'center1', 'center1', 'order2_40', 'center1', 'center1', 'order2_41', 'center1', 'center1', 'order2_42', 'center1', 'center1', 'order1_33', 'order1_34', 'center1', 'center1', 'order1_36', 'order1_37', 'center1', 'center1', 'order1_39', 'center1', 'center1', 'order1_43', 'center1', 'center1', 'order1_45', 'order1_44', 'center1', 'center1', 'order2_45', 'order2_46', 'center1', 'center1', 'order2_51', 'center1', 'center1', 'order2_52', 'center1', 'center1', 'order2_53', 'order1_49', 'center1', 'center1', 'order1_50', 'center1', 'center1', 'order2_56', 'center1', 'center1', 'order2_58', 'order1_51', 'center1', 'center1', 'order2_60', 'order2_59', 'order2_61', 'center1', 'center1', 'order1_56', 'center1', 'center1', 'order1_59', 'order1_64', 'order2_62', 'center1', 'center1', 'order1_66', 'center1', 'center1', 'order2_63', 'center1', 'center1', 'order2_65', 'order1_67', 'center1', 'center1', 'order2_69', 'center1', 'center1', 'order2_70', 'order2_71', 'center1', 'center1', 'order2_73', 'order2_75', 'order2_78', 'center1', 'center1', 'order2_80', 'center1', 'center1', 'order1_70', 'center1', 'center1', 'order1_72', 'order1_75', 'center1', 'center1', 'order1_77', 'center1', 'center1', 'order1_80', 'center1']
drone1 : Total Delivery Time: 55197.85909260275
drone1: Total orders delivered: 75
drone1: Total number of trips: 53
drone1: Total weight carried: 940
drone1: Total distance travelled: 1103957.1818520573
drone1 : --------------------------
drone2 : ----------STATS-----------
drone2 : Record: ['center1', 'center1', 'order1_2', 'order1_3', 'center1', 'center1', 'order1_8', 'order2_1', 'order2_2', 'center1', 'center1', 'order2_7', 'order2_8', 'center1', 'center1', 'order2_15', 'center1', 'center1', 'order1_16', 'center1', 'center1', 'order2_21', 'center1', 'center1', 'order2_26', 'center1', 'center1', 'order1_29', 'center1', 'center1', 'order1_38', 'center1', 'center1', 'order1_40', 'order1_41', 'center1', 'center1', 'order1_46', 'order2_44', 'center1', 'center1', 'order2_47', 'center1', 'center1', 'order2_54', 'center1', 'center1', 'order2_55', 'center1', 'center1', 'order1_52', 'center1', 'center1', 'order1_54', 'center1', 'center1', 'order1_68', 'center1', 'center1', 'order2_72', 'center1', 'center1', 'order2_74', 'center1', 'center1', 'order2_76', 'center1', 'center1', 'order2_77', 'center1', 'center1', 'ord3', 'center2', 'center2', 'order1_55', 'center2', 'center2', 'order1_58', 'order1_57', 'center2', 'center2', 'order1_60', 'center2', 'center2', 'order1_61', 'order1_62', 'center2', 'center2', 'order1_63', 'center2', 'center2', 'order1_65', 'center2', 'center2', 'order2_67', 'order2_64', 'center2', 'center2', 'order2_68', 'center2', 'center2', 'order1_69', 'center2', 'center2', 'order2_79', 'order1_71', 'center2', 'center2', 'order1_74', 'center2']
drone3 : Total Delivery Time: 20355.117005710606
drone3: Total orders delivered: 44
drone3: Total number of trips: 32
drone3: Total weight carried: 565
drone3: Total distance travelled: 407102.340114212
drone3 : --------------------------
drone4 : ----------STATS-----------
drone4 : Record: ['center2', 'center2', 'order1_7', 'center2', 'center2', 'order1_10', 'order1_11', 'center2', 'center2', 'order1_14', 'order1_15', 'order2_16', 'center2', 'center2', 'order1_30', 'center2', 'center2', 'order1_31', 'order2_35', 'center2', 'center2', 'order2_66', 'center2']
drone4 : Total Delivery Time: 2754.8819171270297
drone4: Total orders delivered: 10
drone4: Total number of trips: 6
drone4: Total weight carried: 110
drone4: Total distance travelled: 55097.63834254058
drone4 : --------------------------



Final touches (short path | 75%cap)

drone3 : ----------STATS-----------
drone3 : Record: ['center2', 'center2', 'order2_3', 'order2_4', 'order1_8', 'center2', 'center2', 'order1_12', 'center2', 'center2', 'order1_15', 'order2_13', 'center2', 'center2', 'order1_20', 'order2_16', 'center2', 'center2', 'order1_25', 'center2', 'center2', 'order2_22', 'order2_23', 'center2', 'center2', 'order1_35', 'center2', 'center2', 'order1_42', 'center2', 'center2', 'order1_47', 'center2', 'center2', 'order1_48', 'center2', 'center2', 'order1_61', 'order1_62', 'center2', 'center2', 'order1_63', 'center2', 'center2', 'order1_65', 'center2', 'center2', 'order2_57', 'center2', 'center2', 'order2_66', 'center2', 'center2', 'order2_68', 'center2', 'center2', 'order2_72', 'center2', 'center2', 'order1_81', 'order2_79', 'center2', 'center2', 'order2_25', 'center2']
['order2_3', 'order2_4', 'order1_8', 'order1_12', 'order1_15', 'order2_13', 'order1_20', 'order2_16', 'order1_25', 'order2_22', 'order2_23', 'order1_35', 'order1_42', 'order1_47', 'order1_48', 'order1_61', 'order1_62', 'order1_63', 'order1_65', 'order2_57', 'order2_66', 'order2_68', 'order2_72', 'order1_81', 'order2_79', 'order2_25']     
drone3 : Total Delivery Time: 9948.058961020024
drone3: Total orders delivered: 26
drone3: Total number of trips: 19
drone3: Total weight carried: 350
drone3: Total distance travelled: 198961.17922040063
drone3 : --------------------------
drone4 : ----------STATS-----------
drone4 : Record: ['center2', 'center2', 'order1_10', 'order1_11', 'center2', 'center2', 'order2_10', 'order1_14', 'center2', 'center2', 'order1_24', 'center2', 'center2', 'order1_26', 'order1_28', 'center2', 'center2', 'order1_30', 'center2', 'center2', 'order2_24', 'center2', 'center2', 'order2_27', 'center2', 'center2', 'order2_32', 'order2_33', 'center2', 'center2', 'order1_45', 'order1_46', 'center2', 'center2', 'order2_38', 'center2', 'center2', 'order2_43', 'center2', 'center2', 'order1_53', 'center2', 'center2', 'order2_48', 'order1_57', 'order2_49', 'center2', 'center2', 'order1_60', 'center2', 'center2', 'order1_69', 'center2', 'center2', 'order2_65', 'order2_64', 'center2', 'center2', 'order2_36', 'center2', 'center2', 'order1_70', 'center2']
['order1_10', 'order1_11', 'order2_10', 'order1_14', 'order1_24', 'order1_26', 'order1_28', 'order1_30', 'order2_24', 'order2_27', 'order2_32', 'order2_33', 'order1_45', 'order1_46', 'order2_38', 'order2_43', 'order1_53', 'order2_48', 'order1_57', 'order2_49', 'order1_60', 'order1_69', 'order2_65', 'order2_64', 'order2_36', 'order1_70']  
drone4 : Total Delivery Time: 13467.723382323762
drone4: Total orders delivered: 26
drone4: Total number of trips: 18
drone4: Total weight carried: 315
drone4: Total distance travelled: 269354.4676464753
drone4 : --------------------------
drone2 : ----------STATS-----------
drone2 : Record: ['center1', 'center1', 'order1_1', 'center1', 'center1', 'order1_4', 'order1_5', 'center1', 'center1', 'order1_7', 'center1', 'center1', 'order1_9', 'order2_7', 'center1', 'center1', 'order2_11', 'center1', 'center1', 'order1_17', 'center1', 'center1', 'order1_18', 'order1_19', 'center1', 'center1', 'order2_17', 'center1', 'center1', 'order1_23', 'order2_19', 'center1', 'center1', 'order1_27', 'order2_21', 'center1', 'center1', 'order1_32', 'center1', 'center1', 'order1_34', 'center1', 'center1', 'order2_26', 'center1', 'center1', 'order2_28', 'center1', 'center1', 'order1_37', 'order2_29', 'center1', 'center1', 'order1_38', 'center1', 'center1', 'order1_40', 'order1_41', 'center1', 'center1', 'order2_34', 'order1_44', 'center1', 'center1', 'order2_37', 'center1', 'center1', 'order2_39', 'center1', 'center1', 'order2_40', 'center1', 'center1', 'order1_52', 'center1', 'center1', 'order2_44', 'order2_45', 'center1', 'center1', 'order1_55', 'center1', 'center1', 'order1_56', 'center1', 'center1', 'order1_59', 'order2_50', 'center1', 'center1', 'order2_54', 'center1', 'center1', 'order2_55', 'center1', 'center1', 'order2_56', 'center1', 'center1', 'order2_58', 'order1_68', 'center1', 'center1', 'order2_60', 'order2_59', 'order2_61', 'center1', 'center1', 'order2_63', 'center1', 'center1', 'order1_74', 'center1', 'center1', 'order1_75', 'order2_67', 'center1', 'center1', 'order2_70', 'order1_76', 'center1', 'center1', 'order1_77', 'center1', 'center1', 'order2_73', 'order2_75', 'order1_13', 'center1', 'center1', 'order1_21', 'order2_78', 'center1', 'center1', 'order2_80', 'center1', 'center1', 'order2_6', 'center1', 'center1', 'order1_67', 'order2_71', 'center1', 'center1', 'order1_54', 'center1', 'center1', 'order1_16', 'center1']
['order1_1', 'order1_4', 'order1_5', 'order1_7', 'order1_9', 'order2_7', 'order2_11', 'order1_17', 'order1_18', 'order1_19', 'order2_17', 'order1_23', 'order2_19', 'order1_27', 'order2_21', 'order1_32', 'order1_34', 'order2_26', 'order2_28', 'order1_37', 'order2_29', 'order1_38', 'order1_40', 'order1_41', 'order2_34', 'order1_44', 'order2_37', 'order2_39', 'order2_40', 'order1_52', 'order2_44', 'order2_45', 'order1_55', 'order1_56', 'order1_59', 'order2_50', 'order2_54', 'order2_55', 'order2_56', 'order2_58', 'order1_68', 'order2_60', 'order2_59', 'order2_61', 'order2_63', 'order1_74', 'order1_75', 'order2_67', 'order2_70', 'order1_76', 'order1_77', 'order2_73', 'order2_75', 'order1_13', 'order1_21', 'order2_78', 'order2_80', 'order2_6', 'order1_67', 'order2_71', 'order1_54', 'order1_16']
drone2 : Total Delivery Time: 43416.29074958632
drone2: Total orders delivered: 62
drone2: Total number of trips: 43
drone2: Total weight carried: 785
drone2: Total distance travelled: 868325.8149917267
drone2 : --------------------------
drone1 : ----------STATS-----------
drone1 : Record: ['center1', 'center1', 'order1_2', 'order1_3', 'center1', 'center1', 'order2_2', 'order1_6', 'center1', 'center1', 'order2_5', 'center1', 'center1', 'order2_8', 'order2_9', 'center1', 'center1', 'order2_12', 'order2_14', 'center1', 'center1', 'order2_18', 'order1_22', 'center1', 'center1', 'order1_29', 'center1', 'center1', 'order1_31', 'order1_33', 'order1_36', 'center1', 'center1', 'order2_30', 'center1', 'center1', 'order1_39', 'center1', 'center1', 'order1_43', 'center1', 'center1', 'order2_35', 'center1', 'center1', 'order1_50', 'center1', 'center1', 'order2_41', 'center1', 'center1', 'order2_42', 'center1', 'center1', 'order2_46', 'order1_58', 'center1', 'center1', 'order2_52', 'center1', 'center1', 'order1_64', 'order2_53', 'center1', 'center1', 'order1_66', 'center1', 'center1', 'order1_71', 'order2_62', 'order1_72', 'center1', 'center1', 'order1_73', 'center1', 'center1', 'order2_69', 'center1', 'center1', 'order1_78', 'order1_79', 'center1', 'center1', 'order1_80', 'center1', 'center1', 'order2_74', 'center1', 'center1', 'order2_76', 'center1', 'center1', 'order2_77', 'center1', 'center1', 'order1_51', 'order2_1', 'center1', 'center1', 'order2_15', 'center1', 'center1', 'order2_20', 'center1', 'center1', 'order2_31', 'center1', 'center1', 'order2_47', 'center1', 'center1', 'order2_51', 'center1', 'center1', 'order1_49', 'center1']
['order1_2', 'order1_3', 'order2_2', 'order1_6', 'order2_5', 'order2_8', 'order2_9', 'order2_12', 'order2_14', 'order2_18', 'order1_22', 'order1_29', 'order1_31', 'order1_33', 'order1_36', 'order2_30', 'order1_39', 'order1_43', 'order2_35', 'order1_50', 'order2_41', 'order2_42', 'order2_46', 'order1_58', 'order2_52', 'order1_64', 'order2_53', 'order1_66', 'order1_71', 'order2_62', 'order1_72', 'order1_73', 'order2_69', 'order1_78', 'order1_79', 'order1_80', 'order2_74', 'order2_76', 'order2_77', 'order1_51', 'order2_1', 'order2_15', 'order2_20', 'order2_31', 'order2_47', 'order2_51', 'order1_49']
drone1 : Total Delivery Time: 33667.50411191925
drone1: Total orders delivered: 47
drone1: Total number of trips: 34
drone1: Total weight carried: 570
drone1: Total distance travelled: 673350.0822383846
drone1 : --------------------------



drone1 : ----------STATS-----------
drone1 : Record: ['center1', 'center1', 'order1_2', 'order1_3', 'center1', 'center1', 'order1_4', 'order1_5', 'center1', 'center1', 'order1_7', 'center1', 'center1', 'order1_9', 'order2_7', 'center1', 'center1', 'order2_11', 'center1', 'center1', 'order2_12', 'order2_14', 'center1', 'center1', 'order2_17', 'center1', 'center1', 'order1_23', 'order2_19', 'center1', 'center1', 'order1_31', 'order1_33', 'order1_36', 'center1', 'center1', 'order2_30', 'center1', 'center1', 'order1_39', 'center1', 'center1', 'order1_40', 'order1_41', 'center1', 'center1', 'order1_43', 'center1', 'center1', 'order2_34', 'order1_44', 'center1', 'center1', 'order2_37', 'center1', 'center1', 'order2_39', 'center1', 'center1', 'order2_40', 'center1', 'center1', 'order1_50', 'center1', 'center1', 'order2_41', 'center1', 'center1', 'order2_42', 'center1', 'center1', 'order2_44', 'order2_45', 'center1', 'center1', 'order1_55', 'center1', 'center1', 'order1_56', 'center1', 'center1', 'order1_59', 'order2_50', 'center1', 'center1', 'order1_64', 'order2_53', 'center1', 'center1', 'order2_54', 'center1', 'center1', 'order2_58', 'order1_68', 'center1', 'center1', 'order1_71', 'order2_62', 'order1_72', 'center1', 'center1', 'order1_73', 'center1', 'center1', 'order2_69', 'center1', 'center1', 'order1_77', 'center1', 'center1', 'order2_73', 'order2_75', 'order1_13', 'center1', 'center1', 'order1_21', 'order2_78', 'center1', 'center1', 'order2_80', 'center1', 'center1', 'order1_54', 'center1', 'center1', 'order1_70', 'center1', 'center1', 'order2_20', 'center1', 'center1', 'order2_31', 'center1', 'center1', 'order2_51', 'center1', 'center1', 'order1_16', 'center1']
['order1_2', 'order1_3', 'order1_4', 'order1_5', 'order1_7', 'order1_9', 'order2_7', 'order2_11', 'order2_12', 'order2_14', 'order2_17', 'order1_23', 'order2_19', 'order1_31', 'order1_33', 'order1_36', 'order2_30', 'order1_39', 'order1_40', 'order1_41', 'order1_43', 'order2_34', 'order1_44', 'order2_37', 'order2_39', 'order2_40', 'order1_50', 'order2_41', 'order2_42', 'order2_44', 'order2_45', 'order1_55', 'order1_56', 'order1_59', 'order2_50', 'order1_64', 'order2_53', 'order2_54', 'order2_58', 'order1_68', 'order1_71', 'order2_62', 'order1_72', 'order1_73', 'order2_69', 'order1_77', 'order2_73', 'order2_75', 'order1_13', 'order1_21', 'order2_78', 'order2_80', 'order1_54', 'order1_70', 'order2_20', 'order2_31', 'order2_51', 'order1_16']
drone1 : Total Delivery Time: 41047.12971991017
drone1: Total orders delivered: 58
drone1: Total number of trips: 40
drone1: Total weight carried: 710
drone1: Total distance travelled: 820942.5943982034
drone1 : --------------------------
drone2: With path = ['center1', 'order2_71', 'center1'] Delivering...
drone4 : ----------STATS-----------
drone4 : Record: ['center2', 'center2', 'order1_10', 'order1_11', 'center2', 'center2', 'order1_12', 'center2', 'center2', 'order1_25', 'center2', 'center2', 'order2_22', 'order2_23', 'center2', 'center2', 'order2_27', 'center2', 'center2', 'order2_32', 'order2_33', 'center2', 'center2', 'order1_45', 'order1_46', 'center2', 'center2', 'order1_48', 'center2', 'center2', 'order2_43', 'center2', 'center2', 'order1_53', 'center2', 'center2', 'order2_48', 'order1_57', 'order2_49', 'center2', 'center2', 'order1_65', 'center2', 'center2', 'order2_57', 'center2', 'center2', 'order1_69', 'center2', 'center2', 'order2_66', 'center2', 'center2', 'order2_68', 'center2', 'center2', 'order1_81', 'order2_79', 'center2', 'center2', 'order2_15', 'center2']
['order1_10', 'order1_11', 'order1_12', 'order1_25', 'order2_22', 'order2_23', 'order2_27', 'order2_32', 'order2_33', 'order1_45', 'order1_46', 'order1_48', 'order2_43', 'order1_53', 'order2_48', 'order1_57', 'order2_49', 'order1_65', 'order2_57', 'order1_69', 'order2_66', 'order2_68', 'order1_81', 'order2_79', 'order2_15']
drone4 : Total Delivery Time: 10713.149450859959
drone4: Total orders delivered: 25
drone4: Total number of trips: 18
drone4: Total weight carried: 315
drone4: Total distance travelled: 214262.98901719923
drone4 : --------------------------
drone3 : ----------STATS-----------
drone3 : Record: ['center2', 'center2', 'order2_3', 'order2_4', 'order1_8', 'center2', 'center2', 'order2_10', 'order1_14', 'center2', 'center2', 'order1_15', 'order2_13', 'center2', 'center2', 'order1_20', 'order2_16', 'center2', 'center2', 'order1_24', 'center2', 'center2', 'order1_26', 'order1_28', 'center2', 'center2', 'order1_30', 'center2', 'center2', 'order2_24', 'center2', 'center2', 'order1_35', 'center2', 'center2', 'order1_42', 'center2', 'center2', 'order1_47', 'center2', 'center2', 'order2_38', 'center2', 'center2', 'order1_60', 'center2', 'center2', 'order1_61', 'order1_62', 'center2', 'center2', 'order1_63', 'center2', 'center2', 'order2_65', 'order2_64', 'center2', 'center2', 'order2_72', 'center2', 'center2', 'order2_25', 'center2', 'center2', 'order2_36', 'center2', 'center2', 'order2_6', 'center2']
['order2_3', 'order2_4', 'order1_8', 'order2_10', 'order1_14', 'order1_15', 'order2_13', 'order1_20', 'order2_16', 'order1_24', 'order1_26', 'order1_28', 'order1_30', 'order2_24', 'order1_35', 'order1_42', 'order1_47', 'order2_38', 'order1_60', 'order1_61', 'order1_62', 'order1_63', 'order2_65', 'order2_64', 'order2_72', 'order2_25', 'order2_36', 'order2_6']
drone3 : Total Delivery Time: 13926.982485959035
drone3: Total orders delivered: 28
drone3: Total number of trips: 20
drone3: Total weight carried: 365
drone3: Total distance travelled: 278539.6497191809
drone3 : --------------------------
drone2 : ----------STATS-----------
drone2 : Record: ['center1', 'center1', 'order1_1', 'center1', 'center1', 'order2_2', 'order1_6', 'center1', 'center1', 'order2_5', 'center1', 'center1', 'order2_8', 'order2_9', 'center1', 'center1', 'order1_17', 'center1', 'center1', 'order1_18', 'order1_19', 'center1', 'center1', 'order2_18', 'order1_22', 'center1', 'center1', 'order1_27', 'order2_21', 'center1', 'center1', 'order1_29', 'center1', 'center1', 'order1_32', 'center1', 'center1', 'order1_34', 'center1', 'center1', 'order2_26', 'center1', 'center1', 'order2_28', 'center1', 'center1', 'order1_37', 'order2_29', 'center1', 'center1', 'order1_38', 'center1', 'center1', 'order2_35', 'center1', 'center1', 'order1_52', 'center1', 'center1', 'order2_46', 'order1_58', 'center1', 'center1', 'order2_52', 'center1', 'center1', 'order2_55', 'center1', 'center1', 'order1_66', 'center1', 'center1', 'order2_56', 'center1', 'center1', 'order2_60', 'order2_59', 'order2_61', 'center1', 'center1', 'order2_63', 'center1', 'center1', 'order1_74', 'center1', 'center1', 'order1_75', 'order2_67', 'center1', 'center1', 'order2_70', 'order1_76', 'center1', 'center1', 'order1_78', 'order1_79', 'center1', 'center1', 'order1_80', 'center1', 'center1', 'order2_74', 'center1', 'center1', 'order2_76', 'center1', 'center1', 'order2_77', 'center1', 'center1', 'order1_51', 'order2_1', 'center1', 'center1', 'order1_67', 'order1_49', 'center1', 'center1', 'order2_47', 'center1', 'center1', 'order2_71', 'center1']
['order1_1', 'order2_2', 'order1_6', 'order2_5', 'order2_8', 'order2_9', 'order1_17', 'order1_18', 'order1_19', 'order2_18', 'order1_22', 'order1_27', 'order2_21', 'order1_29', 'order1_32', 'order1_34', 'order2_26', 'order2_28', 'order1_37', 'order2_29', 'order1_38', 'order2_35', 'order1_52', 'order2_46', 'order1_58', 'order2_52', 'order2_55', 'order1_66', 'order2_56', 'order2_60', 'order2_59', 'order2_61', 'order2_63', 'order1_74', 'order1_75', 'order2_67', 'order2_70', 'order1_76', 'order1_78', 'order1_79', 'order1_80', 'order2_74', 'order2_76', 'order2_77', 'order1_51', 'order2_1', 'order1_67', 'order1_49', 'order2_47', 'order2_71']
drone2 : Total Delivery Time: 35121.634952366454
drone2: Total orders delivered: 50
drone2: Total number of trips: 36
drone2: Total weight carried: 630
drone2: Total distance travelled: 702432.6990473293
drone2 : --------------------------