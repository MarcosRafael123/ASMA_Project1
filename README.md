# ASMA_Project1

## Compilation and execution

- Activate virtual enviroment (python 3.9.5)
- Install requirements if needed: pip install -r requirements.txt
- Start XMPP server (hostname used: localhost) (Change hostname global varible on enviroment.py if needed)
- Run the program: python .\enviroment.py


Flow Inicial proposto:

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


Flow:

1. The environment parses the dataset, creates, initializes, and starts all the agents.
2. The center agent has several orders to deliver. Sends to all drones a message representing an offer with the first order. -> "order_offer"
3. Drone agents receive all the offers from the centers, evaluate each order, and formulate proposals to be sent to the center agents in response to their offers. -> "order_proposal"
4. Center agents receive all the proposals from the drones and select the best proposal for the offer. Send to each drone the decision about its proposal. -> "decision"
5. Drone agents receive the decisions for each proposal they send. Add an order if the decision is positive.
6. Drone agents decide whether to continue on the center and await more orders before delivery or to deliver their current orders according to their current capacity.
7. If the drone’s decision is to deliver the current assigned orders, the drone delivers the packages. Drones always deliver orders on the shortest route possible and end at a center to recharge.
8. Go to step 2. Execution is ended when all the centers have no undelivered orders. -> "end"
9. When execution ends. If drones still have assigned orders, deliver them. Statistics about the delivery of packages are shown, and agents are stopped.