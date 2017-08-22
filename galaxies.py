
""" 
Jeu Galaxies
"""

#from ordered_set import OrderedSet # a utiliser ????????????????????????

def doError(): return 0/0 # to generate an error

'''
TYPE_INT = type(123)

def isInt(var):
    res = type(var)==TYPE_INT
    #print(var, res)
    return res
'''
if 0 :
    d = dict()
    d[(1,2)] = "12"
    
    key = (int(1.0), int(2.0))
    print(key, d[key])
    quit()

import tkinter as TK

if 0 :
    ba = bytearray("Salut")# b'Bonjour'
    print(ba)

    quit()
    
#-------------------------    
def yieldFct() :
    i = 0
    while True:
        yield i*i
        i += 1
        
squareGenerator = yieldFct()
#------------------------- 

class listesFournisseursClients:
    def __init__(self, id):
        self.galId   = id    # superflu ! id de la galaxy pour laquelle ces fournisseurs et clients sont valides
        self.fournis = set() # est alimente par au moins un element de la liste
        self.clients = set() # cellules alimentees par  
    
    def addFourni(self, fournisseur):
        self.fournis.add(fournisseur)

    def discardFourni(self, fournisseur):
        self.fournis.discard(fournisseur)
        return self.fournis
    
    def addClient(self, client):
        self.clients.add(client)
        
    def discardClient(self, client):
        self.clients.discard(client)
        return self.clients
    
    def strFours(self):
        s = '{'
        for e in self.clients:
            s += str(e) + ', '
        return s + '}'
    
    def strClis(self):
        s = '{'
        for e in self.clients:
            s += str(e) + ', '
        return s + '}'
    
    def __str__(self):
        return "Galaxy%02d : Fournisseurs:%s, Clients:%s"%(self.galId, self.strFours(), self.strClis())

#print(listesFournisseursClients(3)), quit()        
#----------------------------------------------------
class SetWithData: # liste de dependance d'une cellule relative a une galaxie (ids)
    def __init__(self):
        self.ids          = list()
        self.listsFourCli = list() 
        
    def lfcOfId(self, id):
        return self.listsFourCli[self.ids.index(id)]
    
    def lfcOfIdOrCreateNew(self, id):      
        if id in self.ids :
            return self.lfcOfId(id), False # not newId
        else : # creation d'un nouvel id avec sa listesFournisseursClients
            self.ids.append(id)
            lfc = listesFournisseursClients(id)  
            self.listsFourCli.append(lfc)
            return lfc, True # newId
        
    def addId(self, id):
        lfc, newId = self.lfcOfIdOrCreateNew(id)
        return newId
        
    def addFournisseur(self, id, fournisseur):
        lfc, newId = self.lfcOfIdOrCreateNew(id)
        lfc.addFourni(fournisseur)
        return newId
        
    def discardFournisseur(self, id, fournisseur):
        return self.lfcOfId(id).discardFourni(fournisseur)
    
    def addClient(self, id, client):
        lfc, newId = self.lfcOfIdOrCreateNew(id)
        lfc.addClient(client)
        return newId
        
    def discardClient(self, id, client):
        return self.lfcOfId(id).discardClient(client)
    
    def discard(self, id):
        if id not in self.ids : return None
        i = self.ids.index(id)
        lfc = self.listsFourCli.pop(i)
        id = self.ids.pop(i)
        return id, lfc
    
    def __len__(self): return len(self.ids)
    
    def __getitem__(self, i):
        id = self.ids[i]
        lfc = self.listsFourCli[i]
        return id, lfc

    def __str__(self):
        #return str(list(zip(self.ids, self.listsFourCli)))
        s = ""
        for lfc in self.listsFourCli :
            s += "\n" + str(lfc)
        return s
      
if 0 :
    lid = SetWithData()
    lid.addFournisseur(3,5)
    lid.addFournisseur(2,4)
    lid.addClient(3,7)
    lid.addClient(3,1)
    lid.addFournisseur(3,6)
    print(lid)
    quit()        

#----------------------------------------------------
class Cell: 
    def __init__(self, pos=(0,0), gui=None, root=False):
        self.root = root
        self.gui = gui
        self.pos = pos
        self.id  = None         # set if solved
        self.set_idFournsClients = SetWithData() # set candidate group
        
    def __str__(self):
        s = "root" if self.root else "cell"
        return s + str(self.pos)
    
    def addGroup(self, id):
        newId = self.set_idFournsClients.addId(id)
        if newId and self.gui : self.gui.updateCell(self)
        
    def addFournisseur(self, id, fournisseur): 
        newId = self.set_idFournsClients.addFournisseur(id, fournisseur)
        if newId and self.gui : self.gui.updateCell(self)
        
    def discardFournisseur(self, id, fournisseur):
        fournisseursRestants = self.set_idFournsClients.discardFournisseur(id, fournisseur)
        if self.gui : self.gui.updateCell(self)
        return fournisseursRestants
    
    def addClient(self, id, client): 
        assert client.root==False #, client
        newId = self.set_idFournsClients.addClient(id, client)
        if newId and not self.root and self.gui : self.gui.updateCell(self)
        
    def discardClient(self, id, client):
        clientsRestants = self.set_idFournsClients[id].discardClient(id, client)
        if self.gui : self.gui.updateCell(self)
        return clientsRestants
    
    def getListsFourCli(self, n):            # peu utile
        self.set_idFournsClients.listsFourCli[id]
    
    def getListsFourCliWithId(self, id):
        return self.set_idFournsClients.lfcOfId(id)
    
    def getFournisseurs(self, id):
        return self.getListsFourCliWithId(id).fournis # set
    
    def getClients(self, id):
        return self.getListsFourCliWithId(id).clients # set
    
    def strFournisseurs(self, id):
        return self.getListsFourCliWithId(id).strFours()
    
    def strClients(self, id):
        print(self.getListsFourCliWithId(id))
        return self.getListsFourCliWithId(id).strClis()
    
    def clearAllCandidates(self):
        if not self.root :
            self.set_idFournsClients = SetWithData() # clear all candidates
            if self.gui : self.gui.updateCell(self)
            
    def removeGroup(self, id):
        self.set_idFournsClients.discard(id)
        if self.gui : self.gui.updateCell(self)
        
    def setGroup(self, idToSet): # set definitively the group (solved)
        # examen des consequences sur les dependances (FournisseursClients)
        for id, lfc  in self.set_idFournsClients :
            if id == idToSet       : continue # aucune consequence sur lui_meme
            if len(lfc.clients)==0 : continue # pas de client => pas de consaquence
            for client in lfc.clients:
                print("consequences de la supression dans ", self, " de galaxy%02d , %s"%(lfc.galId, client) )
                print("fournisseurs avant :", client.strFournisseurs(id))
                fournisRestants = client.discardFournisseur(id, self) # on est retire de la liste des fournisseurs de notre client
                print("%s a %d fournisseursRestants"%(client, len(fournisRestants)))
                print("fournisseursRestants :", client.strFournisseurs(id))
                if len(fournisRestants) == 0 : print("!!!!!!!!!!!!!!!!!!!!!!!!!!! lien rompu !!!!!!!!!!")
        self.id = idToSet 
        if self.gui : 
            if self.root : self.gui.setCellId(self)
            else         : self.gui.updateCell(self)
        
    def nbGroups(self):    
        return len(self.set_idFournsClients)
        
    def isFixed(self):
        return self.id != None
        
    def isFree(self):
        return self.id == None
        
    def singleCandidateId(self):
        if not self.isFree()     : return None
        if len(self.set_idFournsClients)!=1 : return None
        #id, dep = self.set_idFournsClients[0] # or bien
        id = self.set_idFournsClients.ids[0] # or bien
        return id #next(iter(self.set_idFournsClients))
    
    def multipleCandidatesIds(self):
        if not self.isFree()     : return None
        if len(self.set_idFournsClients)==1 : return None
        return self.set_idFournsClients

if 0 :
    c1 = Cell(pos=(1,2), root=True)
    print("c1:", c1)
    c2 = Cell(pos=(2,2))
    n = 5
    c2.addFournisseur(n,c1)
    print("c2:", c2)
    print("c2.Fournisseurs(%d):"%n, c2.strFournisseurs(n))
    print(c2.set_idFournsClients.ids)
    print(c2.set_idFournsClients.listsFourCli[0].galId)   
    print(c2.set_idFournsClients.listsFourCli[0].strFours()) 
    print(c2.set_idFournsClients.listsFourCli[0].strClis()) 
    #c2.setGroup(4)                      
    quit()                              
#-------------------------------------------------------------------

class Cells:
    def __init__(self, nbCellsX, nbCellsY, gui=None):
        self.nbCellsX, self.nbCellsY = nbCellsX, nbCellsY
        #self.cells = [list()]*(self.nbCellsX * self.nbCellsY)
        self.cells = list()
        for y in range(self.nbCellsY):
            for x in range(self.nbCellsX):
                self.cells.append(Cell((x,y), gui=gui))
        print("self.cells[0] : " ,self.cells[0])
        
    def getCell(self, x, y):
        ix , iy = int(x), int(y)
        assert ix == x
        assert iy == y
        if ix < 0 or iy < 0 or ix > self.nbCellsX-1 or iy > self.nbCellsY-1 : return None # outside univers
        cell = self.cells[ix+iy*self.nbCellsX]
        #print("getCell(%d,%d) : "%(x,y), cell)
        return cell

    def removeCandidate(self, x, y, cId, color='red'):
        #print("removeCandidate(%d, %d, %d)"%(x, y, cId))
        cell = self.getCell(x, y)
        cell.removeGroup(cId, color=color)
        print("removeCandidate %d at (%d,%d) : reste : "%(cId , x, y), cell )
        return cell
    
    def clearAllCandidatesOfAllcells(self):
        for cell in self.cells : 
            cell.clearAllCandidates()
            
    
    def isFree(self, x, y): # return -3..-5 if outside, -1 if occuped , or the number of possible solution
        cell = self.getCell(x, y)
        if cell and cell.isFree() : return cell.nbGroups()
        return -1
    
    def allCandidates(self, x, y):
        cell = self.getCell(x, y)
        if cell.isFree() : return cell.set_idFournsClients
        return None
    
    def addId(self, ids, ns, x, y): # comptabilise
        cell = self.getCell(x, y)
        if cell and cell.isFixed() :
            id = cell.set_idFournsClients
            if id not in ids :
                ids.append(id)
                ns.append(1)
            else :
                i = ids.index(id)
                ns[i] += 1
    
    def neibourgsIds(self, x, y): # avec comptage
        #print("neibourgsIds(%d,%d)"%(x, y))
        ids = list() # list des groupes voisins
        ns  = list() # nombre de voisin avec le meme groupe
        self.addId(ids, ns, x+1, y)        
        self.addId(ids, ns, x-1, y)        
        self.addId(ids, ns, x, y+1)
        self.addId(ids, ns, x, y-1)
        
        res = list(zip(ids, ns))
        print("neibourgsIds(%d,%d) : "%(x,y), res)
        return res

#-------------------------------------------------------------------

class Galaxy: # set of stars
    def __init__(self, univers, cells, gId, center=(0,0)):
        self.univers = univers
        self.cells   = cells
        self.gId     = gId   # galaxyId
        self.center  = center
        self.stars   = set() 
        
        if self.univers.gui : self.univers.gui.drawStar(center, txt=str(self.gId), color='black')

        self.init()
        
        print(self)
        
    def __str__(self):
        strStars = ''
        for star in self.stars : strStars += " star" + str(star.pos)
        x, y =  self.center
        return "Galaxy%02d at(%3.1f, %3.1f) :%s"%(self.gId, x, y, strStars)
    
    def init(self):
        xC, yC = self.center
        xCentree = (int(xC) == xC)
        yCentree = (int(yC) == yC)
        
        h = 0.5
        if   xCentree     and yCentree : # centree 
            self.addCenterCell(root=True)
        elif not xCentree and yCentree : # a cheval en x
            self.addSymetricStars(+h,0, root=True)
        elif xCentree and not yCentree : # a cheval en y
            self.addSymetricStars(0,-h, root=True) 
            self.addSymetricStars(0,+h, root=True)
        elif not xCentree and not yCentree : # a cheval en x et y
            self.addSymetricStars(+h,-h, root=True)
            self.addSymetricStars(+h,+h, root=True) 
        
    def addCenterCell(self, root=True):
        xC, yC = self.center
        
        cell = self.cells.getCell(xC , yC)
        cell.root = root
        if cell.isFixed() : print("!!! center of galaxy already fixed", cellA)
        else :
            cell.setGroup(self.gId) # fixed
            self.stars.add(cell)
            
    def addSymetricStars(self, dx, dy, root=False):
        xC, yC = self.center
        
        cellA = self.cells.getCell(xC+dx , yC+dy)
        cellA.root = root
        cellB = self.cells.getCell(xC-dx , yC-dy)
        cellB.root = root

        if cellA.isFixed() or cellB.isFixed() : 
            print("!!! cannot add to a galaxy stars already fixed", cellA, cellB)
        else :
            cellA.setGroup(self.gId)
            self.stars.add(cellA)
            
            cellB.setGroup(self.gId)
            self.stars.add(cellB)
        
    def symetricOf(self, cell):
        x, y   = cell.pos
        xC, yC = self.center
        xs, ys = 2*xC-x, 2*yC-y
        return self.cells.getCell(xs , ys) # None is outside univers
        
    def removeStarAndSymetric(self, star):
        self.stars.discard(star)
        self.stars.discard(self.symetricOf(star))
        
    def keepRootStarOnly(self):
        starsList = list(self.stars)
        for star in starsList :
            if not star.root :
                self.stars.discard(star)
    
#-------------------------------------------------------------------
        
class UniversLogic:
    def __init__(self, nbCellsX, nbCellsY, etoiles, gui=None):
        self.gui = gui
        self.nbCellsX, self.nbCellsY = nbCellsX, nbCellsY

        self.cells = Cells(self.nbCellsX, self.nbCellsY, self.gui)
        
        self.galaxies = list()
        
        self.loadGalaxies(etoiles)
        
    def loadGalaxies(self, posGalaxies):
        for i, pos in enumerate(posGalaxies) :
            self.galaxies.append( Galaxy(self, self.cells, i, pos) )
            
    def assignCell(self, x, y, n, fixed=False, color='black'):
        cell = self.cells.getCell(x, y)
        #print("assignCell(%d, %d ,%d)"%(x, y, n), cell)
        if not fixed : 
            cell.addGroup(n, color=color) # set
        else : # if fixed => find implications
            allC = self.cells.allCandidates(x, y)
            if allC :
                #print("allC : ", allC)
                #print("n : ", n)
                allOther = allC - {n}
                #print("allOtherCandidates : ", allOther)
                for cId in allOther :
                    #print("cId : ", cId)
                    i, pos, galaxy = self.galaxies[cId]
                    #print("pos : ", pos)
                    x0, y0 = pos
                    xs, ys = 2*x0-x, 2*y0-y
                    #print("symetric(%d,%d)/%d : (%d,%d)"%(x, y, cId, xs, ys))
                    candidates = self.cells.removeCandidate(xs, ys, cId)
            #self.cells.setCell(x, y, n)
            cell.setGroup(n, color=color)
    
    def assignSymetricCells(self, x, y, dx, dy, n, fixed=False, color='black'):
        self.assignCell(x-dx, y-dy, n, fixed, color)
        self.assignCell(x+dx, y+dy, n, fixed, color)
        
    def symetricCells(self, x, y, n):
        cell = self.cells.getCell(x, y)
        symetricCells = [cell]
        i, pos, galaxy = self.galaxies[n]
        x0, y0 = pos
    
    def removeCandidateFromGalaxyAndSymetricCells(self, x, y, dx, dy, n, color='black'):
        self.cells.removeCandidate(x-dx, y-dy, n, color)
        self.cells.removeCandidate(x+dx, y+dy, n, color)
        
    def findStarsAround(self, galaxy):
        starsAround = set()
        for star in galaxy.stars :
            x, y = star.pos
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) : # in 4 directions
                newStar = self.cells.getCell(x+dx, y+dy)
                #print("newStar:", newStar)
                if newStar == None         : continue # "outside univers"
                if newStar.root            : continue 
                if newStar in galaxy.stars : continue # "already in galaxy"
                if newStar.isFixed() and newStar.id != galaxy.gId : continue # "already affected to an other galaxy"
                
                newStarSym = galaxy.symetricOf(newStar)
                #print("newStarSym:", newStarSym)
                if newStarSym == None         : continue # "outside univers"
                if newStarSym.root            : continue 
                if newStarSym in galaxy.stars : continue # "already in galaxy"
                if newStarSym.isFixed() and newStarSym.id != galaxy.gId : continue # "already affected"
                
                star.addClient(galaxy.gId, newStar)
                star.addClient(galaxy.gId, newStarSym)
                newStar   .addFournisseur(galaxy.gId, star)
                newStarSym.addFournisseur(galaxy.gId, star)
                starsAround.add(newStar)
                starsAround.add(newStarSym)
        if 0 : #len(starsAround) > 0 :
            print("findStarsAround :", galaxy)
            for s in starsAround : print(s)
        return starsAround
    
    def extendGalaxy(self, galaxy):
        x, y = galaxy.center
        galaxy.keepRootStarOnly()
        for t in range(99) :
            starsAround = self.findStarsAround(galaxy)
            if len(starsAround)==0 : 
                print("No more extension for galaxy %d at %d iteration"%(galaxy.gId, t))
                break
            galaxy.stars |= starsAround
            #for star in starsAround: star.addGroup(galaxy.gId)
    
    def findAllExtensions(self):
        while True :
            color='red'
            #print("Start findAllExtensions loops")
            self.cells.clearAllCandidatesOfAllcells()
            for galaxy in self.galaxies :
                self.extendGalaxy(galaxy)
                '''
                x, y = galaxy.center
                galaxy.keepRootStarOnly()
                for t in range(99) :
                    starsAround = self.findStarsAround(galaxy)
                    if len(starsAround)==0 : 
                        print("No more extension for galaxy %d at %d iteration"%(galaxy.gId, t))
                        break
                    galaxy.stars |= starsAround
                    for star in starsAround:
                        star.addGroup(galaxy.gId)
                '''
                yield True # ok iteration not finished
            #print("End loops findAllExtensions")
            yield False
        
    def setCellAndSym(self, cell, id):
        galaxy = self.galaxies[id]
        symStar = galaxy.symetricOf(cell)
        if symStar :
            cell.setGroup(id)
            symStar.setGroup(id)
        else :
            print("cannot find in %s a symetric of %s"%(galaxy, cell))
        #print("singleCandidateId : ", id)
        #self.assignSymetricCells(x0, y0, dx, dy, id, fixed=True, color='green')
        
    def lockSingleCandidates(self):
        while True :
            print("Start lockSingleCandidates loops")
            for x in range(self.nbCellsX):
                for y in range(self.nbCellsY):
                    cell = self.cells.getCell(x, y)
                    if cell.root : continue
                    if cell.isFixed() :
                        if cell.id not in cell.set_idFournsClients.ids :
                            print(cell, " : deconnectee !!!!!!!!!!!!!!!!!")
                    else :
                        ids = cell.set_idFournsClients.ids
                        if len(ids) > 1 :
                            for id in ids :
                                self.galaxies[id].removeStarAndSymetric(cell)
                            cell.clearAllCandidates()
                            continue
                        id = cell.singleCandidateId()
                        if id != None : # fixe candidat unique
                            self.setCellAndSym(cell, id)
                            yield True # attend un rappel pour iterrer
            print("End loops findAllExtensions")
            yield False
        
    def choseCandidateWithSameGroupFellow(self):
        while True :
            print("Start choseCandidateWithSameGroupFellow loops")
            for x in range(self.nbCellsX):
                for y in range(self.nbCellsY):
                    cell = self.cells.getCell(x, y)
                    candidatsIds = cell.multipleCandidatesIds()
                    if candidatsIds != None :
                        neibourgsIdsAndNb = self.cells.neibourgsIds(x, y)
                        fittingIds = list()
                        for candidatId in candidatsIds :
                            for neibourgId, nb in neibourgsIdsAndNb :
                                if neibourgId == candidatId :
                                    fittingIds.append((candidatId, nb))
                        nbFits = len(fittingIds)
                        if   nbFits==0 : 
                            print("Not found neibourgs with id %d"%candidatId)
                        else :
                            if nbFits==1 :
                                id = fittingIds[0][0]
                                #print("Neibourgs : un seul : ", id)
                            else :
                                #print("Neibourgs : sorting fits")
                                sortedFitting = sorted(fittingIds, key = lambda e : e[1], reverse=True)
                                #print("Neibourgs : fits sorted : ", sortedFitting)
                                if sortedFitting[0][1] == sortedFitting[1][1] :
                                    print("Neibourgs : premiers exequo !!! : ",sortedFitting)
                                    break
                                else : id = sortedFitting[0][0]
                            #print("Neibourgs ok :", id)
                            i, pos, galaxy = self.galaxies[id]
                            x0, y0 = pos
                            dx, dy = x - x0, y - y0
                            self.assignSymetricCells(x0, y0, dx, dy, id, fixed=True, color='blue')
                            yield True # attend un rappel pour iterrer
            print("End loops choseCandidateWithSameGroupFellow")
            yield False
        
    def buildWalls(self):
        while True :
            print("build vertical walls")
            for y in range(self.nbCellsY):
                vr = self.cells.getCell(0, y).id #.cells[0 + y*self.nbCellsX].
                for x in range(self.nbCellsX - 1):
                    vl = vr
                    vr = self.cells.getCell(x+1, y).id #.cells[x+1 + y*self.nbCellsX]
                    if vr != vl :
                        #print("vertical walls at (%d,%d)"%(x+1, y))
                        if self.gui : self.gui.drawVertWall(x+1, y)
                        yield True
            print("build horizontal walls")
            for x in range(self.nbCellsX):
                vb = self.cells.getCell(x, 0).id #cells[x + 0*self.nbCellsX]
                for y in range(self.nbCellsY - 1):
                    vt = vb
                    vb = self.cells.getCell(x, y+1).id # cells[x + (y+1)*self.nbCellsX]
                    if vb != vt : 
                        #print("horizontal walls at (%d,%d)"%(x, y+1))
                        if self.gui : self.gui.drawHorizWall(x, y+1)
                        yield True
            print("End loops buildWalls")
            yield False
        
#----------------------------------------------------------

class StatusBar(TK.Frame):
    def __init__(self, master):
        TK.Frame.__init__(self, master)
        self.label = TK.Label(self, text="Bonjour", bd=1, relief=TK.SUNKEN, anchor=TK.W)
        self.label.pack(fill=TK.X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()   
        
class CellInfos:
    def __init__(self, nbCellsX, nbCellsY):
        self.nbCellsX, self.nbCellsY = nbCellsX, nbCellsY
        #self.cells = [list()]*(self.nbCellsX * self.nbCellsY)
        self.cellInfos = list()
        for i in range(self.nbCellsX * self.nbCellsY):
            l = list()
            self.cellInfos.append(l)
            
    def addId(self, x, y, id):
        ix , iy = int(x), int(y)
        assert ix == x
        assert iy == y
        infosIds = self.cellInfos[ix+iy*self.nbCellsX]
        infosIds.append(id)
        #print("addId : ", ix, iy, len(self.cellInfos[ix+iy*self.nbCellsX]))

    def getInfosIds(self, x, y):
        ix , iy = int(x), int(y)
        assert ix == x
        assert iy == y
        return self.cellInfos[ix+iy*self.nbCellsX]
        
#---------------------------------------------------------------------------------------------

class GeneratorWithDelay:
    def __init__(self, fct, delay=1000):
        self.fct   = fct
        self.delay = delay
        self.run   = False
        
    def start(self):
        print("Start ", self.fct.__name__)
        self.run = True
    
    def stop(self):
        self.run = False
        print("Stop ", self.fct.__name__)
    

class GuiBoard(TK.Frame):
    def __init__(self, parent, nbCellsX, nbCellsY):
        TK.Frame.__init__(self, parent)
        self.parent = parent
        
        toolbar = TK.Frame(parent)
        TK.Button(toolbar, text="Extend" , command = self.extend     ).pack(side = TK.LEFT )
        TK.Button(toolbar, text="Solve"  , command = self.solve      ).pack(side = TK.LEFT )
        TK.Button(toolbar, text="Fellow" , command = self.checkFellow).pack(side = TK.LEFT )
        TK.Button(toolbar, text="Walls"  , command = self.walls      ).pack(side = TK.LEFT )
        self.label = TK.Label(toolbar, text="Bonjour", bd=3, width=6, anchor=TK.E, font="Courrier 14 bold", relief=TK.SUNKEN) #, justify=TK.RIGHT
        self.label.pack(side = TK.LEFT )
        TK.Button(toolbar, text="Quit" , command = TK.sys.exit ).pack(side = TK.RIGHT)
        toolbar.pack(side=TK.TOP, fill=TK.X)

        self.nbCellsX, self.nbCellsY = nbCellsX, nbCellsY
                
        self.W, self.H = 400, 400
        self.d = 2 * min(self.W//2//(self.nbCellsX+2), self.H//2//(self.nbCellsY+2))
        self.offsetX = self.d
        self.offsetY = self.d
        print("self.d : " , self.d)
        self.canvas = TK.Canvas(parent, width=self.d*(self.nbCellsX+2), height=self.d*(self.nbCellsY+2))
        self.canvas.pack()
        '''
        self.status_bar = StatusBar(parent)
        self.status_bar.pack(side=TK.BOTTOM, fill=TK.X)
        '''
        
        cmdFrame = TK.Frame(parent)
        cmdFrame.pack(side=TK.BOTTOM, fill=TK.X)
        TK.Button(cmdFrame, text="exec", width=6, command=self.execute).pack(side=TK.RIGHT)
        self.cmdLine = TK.Entry(cmdFrame)
        self.cmdLine.pack(fill=TK.X)
        
        self.cellsInfos = CellInfos(self.nbCellsX, self.nbCellsY)
            
        self.drawGrid()
        
        self.wallsIds = list()
        self.drawFrameWall()
        
        self.generatorsWithDelay = list()
        
        self.tickCnt = 0
        self.clockDelay = 200
        self.update_clock() # startClock
    
    def setUniversLogic(self, universLogic):
        self.universLogic = universLogic
        
        self.generatorsWithDelay.append(GeneratorWithDelay(self.universLogic.findAllExtensions(), 100))
        self.generatorsWithDelay.append(GeneratorWithDelay(self.universLogic.lockSingleCandidates(), 400))
        self.generatorsWithDelay.append(GeneratorWithDelay(self.universLogic.choseCandidateWithSameGroupFellow(), 600))
        self.generatorsWithDelay.append(GeneratorWithDelay(self.universLogic.buildWalls(), 100))
        
    def update_clock(self):
        self.tickCnt += 1
        self.label['text'] = self.tickCnt # next(squareGenerator) 
        self.parent.after(self.clockDelay, self.update_clock)
        
        for gene in self.generatorsWithDelay :
            if gene.run :
                resp = next(gene.fct)
                #print("resp :", resp)
                if not resp : 
                    gene.stop()
                    
    def extend(self):
        self.generatorsWithDelay[0].start()
    
    def solve(self):
        self.generatorsWithDelay[1].start()
    
    def checkFellow(self):
        self.generatorsWithDelay[2].start()
    
    def walls(self):
        self.deleteWalls()
        self.generatorsWithDelay[3].start()
    
    def execute(self):
        cmdLin = self.cmdLine.get()
        leftOp, rightOp = cmdLin.split('=')
        cmd1 = "cell = self.universLogic.cells.getCell%s"%(leftOp.strip())
        cmd2 = "self.universLogic.setCellAndSym(cell,%s)"%(rightOp.strip())
        print("execute", cmd1, cmd2)
        exec(cmd1)
        exec(cmd2)
    
    def drawGrid(self):
        x0, y0, x1, y1 = 0 , 0, self.d*self.nbCellsX, self.d*self.nbCellsY
        x0 += self.offsetX
        y0 += self.offsetY
        x1 += self.offsetX
        y1 += self.offsetY
        self.canvas.create_rectangle(x0, y0, x1, y1, fill='white')
        
        x0, x1 = self.offsetX, self.d*self.nbCellsX + self.offsetX
        for i in range(self.nbCellsY+1):
            y = self.d*i + self.offsetY
            self.canvas.create_line(x0, y, x1, y, fill='gray')
            
        y0, y1 = self.offsetY, self.d*self.nbCellsY + self.offsetY
        for i in range(self.nbCellsX+1):
            x = self.d*i + self.offsetX
            self.canvas.create_line(x, y0, x, y1, fill='gray')
            
    def drawStar(self, pos=(3.5,2), txt='', color='black'):
        xc, yc = pos
        r = self.d/4
        xCenter = xc*self.d + self.d/2 + self.offsetX
        yCenter = yc*self.d + self.d/2 + self.offsetY
        self.canvas.create_oval(xCenter-r, yCenter-r, xCenter+r, yCenter+r, outline='black', fill='white') # "#000000"
        #self.text_id = self.canvas.create_text(xCenter, yCenter, text=txt, fill='red') # , anchor="w", justify="left", font=style.font
        
    def deletePreviousCandidats(self, xc, yc):
        for id in self.cellsInfos.getInfosIds(xc, yc):
            self.canvas.delete(id)
    
    def updateCell(self, cell, color='black'):
        assert not cell.root
        
        xc, yc = cell.pos
        self.deletePreviousCandidats(xc, yc)
        xCenter = xc*self.d + self.d/2  + self.offsetX
        yCenter = yc*self.d + self.d/2  + self.offsetY
        
        
        if cell.id != None :
            #print("update Candidat Elu in cell (%d,%d) at %d,%d"%(xc, yc, xCenter, yCenter))
            txtId = self.canvas.create_text(xCenter, yCenter, text=str(cell.id), fill='green') # , anchor="w", justify="left", font=style.font
            if not cell.root : self.cellsInfos.addId(xc, yc, txtId)
        e = (self.d*26)/100
        for i, candidatId in enumerate(cell.set_idFournsClients.ids) :
            color = 'green' if candidatId == cell.id else 'red'
            if   i==0 : dx, dy = -e,-e
            elif i==1 : dx, dy = +e,-e
            elif i==2 : dx, dy = -e,+e
            elif i==3 : dx, dy = +e,+e
            else      : print("trop de candidats a afficher")
            #print("update Candidat%d in cell (%d,%d) at %d,%d"%(i, xc, yc, xCenter, yCenter))
            txtId = self.canvas.create_text(xCenter+dx, yCenter+dy, text=str(candidatId), fill=color) # , anchor="w", justify="left", font=style.font
            self.cellsInfos.addId(xc, yc, txtId)

    def setCellId(self, cell):
        assert cell.root
        xc, yc = cell.pos
        xCenter = xc*self.d + self.d/2  + self.offsetX
        yCenter = yc*self.d + self.d/2  + self.offsetY
        self.canvas.create_text(xCenter, yCenter, text=str(cell.id), fill='black') # , anchor="w", justify="left", font=style.font
        
    
    def drawHorizWall(self, xc, yc, fixe=False, fill = 'black'):
        e = 1
        r = 0
        x0, y0, x1, y1 = self.d*xc+r, self.d*yc-e, self.d*(xc+1)-r, self.d*yc+e
        x0 += self.offsetX
        y0 += self.offsetY
        x1 += self.offsetX
        y1 += self.offsetY
        id = self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
        if not fixe : self.wallsIds.append(id)
        
    def drawVertWall(self, xc, yc, fixe=False, fill = 'black'):
        e = 1
        r = 0
        x0, y0, x1, y1 = self.d*xc-e, self.d*yc+r, self.d*xc+e, self.d*(yc+1)-r
        x0 += self.offsetX
        y0 += self.offsetY
        x1 += self.offsetX
        y1 += self.offsetY
        id = self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
        if not fixe : self.wallsIds.append(id)
    
    def deleteWalls(self):
        for id in self.wallsIds:
            self.canvas.delete(id)
            
    def drawFrameWall(self):
        yc = 0
        for xc in range(self.nbCellsX):
            self.drawHorizWall(xc, yc, fixe=True)
    
        yc = nbCellsY
        for xc in range(self.nbCellsX):
            self.drawHorizWall(xc, yc, fixe=True)
    
        xc = 0
        for yc in range(self.nbCellsY):
            self.drawVertWall(xc, yc, fixe=True)
    
        xc = nbCellsX
        for yc in range(self.nbCellsY):
            self.drawVertWall(xc, yc, fixe=True)
    
#=================================================================

if __name__ == "__main__":

    nbCellsX, nbCellsY = 7, 7
    
    root = TK.Tk()
    root.title(__file__)
    gui = GuiBoard(root, nbCellsX, nbCellsY)
    posGalaxies1 = [(0.5,0), (5.5,0), 
        (0,1),
        (3.5,1.5), (5.5,1.5), 
        (1,2.5),
        (6,3), 
        (6,4.5),
        (2.5,5), 
        (5,6),
        ]
    posGalaxies2 = [(2,0), (5.5,0.5), 
        (0, 1),
        (1.5, 1.5),
        (4.5, 2.5), 
        (1, 3),
        (4, 4),(6, 4), 
        (2, 5),
        (5.5, 5.5),
        (0, 6),
        ]
    posGalaxies3 = [(3,3), 
        (2, 1),
        (4, 5),
        (1, 1.5), 
        (5, 4.5),
        (0,4),(6,2),
        ]
    universLogic = UniversLogic(nbCellsX, nbCellsY, posGalaxies2, gui)
    gui.setUniversLogic(universLogic)
    
    root.mainloop()
