'''
This script provides a GUI and automatic exploration algorithms with different strategies
It is only used to dump the map and NOT the final solution
To solve this chall you should synchronize the random seed with server so that you can predict the position of chars you caught (during which the whole map used at server required)
'''

from pwn import *
from random import randint
import cPickle as pickle

context.log_level='debug'

c = remote('78.47.17.200', 7888)

cmds = 'wasd'
delta = [[0,-1],[-1,0],[0,1],[1,0]]
m = pickle.load(open('map'))

'''
for i in range(50):
    for j in range(50):
        m[i][j] = -1
'''
v = []
for i in range(50):
    v.append([0]*50)

d = c.recv().split('\x00')
curx, cury = 0,0
todo = []
fs = []
head = 2
cnt = 0
rand = False
MS = 11 # show map size should be odd
rev = [2,3,0,1]
remain = 0 # is close?

def docheck(x,y):
    global stage
    print 'check',x,y
    cand = -1
    for i in range(4):
        xx = x+delta[i][0]
        yy = y+delta[i][1]
        if xx<0 or xx>=50 or yy<0 or yy>=50:
            continue
        print xx,yy,m[yy][xx]
        if m[yy][xx]==-1:
            if cand == -1:
                cand = i
            else:
                return False
        elif m[yy][xx]==1:
            return True # might wrong
    if cand != -1:
        xx = x+delta[cand][0]
        yy = y+delta[cand][1]
        print 'detect',yy,xx
        m[yy][xx] = 1
        return True
    print 'warning!!!'
    stage = -1
    return True

def showmap(curx,cury):
    for ij in range(MS):
        for ii in range(MS):
            x=curx+ii-MS/2
            y=cury+ij-MS/2
            if x<0 or x>=50 or y<0 or y>=50:
                print '#',
            elif m[y][x]==-1:
                print '?',
            elif m[y][x]==1:
                print 'X',
            elif x==curx and y==cury:
                print '@',
            else:
                print '.',
        print 

# init
ys = 25
xs = 40
for i in range(ys):
    c.sendline('s')
    c.recv()
cury = ys
for i in range(xs):
    c.sendline('d')
    c.recv()
curx = xs

stage = -1
danger = False
v[0][0] = 1
while True:
    '''
    if curx==32 and cury==0:
        todo = [2,3,3,0][::-1]
    if len(todo)>0:
        idx = todo.pop()
    else:
    '''
    force = False
    showmap(curx,cury)
    idx = (head+3)%4 # stage=0 defaults

    '''
    if curx==0 and cury==25:
        stage = 1
    elif curx==25 and cury==25:
        stage = 0
    '''
    if stage == 1:
        idx = 3
    elif stage == 4:
        if curx%2==0:
            if cury==26:
                idx = 3
            elif cury==25 or cury==24:
                idx = 2
        else:
            if cury==26 or cury==25:
                idx = 0
            elif cury==24:
                idx = 3
        if curx in [12,14,21,33,43,47,48] and cury==25:
            idx = 3
        if curx==48:
            stage = 2
    elif stage == 5:
        if curx==0 and cury==22:
            rand = True
        if rand:
            if curx == 17 and cury in [21]:
                idx = 2
            else:
                idx = 3
        if curx==50:
            part = ['?']*51
            for f in fs:
                part[f[1]] = f[0]
            print ''.join(part)
            break
    elif stage == 2:
        while True:
            idx = randint(0,3)
            if remain>0:
                remain -= 1
                break
            if idx != rev[head]:
                break
        '''
        lim = 10
        if 25-curx>lim:
            idx = 3
        elif curx-25>lim:
            idx = 1
        elif 25-cury>lim:
            idx = 2
        elif cury-25>lim:
            idx = 0
        if danger:
            idx = rev[head]
        '''
    elif stage == -1:
        while True:
            try:
                line = raw_input().strip()
                if cmds.find(line)!=-1:
                    idx = cmds.find(line)
                    force = True
                    break
                if line=='q':
                    stage = 3
                    break
                elif line=='auto':
                    stage = 2
                c0,c1 = line.split(' ')
                if c0=='set1':
                    x,y=map(int,c1.split(','))
                    m[y][x]=1
                elif c0=='set0':
                    x,y=map(int,c1.split(','))
                    m[y][x]=0
            except:
                pass
    if stage==3:
        break

    if not force:
        found = False
        '''
        for i in range(4):
            x = curx+delta[idx][0]
            y = cury+delta[idx][1]
            if x>=0 and y>=0 and x<50 and y<50 and m[y][x]!=1 and v[y][x]!=1:
                found = True
                break
            idx = (idx+1)%4
        '''
        if not found:
            while True:
                x = curx+delta[idx][0]
                y = cury+delta[idx][1]
                if x>=0 and y>=0 and x<50 and y<50 and m[y][x]!=1:
                    break
                idx = (idx+1)%4
    head = idx
    c.sendline(cmds[idx])
    if d[0]!='iw':
        curx += delta[idx][0]
        cury += delta[idx][1]
    print curx,cury
    print fs
    print 'state:',stage, head, remain
    v[cury][curx] = 1
    cnt += 1
    #v[cury][curx] = cnt
    try:
        rep = c.recv().strip().split('\n')
        d = []
        for tmp in rep:
            d.extend(tmp.split('\x00'))
    except:
        break
    if d[0]!='i' and d[0]!='iw':
        print '---'
        print d
        if 'Congrats' in ''.join(d):
            break
        print '---'
    if d[0]=='f':
        fs.append((d[1],curx,cury,cnt))
        # flag moves (cnt-1)/2 steps
        d = d[2:]
    if d[0]=='i':
        m[cury][curx] = 0
        if len(d)==1:
            # not in danger
            for ii in range(4):
                x = curx+delta[ii][0]
                y = cury+delta[ii][1]
                if x>=0 and y>=0 and x<50 and y<50:
                    m[y][x] = 0
                
        if len(d)>1 and 'breeze' in ''.join(d):
            if not docheck(curx,cury):
                danger = True
            else:
                danger = False
        else:
            danger=False
        if stage == 2 and len(d)>1 and 'smell' in ''.join(d):
            remain = 10
    if d[0]=='d':
        m[cury][curx] = 1

pickle.dump(m, open('map','w'))
c.interactive()
