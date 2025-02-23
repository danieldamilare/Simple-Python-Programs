import random
import matplotlib.pyplot as plt
import numpy as np

# Set plotting parameters
plt.rcParams['lines.linewidth'] = 4
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['xtick.major.size'] = 7
plt.rcParams['ytick.major.size'] = 7
plt.rcParams['legend.numpoints'] = 1

class Location:
    def __init__(self, x, y):
        """Initialize location with x and y coordinates"""
        self.x = float(x)
        self.y = float(y)

    def move(self, deltaX, deltaY):
        """Return new Location moved by deltaX and deltaY"""
        return Location(self.x + deltaX, self.y + deltaY)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distFrom(self, other):
        """Calculate Euclidean distance from another location"""
        return ((self.x - other.getX())**2 + (self.y - other.getY())**2)**0.5

    def __str__(self):
        return f'<{self.x}, {self.y}>'

class Field:
    def __init__(self):
        """Initialize empty field"""
        self.drunks = {}
        
    def addDrunk(self, drunk, loc):
        """Add drunk to field at specified location"""
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        self.drunks[drunk] = loc
            
    def moveDrunk(self, drunk):
        """Move drunk according to its step behavior"""
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        self.drunks[drunk] = self.drunks[drunk].move(xDist, yDist)
        
    def getLoc(self, drunk):
        """Get current location of drunk"""
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]

class Drunk:
    def __init__(self, name=None):
        """Initialize drunk with optional name"""
        self.name = name if name is not None else 'Anonymous'

    def __str__(self):
        return self.name

class UsualDrunk(Drunk):
    def takeStep(self):
        """Take a random step in one of four directions"""
        stepChoices = [(0,1), (0,-1), (1,0), (-1,0)]
        return random.choice(stepChoices)

class MasochistDrunk(Drunk):
    def takeStep(self):
        """Take a random step with slightly biased distances"""
        stepChoices = [(0.0,1.1), (0.0,-0.9), (1.0,0.0), (-1.0,0.0)]
        return random.choice(stepChoices)

class OddField(Field):
    def __init__(self, numHoles=1000, xRange=100, yRange=100):
        """Initialize field with random wormholes"""
        super().__init__()
        self.wormholes = {}
        for _ in range(numHoles):
            x = random.randint(-xRange, xRange)
            y = random.randint(-yRange, yRange)
            newX = random.randint(-xRange, xRange)
            newY = random.randint(-yRange, yRange)
            self.wormholes[(x, y)] = Location(newX, newY)

    def moveDrunk(self, drunk):
        """Move drunk and check for wormholes"""
        super().moveDrunk(drunk)
        x = self.drunks[drunk].getX()
        y = self.drunks[drunk].getY()
        if (x, y) in self.wormholes:
            self.drunks[drunk] = self.wormholes[(x, y)]

class StyleIterator:
    def __init__(self, styles):
        """Initialize with list of plot styles"""
        self.index = 0
        self.styles = styles

    def nextStyle(self):
        """Return next style in rotation"""
        result = self.styles[self.index]
        self.index = (self.index + 1) % len(self.styles)
        return result

def walk(field, drunk, numSteps):
    """Simulate a walk and return final distance from start"""
    start = field.getLoc(drunk)
    for _ in range(numSteps):
        field.moveDrunk(drunk)
    return start.distFrom(field.getLoc(drunk))

def simWalks(numSteps, numTrials, drunkClass):
    """Simulate multiple walks and return distances"""
    drunk = drunkClass('Homer')
    origin = Location(0, 0)
    distances = []
    
    for _ in range(numTrials):
        field = Field()
        field.addDrunk(drunk, origin)
        distances.append(round(walk(field, drunk, numSteps), 1))
    return distances

def plotDrunkCompare(drunkKinds, walkLengths, numTrials):
    """Compare different types of drunks with visualization"""
    styleChoice = StyleIterator(('m-', 'b--', 'g-.'))
    plt.figure(figsize=(10, 8))
    
    for drunkClass in drunkKinds:
        means = []
        for numSteps in walkLengths:
            trials = simWalks(numSteps, numTrials, drunkClass)
            means.append(sum(trials)/len(trials))
            
        curStyle = styleChoice.nextStyle()
        plt.plot(walkLengths, means, curStyle, label=drunkClass.__name__)
    
    plt.title(f'Mean Distance from Origin ({numTrials} trials)')
    plt.xlabel('Number of Steps')
    plt.ylabel('Distance from Origin')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

def plotFinalLocations(drunkKinds, numSteps, numTrials):
    """Plot final locations of different types of drunks"""
    styleChoice = StyleIterator(('k+', 'r^', 'mo'))
    plt.figure(figsize=(10, 10))
    
    for drunkClass in drunkKinds:
        drunk = drunkClass()
        locations = []
        
        for _ in range(numTrials):
            field = OddField()
            field.addDrunk(drunk, Location(0, 0))
            for _ in range(numSteps):
                field.moveDrunk(drunk)
            locations.append(field.getLoc(drunk))
        
        xVals = [loc.getX() for loc in locations]
        yVals = [loc.getY() for loc in locations]
        meanX = sum(abs(x) for x in xVals) / len(xVals)
        meanY = sum(abs(y) for y in yVals) / len(yVals)
        
        curStyle = styleChoice.nextStyle()
        plt.plot(xVals, yVals, curStyle,
                label=f'{drunkClass.__name__}\nmean abs dist = <{meanX:.1f}, {meanY:.1f}>')
    
    plt.title(f'Location at End of Walks ({numSteps} steps)')
    plt.xlim(-1000, 1000)
    plt.ylim(-1000, 1000)
    plt.xlabel('Steps East/West of Origin')
    plt.ylabel('Steps North/South of Origin')
    plt.legend(loc='lower center')
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == '__main__':
    random.seed(0)  # For reproducibility
    
    # Compare different types of drunks
    walkLengths = [10, 100, 1000, 10000]
    plotDrunkCompare((UsualDrunk, MasochistDrunk), walkLengths, 100)
    
    # Plot final locations
    plotFinalLocations((UsualDrunk, MasochistDrunk), 10000, 1000)