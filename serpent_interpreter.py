# *******************************************************
# Nom ......... : serpent_interpreter.y
# Auteur ...... : Yanis Nebbaki (approfondissement, code de base HowCode)
# Version ..... : V1 pour le projet
# Licence ..... : L3 - I&C
# Exercice : PROJET
# Compilation : python3 serpent_interpreter.py
#********************************************************

from sly import Lexer
from sly import Parser
import math
import os

class BasicLexer(Lexer):
    tokens = { NAME, STRING, SI, FAIRE, SINON, POUR, FONC, JSQ, ARROW, EQEQ, ECRIS, EXEMPLE, RAPPEL, SOH, OSH, HOS, SIN, ASIN, CAH, ACH, HAC, COS, ACOS, TOA, OTA, AOT, TAN, ATAN, NOMBRE_FLOTTANT, EFFACER }
    ignore = '\t '  # ignore les tabulations et les espaces

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';' }

    # Define tokens
    #S : sinus
    #O : opposé
    #H : hypoténuse
    #C : cosinus
    #T : tangente
    #SIN : sinus ASIN : arcsinus | COS : cosinus ACOS : arcsinus | TAN : tangente ATAN : arctangente
    # Token pour les calculs avec le sinus, 1ère lettre => ce qu'on veut calculer, 2è et 3è lettre les opérandes
    SOH = r'SOH'
    OSH = r'OSH'
    HOS = r'HOS'
    SIN = r'SIN'     # SIN se trouve au dessus du token SI pour éviter les conflits
    ASIN = r'ASIN'
    # Token pour les calculs avec le cosinus, 1ère lettre => ce qu'on veut calculer, 2è et 3è lettre les opérandes
    CAH = r'CAH'
    ACH= r'ACH'
    HAC = r'HAC'
    COS = r'COS'     
    ACOS = r'ACOS'
    # Token pour les calculs avec la tangente, 1ère lettre => ce qu'on veut calculer, 2è et 3è lettre les opérandes
    TOA = r'TOA'
    OTA = r'OTA'
    AOT = r'AOT'
    TAN = r'TAN'
    ATAN = r'ATAN'
    #TOKEN GENERAUX
    FAIRE = r'FAIRE' # THEN
    SINON = r'SINON' # ELSE
    POUR = r'POUR'   # FOR
    FONC = r'FONC'   # FUNCTION
    JSQ= r'JSQ'      # TO
    SI = r'SI'       # IF
    ARROW = r'->'
    EFFACER = r'EFFACER'
    EXEMPLE = r'EXEMPLE' # Exemple triangle rectangle
    RAPPEL = r'RAPPEL'   # Relations trigonométriques
    ECRIS = r'ECRIS'     # TOKEN ECRIS
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'

    EQEQ = r'=='
    
    @_(r'(0|[1-9]\d*)(\.\d+)?')   # Regex des nombres entiers ou flottants, positifs
    def NOMBRE_FLOTTANT(self, t): # Nouvelle règle pour la gestion des nombres flottants
        t.value = float(t.value)  # Conversion en float
        return t

    @_(r'#.*')                  # ligne commençant par # traitée comme des commentaires
    def COMMENT(self, t):
        pass   

    @_(r'\n+')                  # gestion des lignes
    def newline(self,t ):
        self.lineno = t.value.count('\n')

class BasicParser(Parser):
    tokens = BasicLexer.tokens

    precedence = (              # priorité et associativté des opérateurs
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.env = { }

    @_('')
    def statement(self, p):
        pass
    # CALCULS AVEC LE SINUS #
    @_('SOH NOMBRE_FLOTTANT NOMBRE_FLOTTANT')                       # Pour obtenir le SINUS à partir des côtés              
    def statement(self, p):
        return('soh_cmd', p.NOMBRE_FLOTTANT0, p.NOMBRE_FLOTTANT1)      
    
    @_('OSH NOMBRE_FLOTTANT NOMBRE_FLOTTANT')                       # Pour obtenir le côté OPPOSE        
    def statement(self, p):
        return('osh_cmd', p.NOMBRE_FLOTTANT0, p.NOMBRE_FLOTTANT1)
    
    @_('HOS NOMBRE_FLOTTANT NOMBRE_FLOTTANT')                       # Pour obtenir l'HYPOTENUSE       
    def statement(self, p):
        return('hos_cmd', p.NOMBRE_FLOTTANT0, p.NOMBRE_FLOTTANT1)
    
    @_('SIN NOMBRE_FLOTTANT')                                       # Pour obtenir le SINUS à partir de l'angle   
    def statement(self, p):
        return('sin_cmd', p.NOMBRE_FLOTTANT)
    
    @_('ASIN NOMBRE_FLOTTANT')                                     # Pour obtenir l'ANGLE à partir du sinus (sin-1 ou arc sinus)                           
    def statement(self, p):
        return('asin_cmd', p.NOMBRE_FLOTTANT)
    
    # CALCULS AVEC LE COSINUS #
    @_('CAH NOMBRE_FLOTTANT NOMBRE_FLOTTANT')                       # Pour obtenir le COSINUS à partir des côtés              
    def statement(self, p):
        return('cah_cmd', p.NOMBRE_FLOTTANT0, p.NOMBRE_FLOTTANT1)      
    
    @_('ACH NOMBRE_FLOTTANT NOMBRE_FLOTTANT')                       # Pour obtenir le côté ADJACENT       
    def statement(self, p):
        return('ach_cmd', p.NOMBRE_FLOTTANT0, p.NOMBRE_FLOTTANT1)
    
    @_('HAC NOMBRE_FLOTTANT NOMBRE_FLOTTANT')                       # Pour obtenir l'HYPOTENUSE       
    def statement(self, p):
        return('hac_cmd', p.NOMBRE_FLOTTANT0, p.NOMBRE_FLOTTANT1)
    
    @_('COS NOMBRE_FLOTTANT')                                       # Pour obtenir le COSINUS à partir de l'angle   
    def statement(self, p):
        return('cos_cmd', p.NOMBRE_FLOTTANT)
    
    @_('ACOS NOMBRE_FLOTTANT')                                     # Pour obtenir l'ANGLE à partir du cosinus (cos-1 ou arc cosinus)                           
    def statement(self, p):
        return('acos_cmd', p.NOMBRE_FLOTTANT)
    
    # CALCULS AVEC LE COSINUS #
    @_('TOA NOMBRE_FLOTTANT NOMBRE_FLOTTANT')                       # Pour obtenir la TANGENTE à partir des côtés              
    def statement(self, p):
        return('toa_cmd', p.NOMBRE_FLOTTANT0, p.NOMBRE_FLOTTANT1)      
    
    @_('OTA NOMBRE_FLOTTANT NOMBRE_FLOTTANT')                       # Pour obtenir le côté OPPOSE      
    def statement(self, p):
        return('ota_cmd', p.NOMBRE_FLOTTANT0, p.NOMBRE_FLOTTANT1)
    
    @_('AOT NOMBRE_FLOTTANT NOMBRE_FLOTTANT')                       # Pour obtenir le côté ADJACENT    
    def statement(self, p):
        return('aot_cmd', p.NOMBRE_FLOTTANT0, p.NOMBRE_FLOTTANT1)
    
    @_('TAN NOMBRE_FLOTTANT')                                       # Pour obtenir la TANGENTE à partir de l'angle   
    def statement(self, p):
        return('tan_cmd', p.NOMBRE_FLOTTANT)
    
    @_('ATAN NOMBRE_FLOTTANT')                                     # Pour obtenir l'ANGLE à partir de la tangente (arc tangente)                           
    def statement(self, p):
        return('atan_cmd', p.NOMBRE_FLOTTANT)
    
    # Exemple triangle rectangle
    @_('EXEMPLE')                            
    def statement(self, p):
        return('exemple_cmd', p)
    
    #Rappel Relations Trigonométriques
    @_('RAPPEL')                            
    def statement(self, p):
        return('rappel_cmd', p)
    
    @_('EFFACER')                                       # Pour clear la console
    def statement(self, p):
        return('effacer_cmd', p)
    
    @_('ECRIS STRING')                                  # print associé au token ECRIS
    def statement(self, p):
        return('ecris_cmd', p.STRING)
    
    @_('POUR var_assign JSQ expr FAIRE statement')      # boucle for
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

    @_('SI condition FAIRE statement SINON statement')  # test si
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    @_('FONC NAME "(" ")" ARROW statement')             # fonction
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement)

    @_('NAME "(" ")"')                                  # nom de la fonction et appel
    def statement(self, p):
        return ('fun_call', p.NAME)

    @_('expr EQEQ expr')                                # gestion du test d'égalité ==
    def condition(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)

    @_('var_assign')                                    # assignement de variable
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr')                                 # assignement de variable si il s'agit d'une expression (nombre ou opération)
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('NAME "=" STRING')                               # assignement de variable si il s'agit d'une chaîne de caractères
    def var_assign(self, p):    
        return ('var_assign', p.NAME, p.STRING)

    @_('expr')                                          # définition d'une expression
    def statement(self, p):
        return (p.expr)

    @_('expr "+" expr')                                 # addition
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')                                 # soustraction
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')                                 # multiplication
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')                                 # division
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')                         # opérateur unaire -
    def expr(self, p):
        return p.expr[0], -p.expr[1]

    @_('NAME')                                          # nom de variable
    def expr(self, p):
        return ('var', p.NAME)

    @_('NOMBRE_FLOTTANT')                               # nombre
    def expr(self, p):
        return ('num', p.NOMBRE_FLOTTANT)



class BasicExecute:


    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and (isinstance(result, float) or isinstance(result, int)): # ajout de la détection du type foat
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):
        dernier_sinus = "dernier_sinus"
        dernier_cosinus = "dernier_cosinus"
        derniere_tangente = 'derniere_tangente'
        dernier_oppose = 'dernier_oppose'
        dernier_adjacent = 'dernier_adjacent'
        dernier_hypotenuse = 'dernier_hypotenuse'
        dernier_angle = 'dernier_angle'

        if isinstance(node, int) or isinstance(node, float): # ajout du type float
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':            # si le 1er noeud est de type program alors
            if node[1] == None:             # cela indique qu'il s'agit d'un programme
                self.walkTree(node[2])      # contenant plusieurs instructions
            else:                           # la méthode walkTree est appelée récursivement
                self.walkTree(node[1])      # pour chaque instruction
                self.walkTree(node[2])

        if node[0] == 'num':                # si le noeud est un nombre, la valeur est renvoyée
            return node[1]

        if node[0] == 'str':                # si le noeud est un string, la valeur est renvoyée
            return node[1]

        if node[0] == 'if_stmt':            # si le noeud est un test conditionnel, l'expression
            result = self.walkTree(node[1]) # conditionnelle est évaluée, si elle est vraie
            if result:
                return self.walkTree(node[2][1]) # la 1ere branche est exécutée
            return self.walkTree(node[2][2])     # sinon la 2eme est exécutée

        if node[0] == 'condition_eqeq':          # noeud ==
            return self.walkTree(node[1]) == self.walkTree(node[2]) # comparaison des deux expressions de chaque côté du ==

        if node[0] == 'fun_def':            # noeud de définition d'une fonction, la fonction est ajoutée à l'envrionnement et son nom comme clée
            self.env[node[1]] = node[2]

        if node[0] == 'fun_call':           # appel de fonction
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Undefined function '%s'" % node[1])
                return None

        if node[0] == 'add':                                            # noeuds des opérations mathématiques + - * /
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == 'var_assign':                    # noeud d'affectation de variable
            if (node[1] == dernier_sinus or            # ajout d'une condition pour réserver les variable servant à stocker les résultats des calculs SOHCAHTOA etc...
            node[1] == dernier_cosinus or 
            node[1] == derniere_tangente or 
            node[1] == dernier_adjacent or 
            node[1] == dernier_oppose or 
            node[1] == dernier_hypotenuse or 
            node[1] == dernier_angle):
                print("!!! Variable réservée pour stocker les résultats des calculs, veuillez en utiliser une autre !!!")
                return None
            else:
                self.env[node[1]] = self.walkTree(node[2]) # la valeur est évaluée et assignée à la variable correspondante dans l'envrionnement
                return node[1]

        if node[0] == 'ecris_cmd':
            return self.walkTree(node[1])
        
        if node[0] == 'effacer_cmd':
            os.system('clear')
            return None

        
        # Calcul avec le SINUS
        if node[0] == 'soh_cmd':                    # Calcul Sinus = opposé / hypoténuse
            oppose = self.walkTree(node[1])         # Premier nombre flottant stocké
            hypotenuse = self.walkTree(node[2])     # Second nombre flottant stocké
            if hypotenuse <= oppose:
                print(f"!!! Valeur de l'hypoténuse ({hypotenuse}) inférieure/égale à celle du côté ({oppose}) !!!") # Gestion de l'erreur où hypoténuse < côté
                return None
            sinus_x = round((oppose / hypotenuse), 3) # Arrondi au millième
            if 0 < sinus_x < 1:
                self.env[dernier_sinus] = sinus_x    # Stockage de la valeur pour la consulter plus tard
                return sinus_x
            print(f"!!! Valeur du sinus ({sinus_x}) non comprise entre 0 et 1 !!!") # Si le résultat n'est pas compris entre 0 et 1, on renvoie la valeur obtenue et un message d'erreur
            return None
        
        if node[0] == 'osh_cmd':                    # Calcul Opposé = sinus * hypoténuse
            sinus = self.walkTree(node[1])
            hypotenuse = self.walkTree(node[2])
            if (0 >= sinus) or (1 <= sinus):
                print(f"!!! Valeur du sinus ({sinus}) non comprise entre 0 et 1 !!!") # Gestion de l'erreur où sinus n'est pas compris strictement entre 0 et 1
                return None
            oppose = round((sinus * hypotenuse), 3) # Arrondi au millième
            if oppose >= hypotenuse:
                print(f"!!! Valeur de l'hypoténuse ({hypotenuse}) inférieure/égale à celle du côté ({oppose}) !!!") # Gestion de l'erreur où hypoténuse < côté
                return None
            self.env[dernier_oppose] = oppose       # Stockage de la valeur pour la consulter plus tard
            return oppose
        
        if node[0] == 'hos_cmd':                    # Calcul Hyppoténuse = oppose / sinus
            oppose = self.walkTree(node[1])
            sinus = self.walkTree(node[2])
            if (0 >= sinus) or (1 <= sinus):
                print(f"!!! Valeur du sinus ({sinus}) non comprise entre 0 et 1 !!!") # Gestion de l'erreur où sinus n'est pas compris strictement entre 0 et 1
                return None
            hypotenuse = round((oppose / sinus), 3) # Arrondi au millième
            if hypotenuse <= oppose:
                print(f"!!! Valeur de l'hypoténuse ({hypotenuse}) inférieure/égale à celle du côté ({oppose}) !!!") # Gestion de l'erreur où hypoténuse < côté
                return None
            self.env[dernier_hypotenuse] = hypotenuse   # Stockage de la valeur pour la consulter plus tard
            return hypotenuse
        
        if node[0] == 'sin_cmd':                   # Calcul Sinus à partir de l'angle
            angle = self.walkTree(node[1])
            if (0 >= angle) or (angle>= 90):       # Gestion de l'erreur si l'angle n'est pas aigu
                print(f"!!! Angle ({angle}) non aigu !!!")
                return None
            sinus_x = round((math.sin(math.radians(angle))), 3) # Conversion en radians puis calcul du sinus, on arrondit le résultat
            self.env[dernier_sinus] = sinus_x      # Stockage de la valeur pour la consulter plus tard
            return sinus_x 
        
        if node[0] == 'asin_cmd':                 # Calcul de l'angle à partir du sinus
            sinus = self.walkTree(node[1])
            if (0 >= sinus) or (sinus>= 1):       # Gestion de l'erreur si le sinus n'est pas compris entre 0 et 1
                print(f"!!! Sinus ({sinus}) non compris entre 0 et 1 !!!")
                return None
            angle = math.degrees(math.asin(sinus))  # Conversion du résultat de arc sin qui est en radians en degrés
            angle = round(angle, 3) # Arrondi
            self.env[dernier_angle] = angle          # Stockage de la valeur pour la consulter plus tard
            return angle 

        # FIN Calcul avec le SINUS

        # Calcul avec le COSINUS
        if node[0] == 'cah_cmd':                    # Calcul Cosinus = adjacent / hypoténuse
            adjacent = self.walkTree(node[1])
            hypotenuse = self.walkTree(node[2])
            if hypotenuse <= adjacent:
                print(f"!!! Valeur de l'hypoténuse ({hypotenuse}) inférieure/égale à celle du côté ({adjacent}) !!!") # Gestion de l'erreur où hypoténuse < côté
                return None
            cosinus_x = round((adjacent / hypotenuse), 3)
            if 0 < cosinus_x < 1:
                self.env[dernier_cosinus] = cosinus_x       # Stockage de la valeur pour la consulter plus tard
                return cosinus_x
            print(f"!!! Valeur du cosinus ({cosinus_x}) non comprise entre 0 et 1 !!!") # Gestion de l'erreur où cosinus n'est pas compris strictement entre 0 et 1
            return None
        
        if node[0] == 'ach_cmd':                    # Calcul Adjacent = cosinus * hypoténuse
            cosinus = self.walkTree(node[1])
            hypotenuse = self.walkTree(node[2])
            if (0 >= cosinus) or (1 <= cosinus):
                print(f"!!! Valeur du cosinus ({cosinus}) non comprise entre 0 et 1 !!!") # Gestion de l'erreur où cosinus n'est pas compris strictement entre 0 et 1
                return None
            adjacent = round((cosinus * hypotenuse), 3)
            if adjacent >= hypotenuse:
                print(f"!!! Valeur de l'hypoténuse ({hypotenuse}) inférieure à celle du côté ({adjacent}) !!!") # Gestion de l'erreur où hypoténuse < côté
                return None
            self.env[dernier_adjacent] = adjacent   # Stockage de la valeur pour la consulter plus tard
            return adjacent
        
        if node[0] == 'hac_cmd':                    # Calcul Hyppoténuse = adjacent / cosinus
            adjacent = self.walkTree(node[1])
            cosinus = self.walkTree(node[2])
            if (0 >= cosinus) or (1 <= cosinus):
                print(f"!!! Valeur du cosinus ({cosinus}) non comprise entre 0 et 1 !!!") # Gestion de l'erreur où cosinus n'est pas compris strictement entre 0 et 1
                return None
            hypotenuse = round((adjacent / cosinus), 3)
            if hypotenuse <= adjacent:
                print(f"!!! Valeur de l'hypoténuse ({hypotenuse}) inférieure/égale à celle du côté ({adjacent}) !!!") # Gestion de l'erreur où hypoténuse < côté
                return None
            self.env[dernier_hypotenuse] = hypotenuse   # Stockage de la valeur pour la consulter plus tard
            return hypotenuse
        
        if node[0] == 'cos_cmd':                      # Calcul Cosinus à partir de l'angle
            angle = self.walkTree(node[1])
            if (0 >= angle) or (angle >= 90):            # Gestion de l'erreur si l'angle n'est pas aigu
                print(f"!!! Angle ({angle}) non aigu !!!")
                return None
            cosinus_x = round(math.cos(math.radians(angle)), 3) # Conversion en radians puis calcul du cosinus
            self.env[dernier_cosinus] = cosinus_x
            return cosinus_x       
        
        if node[0] == 'acos_cmd':                     # Calcul de l'angle à partir du cosinus
            cosinus = self.walkTree(node[1])
            if (0 >= cosinus) or (cosinus >= 1):         # Gestion de l'erreur si l'angle n'est pas aigu
                print(f"!!! Cosinus ({cosinus}) non compris entre 0 et 1 !!!")
                return None
            angle = math.degrees(math.acos(cosinus))  # Conversion en degrés
            angle = round(angle, 3)
            self.env[dernier_angle] = angle
            return angle

        # FIN Calcul avec le COSINUS

        # Calcul avec la TANGENTE

        if node[0] == 'toa_cmd':                      # Calcul Tangente = oppose / adjacent
            oppose = self.walkTree(node[1])
            adjacent = self.walkTree(node[2])
            tangente_x = round((oppose / adjacent), 3)
            self.env[derniere_tangente] = tangente_x
            return tangente_x
        
        if node[0] == 'ota_cmd':                      # Calcul Oppose = tangente * adjacent
            tangente = self.walkTree(node[1])
            adjacent = self.walkTree(node[2])
            oppose = round((tangente * adjacent), 3)
            self.env[dernier_oppose] = oppose
            return oppose
        
        if node[0] == 'aot_cmd':                      # Calcul Adjacent = oppose / adjacent
            oppose = self.walkTree(node[1])
            tangente = self.walkTree(node[2])
            adjacent = round((oppose / tangente), 3)
            self.env[dernier_adjacent] = adjacent
            return adjacent
        
        if node[0] == 'tan_cmd':                      # Calcul Tangente à partir de l'angle
            angle = self.walkTree(node[1])
            if (0 >= angle) or (angle >= 90):            # Gestion de l'erreur si l'angle n'est pas aigu
                print(f"!!! Angle ({angle}) non aigu !!!")
                return None
            tangente_x = round((math.tan(math.radians(angle))), 3) # Conversion en radians puis calcul de la tangente
            self.env[derniere_tangente] = tangente_x
            return tangente_x    
        
        if node[0] == 'atan_cmd':                    # Calcul de l'angle à partir de la tangente
            tangente = self.walkTree(node[1])
            angle = math.degrees(math.atan(tangente))  # Conversion en degrés
            angle = round(angle, 3)           
            self.env[dernier_angle] = angle
            return angle

        # FIN Calcul avec la TANGENTE
            
        #Exemple triangle rectangle
        if node[0] == 'exemple_cmd':
            print("\n  A\n  x\n  xx\n  xxx\n  xxxx\nB xxxxx C\n\nTriangle ABC, rectangle en B.\n\n")

            print("              opposé à Â soit BC")
            print("sinus Â    = --------------------")    
            print("              hypoténuse soit AC\n")

            print("              adjacent à Â soit AB")
            print("cosinus Â  = ----------------------")    
            print("               hypoténuse soit AC\n")

            print("               opposé à Â soit BC")
            print("tangente Â = ----------------------")    
            print("              adjacent à Â soit AB\n")
            return None
        
        #Rappel des relations trigonométriques
        if node[0] == 'rappel_cmd':
            print("\n1 - Nous travaillons sur des angles aigus : 0° < angle < 90°.\n\n2 - Moyen mnémotechnique : SOH CAH TOA.\n")
            print("                      Opposé")
            print("    SOH Sinus    = ------------")    
            print("                    Hypoténuse\n")

            print("                     Adjacent")
            print("    CAH Cosinus  = ------------")    
            print("                    Hypoténuse\n")

            print("                     Opposé")
            print("    TOA Tangente = ----------")    
            print("                    Adjacent\n")
            print("3 - Si un résultat vous semble étrange, rappelez vous que :\n    l'hypoténuse est plus grand que chaque côté\n    0 < cos x < 1\n    0 < sin x < 1\n    cos² x + sin² x = 1\n")
            return None


        if node[0] == 'var':                # noeud faisant référence à une variable, sa valeur est renvoyée à partir de l'environnement
            try:
                return self.env[node[1]]
            except LookupError:
                print("Variable '"+node[1]+"' non définie !")
                return None

        if node[0] == 'for_loop':           # noeud d'une boucle POUR / FOR
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = int(self.env[loop_setup[0]])

                loop_limit = int(loop_setup[1])

                for i in range(loop_count+1, loop_limit+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':     # noeud de la configuration d'une boucle POUR / FOR, valeurs initiales et limites sont renvoyées
            return (self.walkTree(node[1]), self.walkTree(node[2]))

#def calcul_automatique(adjacent, oppose, hypotenuse, sinus, cosinus, tangente, angle_A, angle_B) POTENTIEL AMELIORATION
    
if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}
    while True:
        try:
            text = input('serpent > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            BasicExecute(tree, env)


    