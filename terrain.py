from ursina import *
from mining_system import *
from building_system import *

class MeshTerrain:
    def __init__(this, landscale):

        this.landscale = landscale
        this.block = load_model('assets/block.obj')
        this.textureAtlas = 'assets/texture_atlas.png'
        this.numVertices = len(this.block.vertices)

        this.subsets = []
        this.numSubsets = 512

        this.subWidth = len(this.landscale)
        this.currentSubset = 0

        # Our terrain dictionary :D
        this.td = {}

        # Our vertex dictionary -- for mining.
        this.vd = {}

        for i in range(0,this.numSubsets):
            e = Entity( model=Mesh(),
                        texture=this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)
        
    # Highlight looked-at block :)
    def update(this,pos,cam):
        highlight(pos,cam,this.td)
    
    def input(this,key):
        if key=='left mouse up' and bte.visible==True:
            epi = mine(this.td,this.vd,this.subsets)
            if epi != None:
                this.genWalls(epi[0],epi[1])
                this.subsets[epi[1]].model.generate()
        # ***
        if bte.visible==True:
            bsite = checkBuild(key,bte.position,this.td)
            if bsite!= None:
                this.genBlock(floor(bsite.x),floor(bsite.y),floor(bsite.z),subset=0)
                gapShell(this.td,bsite)
                this.subsets[0].model.generate()
    
    # I.e. after mining, to create illusion of depth.
    def genWalls(this,epi,subset):
        if epi==None: return
        # Refactor this -- place in mining_system 
        # except for call to genBlock?
        wp =    [   Vec3(0,1,0),
                    Vec3(0,-1,0),
                    Vec3(-1,0,0),
                    Vec3(1,0,0),
                    Vec3(0,0,-1),
                    Vec3(0,0,1)]
        for i in range(0,6):
            np = epi + wp[i]
            if this.td.get( (floor(np.x),
                            floor(np.y),
                            floor(np.z)))==None:
                this.genBlock(np.x,np.y,np.z,subset,gap=False)

    def genBlock(this,x,y,z,subset=-1,gap=True):
        if subset==-1: subset=this.currentSubset
        # Extend or add to the vertices of our model.
        model = this.subsets[subset].model

        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])
        # Record terrain in dictionary :)
        this.td[(floor(x),
                floor(y),
                floor(z))] = "t"
        # Also, record gap above this position to
        # correct for spawning walls after mining.
        if gap==True:
            key =  ((floor(x),
                    floor(y+1),
                    floor(z)))
            if this.td.get(key)==None:
                this.td[key] = "g"

        # Record subset index and first vertex of this block.
        vob = (subset, len(model.vertices)-37)
        this.vd[(floor(x),
                floor(y),
                floor(z))] = vob

        uu = 8
        uv = 7

        model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])

    def genTerrain(this):
        x = 0
        z = 0

        for x_dynamic in range(0,int(this.subWidth)):
            for z_dynamic in range(0,int(this.subWidth)):
                this.genBlock(x+x_dynamic, this.landscale[x+x_dynamic][z+z_dynamic], z+z_dynamic)

        this.subsets[0].model.generate()