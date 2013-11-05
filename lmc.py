class LMC(object):
    """
    Implementation du little men computer.
    """
    def __init__(self, registres):
        """
        registres --- liste de tuplets (instruction, registre)
        """
        self.registres = registres
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
        self.registres[adresse] = ('DAT', self.accumulateur)

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
            # print('compteur: {}, accumulateur: {}, registres: {}'.format(self.compteur, self.accumulateur, self.registres))
            instruction, adresse = self.registres[self.compteur]
            self.compteur += 1
            self.instructions[instruction](self, adresse)

if __name__ == '__main__':

    import sys
     
    registres = []
   
    # Interpretation du programme
    with open(sys.argv[1], 'r') as f:
            
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
                if LMC.instructions.has_key(pieces[0]): # instruction a gauche, adresse a droite
                    instruction, adresse = tuple(pieces)
                else: # instruction a droite, label a gauche
                    label, instruction = tuple(pieces)
                
            if len(pieces) == 3:
                label, instruction, adresse = tuple(pieces)              

            if len(pieces) > 3:
                raise RuntimeError("")

            # Tests
            if not LMC.instructions.has_key(instruction):
                raise RuntimeError("{} is not a valid instruction in line \n>>> {}".format(instruction, line))
             
            registres.append((instruction, adresse))

            if label is not None:
                labels[label] = len(registres) - 1

        # Traitements des labels
        for index, (instruction, adresse) in enumerate(registres):
            if labels.has_key(adresse):
                registres[index] = (instruction, int(labels[adresse]))
            elif adresse is not None:
                registres[index] = (instruction, int(adresse))

    LMC(registres).run()
