#List different kinds of block components
#Block connection types are needed for functions to use as arguments 

blockParts = {}

blockParts['print'] = {'connectionTypes':('string')}
blockParts['string'] = {'connectionTypes':()}
#connections are arguments
#by default key is block part name

blockspace = []

blockRefCount = 0

def addBlockToSpace(kind,x,y,data=[]):
	global blockspace
	global blockRefCount

	orig = blockParts[kind]
	ref = orig.copy()
	ref['command'] = kind
	ref['xy'] = x,y
	ref['id'] = blockRefCount
	ref['connections'] = []# list of found connections#####
	ref['data'] = data
	ref['width']=20
	ref['height']=20
	
	blockspace.append(ref)
	
	blockRefCount = blockRefCount + 1

#print (blockspace)

def findConnections(block):
	#TODO: 	find correct sequence for functions
	#		maybe with named areas
	x = block['xy'][0]
	y = block['xy'][1]
	
	width = block['width']
	height = block['height']
	
	highestX = x+width
	highestY = y+height
	
	foundConnections = []
	for block in blockspace:
		aBlockX = block['xy'][0]
		aBlockY = block['xy'][1]
		if aBlockX == highestX:
			if aBlockY == highestY:
				foundConnections.append(block['id'])
	
	return foundConnections
			
def runBlock(block):
	global blockspace
	
	resolvedAttribs = [] #start with no data, build up data
	block['connections']=findConnections(block) #what blocks are connected?
	
	#print ('connections',block['connections'])
	
	for blockConnection in block['connections']:
		resolvedAttribs.append(blockspace[blockConnection]['data'])
		
	#print ('resolvedAttribs',resolvedAttribs)
	
	resolvedAttribs = tuple(resolvedAttribs)
	
	if hasattr(__builtins__,block['command']):
		getattr(__builtins__,block['command'])(resolvedAttribs)


def runBlockspace():
	global blockspace
	runBlock(blockspace[0])

addBlockToSpace('print',100,100)
addBlockToSpace('string',120,120, 'test')

runBlockspace()
