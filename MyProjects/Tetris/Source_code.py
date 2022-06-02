grille = [['J', 'R', 'R', 'N', 'V', 'R', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE'],
          ['R', 'R', 'B', 'J', 'VIDE', 'R', 'N', 'V', 'VIDE', 'VIDE', 'VIDE', 'VIDE'],
          ['J', 'N', 'N', 'R', 'VIDE', 'J', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE'],
          ['J', 'J', 'R', 'R', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'N', 'V', 'R'],
          ['J', 'VIDE', 'R', 'VIDE', 'VIDE', 'R', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE'],
          ['VIDE', 'V', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE'],
          ['J', 'VIDE', 'R', 'VIDE', 'VIDE', 'R', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE', 'VIDE']]
l,h=len(grille),len(grille[0])
#-----------------------------------------------------------------------------------
def creeGrille(l,h):
        return( [ [ "VIDE" for j in range(h) ] for i in range(l) ] )
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
def color(x,y):
        if grille[x][y]=="J":return("yellow")
        if grille[x][y]=="R":return("red")
        if grille[x][y]=="N":return("black")
        if grille[x][y]=="V":return("green")
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------        
#-----------------------------------------------------------------------------------
def grilleLibre(grille,k,i):
    for j in range(h-k,h):
        if grille[i][j]!= 'VIDE':
            return False
    return True
#-----------------------------------------------------------------------------------
def descente(grille,x,y,k):
    if y!=0 and grille[x][y-1]=="VIDE":
        for j in range(y,y+k):
            grille[x][j-1]=grille[x][j]
        grille[x][y+k-1]="VIDE"
#-----------------------------------------------------------------------------------
def deplacerBarreau(grille,x,y,k,d):
    for i in range(y,y+k):  
        if x+d==l or x+d==-1 or  grille[x+d][i]!="VIDE":
            return
    for j in range(y,y+k):
        grille[x+d][j]=grille[x][j]
        grille[x][j]="VIDE"
#-----------------------------------------------------------------------------------
def permuterBarreau(grille,x,y,k):
    s=grille[x][y]
    for j in range(y,y+k-1):
        grille[x][j]=grille[x][j+1]
    grille[x][y+k-1]=s
#-----------------------------------------------------------------------------------
def descenteRapide(grille,x,y,k):
    s=0
    for j in range(y-1,0,-1):
        if grille[x][j]== 'VIDE':s+=1
        else:break
    if s!=0:
        for j in range(0,k):
            grille[x][y-s+j]=grille[x][y+j]
            grille[x][y+j]="VIDE"
    return(s)
        
#-----------------------------------------------------------------------------------
def detecteAlignement(rangee):
    n,x,score,count=len(rangee),rangee[0],0,1
    marking=[False for j in range(n)]
    for i in range(1,n):
        y=rangee[i] 
        if y==x and y!="VIDE": count+=1
        else:
            if count>2:
                score+=count-2
                for j in range(count):marking[i-1-j]=True
            count,x=1,y
    if count>2:
        score+=count-2
        for j in range(count):marking[n-1-j]=True
    return (marking, score)
#-----------------------------------------------------------------------------------
def scoreRangee(grille,g,i,j,dx,dy):
    if dx==0 and dy==0: return 0
    else:
        x,y,rangee=i,j,[]
        while 0 <=x <l and 0<=y<h:
            rangee.append(grille[x][y])
            x,y=x+dx,y+dy
        marking,score=detecteAlignement(rangee)
        for p in range(len(rangee)):
            if marking[p]:
                g[i+p*dx][j+p*dy]="VIDE"
        return score
#-----------------------------------------------------------------------------------
def copie(grille):
    return [[grille[i][j] for j in range(h)] for i in range(l)]
#-----------------------------------------------------------------------------------
def effaceAlignement(grille):
    g=copie(grille)
    score,dx,dy=0,1,1
    for i in range(l):
        score+= scoreRangee(grille,g,i,0,dx,dy)
    for j in range(1,h):
        score+= scoreRangee(grille,g,0,j,dx,dy)
    dx,dy=1,0
    for k in range(h):
        score+= scoreRangee(grille,g,0,k,dx,dy)
    dx,dy=1,-1
    for m in range(l):
        score+= scoreRangee(grille,g,m,h-1,dx,dy)
    for s in range(h-1):
        score+= scoreRangee(grille,g,0,s,dx,dy)
    dx,dy=0,1
    for r in range(l):
        score+= scoreRangee(grille,g,r,0,dx,dy)
    return (afficheGrille(g),score)
#-----------------------------------------------------------------------------------
def tassementGrille(grille):
    for i in range(l):
        p=0
        for j in range(h):
            if grille[i][j]=="VIDE":p+=1
            elif p!=0:
                grille[i][j-p],grille[i][j]=grille[i][j],"VIDE"
#-----------------------------------------------------------------------------------
def calculScore(grille):
    score,s=0,1999
    while s!=0:
        T,s= effaceAlignement(grille)
        tassementGrille(T)
        grille,score=T,score+s
    return (afficheGrille(grille),score)
#-----------------------------------------------------------------------------------
def tailleRegionUnicolore(grille,x,y):
        if grille[x][y]=="VIDE":return((grille,0))
        c=grille[x][y]
        grille[x][y],res= "VIDE",1
        if x>0 and grille[x-1][y]==c:
                res+= tailleRegionUnicolore(grille,x-1,y)[1]
        if x+1<l and grille[x+1][y]==c:
                res+= tailleRegionUnicolore(grille,x+1,y)[1]
        if y>0 and grille[x][y-1]==c:
                res+= tailleRegionUnicolore(grille,x,y-1)[1]
        if y+1<h and grille[x][y+1]==c:
                res+= tailleRegionUnicolore(grille,x,y+1)[1]
        return(grille,res)
#-----------------------------------------------------------------------------Bonus
def calculScore2(g):
    s=0
    def check(grille,x,y):
            G=copie(grille)
            if 3<=tailleRegionUnicolore(G,x,y)[1]:
                    return True        
    T=True
    while T==True:
        T=False
        tassementGrille(g)
        for x in range(l):
            for y in range(h):
                if g[x][y]!="VIDE":
                        if check(g,x,y)==True:
                                s+=tailleRegionUnicolore(g,x,y)[1]
                                T=True
                                
    return(s)
#-----------------------------------------------------------------------------------
def creeBarreau(grille):
        import random as rn
        a=rn.randint(1,3)
        b=rn.randint(0,5)
        if grilleLibre(grille,a,b):
                for i in range(a):
                        grille[b][h-i-1]=rn.choice(["J","R","N","V"])
        return(b,h-a,a)

#-----------------------------------------------------------------------------------                            
#-----------------------------------------------------------------------------------

