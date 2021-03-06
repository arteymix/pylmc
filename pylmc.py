#!/usr/bin/python3

class LMC(object):
    """
    Implementation du little men computer.
    """
    def __init__(self, registres, debug = False):
        """
        registres --- liste de tuplets (instruction, adresse)
        debug     --- enable or disable debug output
        """
        self.registres = registres
        self.debug = debug
        self.accumulateur = 0
        self.compteur = 0

    def ADD(self, adresse):
        instruction, valeur = self.registres[adresse]
        self.accumulateur += valeur

    def SUB(self, adresse):
        instruction, valeur = self.registres[adresse]
        self.accumulateur -= valeur

    def LDA(self, adresse):
        instruction, valeur = self.registres[adresse]
        self.accumulateur = valeur

    def STO(self, adresse):
        """
        Stocke le contenu de l'accumulateur dans un registre
        adresse --- adresse du registre
        """
        instruction, valeur = self.registres[adresse]
        self.registres[adresse] = (instruction, self.accumulateur)

    def IN(self, adresse):
        self.accumulateur = int(input('<<< '))

    def OUT(self, adresse):
        print('>>> ' + str(self.accumulateur))

    def HLT(self, adresse):
        exit()

    def BR(self, adresse):
        self.compteur = adresse

    def BRP(self, adresse):
        if self.accumulateur >= 0:
            self.BR(adresse)

    def BRZ(self, adresse):
        if self.accumulateur == 0:
            self.BR(adresse)
            
    def DAT(self, value):
        pass
            
    instructions = {
        'ADD': ADD,
        'SUB': SUB,
        'STO': STO,
        'LDA': LDA,
        'IN' : IN,
        'OUT': OUT,
        'HLT': HLT,
        'BR' : BR,
        'BRP': BRP,
        'BRZ': BRZ,
        'DAT': DAT
    }
            
    def run(self):
        """
        Execute le programme stocke dans les registres.
        """
        # Execution du programme
        while True:
            instruction, adresse = self.registres[self.compteur]
            if self.debug:
                print("{}: {} {}".format(self.compteur, instruction, adresse))
            self.compteur += 1
            self.instructions[instruction](self, adresse)

if __name__ == '__main__':

    import sys
     
    registres = []
   
    # Interpretation du programme
    with open(sys.argv[-1], 'r') as f:
            
        labels = {}

        for line in f:
            # On enleve les commentaires
            if '#' in line:
                line = line[0:line.find('#')]

            pieces = line.split()

            instruction, adresse, label = None, None, None
                
            # ligne vide
            if len(pieces) == 0:
                continue

            if len(pieces) == 1:  # Instruction seule
               instruction = pieces[0]

            if len(pieces) == 2:
                if pieces[0] in LMC.instructions: # instruction a gauche, adresse a droite
                    instruction, adresse = tuple(pieces)
                else: # instruction a droite, label a gauche
                    label, instruction = tuple(pieces)
                
            if len(pieces) == 3:
                label, instruction, adresse = tuple(pieces)              

            if len(pieces) > 3:
                raise RuntimeError("")

            # Tests
            if instruction not in LMC.instructions:
                raise RuntimeError("{} is not a valid instruction in line \n>>> {}".format(instruction, line))
             
            registres.append((instruction, adresse))

            if label is not None:
                labels[label] = len(registres) - 1

        # Traitements du programme
        for index, (instruction, adresse) in enumerate(registres):

            if adresse in labels:
                adresse = labels[adresse]
            
            if adresse is not None: # Happens with IN, OUT, DATA
                adresse = int(adresse)

            registres[index] = (instruction, adresse)

    LMC(registres, '--debug' in sys.argv).run()
