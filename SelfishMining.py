import random


# INPUT
# n : number of attack cycles belonging to R+
# q : relative hashrate belonging to [0;1]
# gamma : the ratio of honest miners that choose to mine on the pool’s block belonging to [0;1]
# alpha : the selfish pool mining power belonging to [0;0.5]
# bitcoinValue : coinbase belonging to R+
# bitcoinReward : no. of bitcoin for each block mined belonging to R+
class SelfishMining:

    # Initialisation
    def init(self, **inputVar):
        self.n = inputVar['numberCycles']
        self.q = inputVar['relativeHashrate']
        self.gamma = inputVar['gamma']
        self.alpha = inputVar['alpha']

        self.honestChain = 0 # unit
        self.selfishChain = 0 # unit
        self.officialChain = 0 # unit
        self.oprhanBlocks = 0 # unit
        self.delta = 0 # advance of selfish miners on honests'ones

        self.counter = 1 # unit
        self.time = 0 # second    
        self.miningTime = 600 # seconds
        self.timeUpdate = 0 # second

        self.bitcoinValue = inputVar['bitcoinValue']
        self.bitcoinReward = inputVar['bitcoinReward']
        self.miningReward = self.bitcoinValue * self.bitcoinReward # dollars
        self.profitSelfishMining = 0 # dollar

    # Simulation 1 - Mining classic 
    def Simulation1(self):
        while(self.counter <= self.n):
            r1 = random.uniform(0,1)
            
            # Update variables
            self.update()

            # If selfish miner solve the block
            if(r1 < self.q):
                self.selfishChain += 1

                # Beginning of the attack
                self.Simulation2()

            # If honest miner solve the block in first
            else:
                self.officialChain += self.honestChain
                self.selfishChain = self.honestChain = 0
                self.counter += 1

    
    # Simulation 2 - SelfishMining Attack
    def Simulation2(self):
        r2 = random.uniform(0,1)
            
        # Update variables
        self.update()

        # If selfish miner solve the block in first
        if(r2 < self.q):
            self.selfishChain += 1
        else:
            # Difference between selfish and honest chain
            if(self.delta == 0):
                if(r2 < self.q):
                    self.selfishChain += 1
                    self.officialChain += self.selfishChain
                    self.profitSelfishMining += self.miningReward * self.selfishChain
                    self.oprhanBlocks += self.honestChain
                    self.counter += self.selfishChain
                    self.selfishChain = self.honestChain = 0

                else:
                    r3 = random.uniform(0,1)
                    if(r3 <= self.gamma):
                        self.selfishChain += 1
                        self.officialChain += self.selfishChain
                        self.profitSelfishMining += self.miningReward * self.selfishChain
                        self.oprhanBlocks += self.honestChain
                        self.counter += self.selfishChain
                        self.selfishChain = self.honestChain = 0
                    else:
                        self.officialChain += self.honestChain
                        self.counter += self.honestChain
                        self.selfishChain = self.honestChain = 0

            # Difference between selfish and honest chain
            elif(self.delta == 1):
                self.officialChain += self.selfishChain
                self.profitSelfishMining += self.miningReward * self.selfishChain
                self.oprhanBlocks += self.honestChain
                self.counter += self.selfishChain
                self.selfishChain = self.honestChain = 0

            elif(self.delta == -1):
                self.officialChain += self.honestChain
                self.counter += self.honestChain
                self.oprhanBlocks += self.selfishChain
                self.selfishChain = self.honestChain = 0

    def update(self):
        # Updating the difficulty
        if(self.counter % 2016 == 0):
            self.miningTime = self.miningTime * ((2016 * 600) / self.timeUpdate)
            self.timeUpdate = 0

        # Updating time 
        self.time += self.miningTime
        self.timeUpdate += self.miningTime

        # Updating delta
        self.delta = self.selfishChain - self.honestChain

