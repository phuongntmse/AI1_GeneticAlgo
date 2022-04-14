# AI1_GeneticAlgo
Consider a function y=f(x) taking its values from [0..1]. We want to find the minimum of this function (the minimum value is not one of the bounds) by applying a genetic algorithm.

Soit une fonction y=f(x) prenant ses valeurs sur [0..1]. On souhaite trouver le minimum de cette fonction (la valeur minimum n'est pas l'une des bornes) en appliquant un algorithme génétique.

Indications

1 - Codage des données : Codage binaire
  - Pour un codage par octet (8 bits), on procède comme suit : pour toute valeur réelle de x, on prend la valeur entière du résultat de (x*2^8). La représentation du résultat en binaire donne une séquence de 8 bits (octet). Exemple : x=0,3 est codé comme suit : 0,3 * 2^8=76,8 , puis 76 en binaire est codé : 01001100.
  - Plus généralement, on peut utiliser un codage binaire sur n bits (pour plus de précision) : Dans ce cas pour un réel x, on code la partie entière de (x*2^n) sur une séquence de n bits.

2 - Fonction d'évaluation : dans ce cas il s'agit de f

3 - Croisement : Choix aléatoire d'individus à croiser (roulette russe) avec un taux de 25% à 75% de remplacement, et choix aléatoires des endroits ou le croisement doit s'effectuer.

4 - Mutation : Taux de mutation très faible (1%). Changer aléatoirement le bit d'un individu
