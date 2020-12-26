import random


# INPUT
# n : number of attack cycles belonging to R+
# q : relative hashrate belonging to [0;1]
# gamma : the ratio of honest miners that choose to mine on the pool’s block belonging to [0;1]
# bitcoinValue : coinbase belonging to R+
# bitcoinReward : no. of bitcoin for each block mined belonging to R+
class SelfishMining:

    # Initialisation
    def __init__(self, **inputVar):
        self.n = inputVar['numberCycles']
        self.q = inputVar['relativeHashrate']
        self.gamma = inputVar['gamma']

        self.honestChain = 0 # unit
        self.selfishChain = 0 # unit
        self.officialChain = 0 # unit
        self.orphanBlocks = 0 # unit
        self.delta = 0 # advance of selfish miners on honests'ones

        self.time = 0 # second    
        self.miningTime = 600 # seconds
        self.timeUpdate = 0 # second

        self.bitcoinValue = inputVar['bitcoinValue']
        self.bitcoinReward = inputVar['bitcoinReward']
        self.miningReward = self.bitcoinValue * self.bitcoinReward # dollars
        self.profitSelfishMining = 0 # dollar

    # Simulation 1 - Mining classic 
    def Simulation1(self):
        while(self.officialChain < self.n):

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
                self.officialChain += 1

    
    # Simulation 2 - SelfishMining Attack
    def Simulation2(self):
        while(self.selfishChain != 0 and self.officialChain <= self.n):
            r2 = random.uniform(0,1)

            # Update variables
            self.update()
            # If selfish miner solve the block in first
            if(r2 < self.q):
                self.selfishChain += 1
            else:
                self.honestChain +=1 

                # Difference between selfish and honest chain
                if(self.delta == 0):
                    if(r2 < self.q):
                        self.selfishChain += 1
                        self.officialChain += self.selfishChain
                        self.profitSelfishMining += self.miningReward * self.selfishChain
                        self.orphanBlocks += self.honestChain
                        self.selfishChain = self.honestChain = 0

                    else:
                        r3 = random.uniform(0,1)
                        # if the ratio of honest miners choose to mine on the pool’s block
                        if(r3 <= self.gamma):
                            self.selfishChain += 1
                            self.officialChain += self.selfishChain
                            self.profitSelfishMining += self.miningReward * self.selfishChain
                            self.orphanBlocks += self.honestChain
                            self.selfishChain = self.honestChain = 0
                        else:
                            self.officialChain += self.honestChain
                            self.selfishChain = self.honestChain = 0

                # Difference between selfish and honest chain
                elif(self.delta == 1):
                    self.officialChain += self.selfishChain
                    self.profitSelfishMining += self.miningReward * self.selfishChain
                    self.orphanBlocks += self.honestChain
                    self.selfishChain = self.honestChain = 0

                elif(self.delta == -1):
                    self.officialChain += self.honestChain
                    self.orphanBlocks += self.selfishChain
                    self.selfishChain = self.honestChain = 0


    def update(self):
        # Updating the difficulty
        if(self.officialChain % 2016 == 0 and self.officialChain != 0):
            self.miningTime = self.miningTime * ((2016 * 600) / self.timeUpdate)
            self.timeUpdate = 0

        # Updating time 
        self.time += self.miningTime
        self.timeUpdate += self.miningTime

        # Updating delta
        self.delta = self.selfishChain - self.honestChain

def timeConverter(n):
    if(n>=60):
        min=n//60
        sec=n%60
        if(min>=60):
            hour=min//60 
            min = min%60
            if(hour>=24):
                day=hour//24
                hour=hour%24
            else:
                day=0
        else:
            hour=0 
    else:
        min=0
        sec=n
    return sec, min, hour, day


n = int(input("numberCycle : "))
q = float(input("relativeHashrate : "))
gamma = float(input("gamma : "))
bitcoinValue = int(input("bitcoinValue : "))
bitcoinReward = int(input("bitcoinReward : "))
inputVariables = {'numberCycles':n, 'relativeHashrate':q, 'gamma':gamma,'bitcoinValue':bitcoinValue,'bitcoinReward':bitcoinReward}

#inputVariables = {'numberCycles':10, 'relativeHashrate':0.25, 'gamma':0.5,'bitcoinValue':10000,'bitcoinReward':6}

new = SelfishMining(**inputVariables)
new.Simulation1()
print('\nreward :', new.profitSelfishMining, end=' dollars\n')
time = timeConverter(new.time)
if(time[3] == 0): 
    print('time :', time[2],'hours', time[1],'minutes', time[0],'seconds')
elif(time[2] == 0): 
    print('time :', time[1],'minutes', time[0],'seconds')
elif(time[1] == 0): 
    print('time :', time[0],'seconds')
else:
    print('time :', time[3],'days', time[2],'hours', time[1],'minutes', time[0],'seconds')
print('orphanBlocks :', new.orphanBlocks, end=' units\n')
print('officialChain :', new.officialChain, end=' units\n\n')

