"""SCREENER: ASCII Screensaver Maker"""
import pygame, sys, math, random, json, os, colorsys, time
pygame.init()

SAVE_FILE = "screener_settings.json"
FPS = 60
UI_FS = 14
MIN_F, MAX_F, DEF_F = 10, 28, 16

C_BG=(8,8,14); C_PANEL=(14,14,22); C_BORDER=(200,205,215); C_DIM=(80,85,95)
C_TEXT=(170,175,180); C_HI=(230,235,240); C_ACCENT=(0,255,200)
C_HOVER=(25,30,40); C_ACTIVE=(15,35,35); C_BTN=(35,38,52); C_BTN_H=(50,55,72)
C_SL_BG=(30,30,42); C_SL_FG=(0,200,180); C_PLAY=(0,220,100); C_DANGER=(220,60,60)

BG_COLORS = {"Black":(0,0,0),"Dark Navy":(5,5,20),"Dark Green":(0,8,4),
             "Dark Purple":(8,2,12),"Dark Red":(10,2,2),"Charcoal":(12,12,12)}
BG_NAMES = list(BG_COLORS.keys())

CHAR_SETS = {
    "blocks": "░▒▓█▄▀■□▌▐▪▫",
    "greek": "αβγδεζηθικλμνξπρστυφχψωΓΔΘΛΞΠΣΦΨΩ",
    "geometry": "◊○●◆◇■□▲△▼▽★☆♦♠♣♥",
    "binary": "01",
    "symbols": "@#$%&*+=~!?<>{}[]|/\\^:;",
    "classic": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    "math": "±×÷∞≈≠≤≥√∂∑∏∫",
    "arrows": "←→↑↓↔↕◄►▲▼",
    "currency": "$¢£¥©®™°§¶†‡",
    "box_draw": "─│┌┐└┘├┤┬┴┼═║╔╗╚╝╠╣╦╩╬",
}
CS_NAMES = list(CHAR_SETS.keys())

COLOR_PALETTES = {
    "phosphor_green":[(51,255,51),(34,204,34),(17,153,17),(0,102,0)],
    "amber_crt":[(255,176,0),(255,140,0),(204,108,0),(153,76,0)],
    "cool_white":[(220,230,255),(180,195,230),(140,155,200),(90,100,150)],
    "deep_ocean":[(0,200,220),(0,140,180),(0,80,130),(0,30,80)],
    "forest_floor":[(140,200,60),(80,160,40),(50,120,30),(20,80,20)],
    "autumn_decay":[(220,180,50),(200,140,30),(180,80,20),(120,40,10)],
    "volcanic":[(255,120,0),(255,60,0),(200,30,0),(120,0,0)],
    "arctic_aurora":[(0,255,128),(0,200,255),(128,0,255),(255,0,128)],
    "bioluminescent":[(0,255,200),(0,200,255),(0,150,180),(0,100,120)],
    "desert_dusk":[(200,100,50),(180,60,80),(120,40,100),(60,20,80)],
    "coral_reef":[(255,127,80),(255,99,71),(255,69,0),(200,50,50)],
    "c64_purple":[(134,122,222),(108,94,181),(80,69,155),(53,40,121)],
    "gameboy":[(155,188,15),(139,172,15),(48,98,48),(15,56,15)],
    "vaporwave":[(255,113,206),(185,103,255),(1,205,254),(5,255,161)],
    "tron_blue":[(0,200,255),(0,255,255),(0,150,200),(0,80,120)],
    "mainframe":[(255,150,0),(255,100,0),(200,80,0),(150,50,0)],
    "blood_moon":[(180,0,0),(120,0,20),(80,0,40),(40,0,30)],
    "lavender_mist":[(200,180,255),(170,140,230),(140,100,200),(100,60,160)],
    "midnight_blue":[(120,120,200),(80,80,160),(60,60,120),(40,40,80)],
    "toxic_waste":[(200,255,0),(128,255,0),(0,255,0),(0,200,0)],
    "old_paper":[(210,180,140),(180,150,110),(150,120,80),(100,80,50)],
    "hot_pink":[(255,0,200),(255,0,128),(200,0,255),(150,0,200)],
    "golden_hour":[(255,200,50),(255,160,30),(230,120,20),(180,80,10)],
    "steel":[(180,190,200),(140,150,165),(100,110,130),(60,70,85)],
    "matrix":[(0,255,65),(0,200,50),(0,140,35),(0,80,20)],
    "electric":[(100,0,255),(200,0,255),(255,0,200),(255,0,100)],
    "infrared":[(255,0,0),(200,0,50),(150,0,100),(100,0,80)],
    "synthwave":[(255,0,128),(180,0,255),(0,180,255),(255,0,255)],
    "pastel_dream":[(255,179,186),(255,223,186),(255,255,186),(186,255,201)],
    "bruise":[(140,80,160),(100,40,120),(80,20,100),(60,0,80)],
    "rust":[(183,65,14),(160,50,10),(120,35,5),(80,20,0)],
    "beach_sunset":[(255,94,77),(255,154,100),(255,206,135),(255,240,165)],
    "northern_lights":[(0,255,100),(0,180,200),(80,0,255),(200,0,180)],
    "coffee":[(200,150,100),(160,110,70),(120,75,40),(80,45,15)],
    "candy":[(255,100,150),(255,150,50),(100,255,150),(150,50,255)],
    "twilight":[(80,40,120),(60,60,140),(40,80,160),(20,120,180)],
    "copper":[(204,120,50),(180,100,40),(140,75,25),(100,50,10)],
    "emerald":[(0,200,100),(0,160,80),(0,120,60),(0,80,40)],
    "sakura":[(255,183,197),(255,150,170),(240,120,150),(200,80,120)],
    "glacier":[(200,240,255),(160,210,240),(120,180,220),(80,140,200)],
    "firefly":[(200,255,100),(150,200,50),(100,150,0),(60,100,0)],
}
PAL_NAMES = list(COLOR_PALETTES.keys())

ANIM_NAMES = ["Matrix Rain","Sine Wave","Spiral Vortex","Bouncing Particles",
              "Drifting Snow","Cellular Automata","Warp Tunnel"]

MONO_FONT = 'firacode'

_cc = {}
def _cc_clear():
    global _cc; _cc.clear()
def rc(font, ch, color):
    k = (id(font), ch, color)
    if k not in _cc:
        try: _cc[k] = font.render(ch, True, color)
        except: _cc[k] = font.render("?", True, color)
    return _cc[k]
def lc(c1, c2, t):
    return tuple(int(a+(b-a)*t) for a,b in zip(c1,c2))
def palc(pal, t):
    t=max(0.0,min(1.0,t)); n=len(pal)
    if n==1: return pal[0]
    idx=t*(n-1); i=int(idx); f=idx-i
    return pal[-1] if i>=n-1 else lc(pal[i],pal[i+1],f)
def sc(c, s):
    return tuple(max(0,min(255,int(v*s))) for v in c)
def load_font(size):
    p = pygame.font.match_font(MONO_FONT)
    if p:
        try: return pygame.font.Font(p, size)
        except: pass
    return pygame.font.SysFont('monospace', size)

class Animation:
    def __init__(self):
        self.cols=self.rows=0; self.size=1.0
    def resize(self,c,r):
        if c!=self.cols or r!=self.rows:
            self.cols,self.rows=c,r; self._init()
    def _init(self): pass
    def update(self,dt,speed,trail=8,count=100,size=1.0):
        self.size=size
    def get_cells(self): return []

class MatrixRain(Animation):
    def _init(self):
        self.drops=[]
        for c in range(self.cols):
            self.drops.append({'y':random.uniform(-self.rows,0),
                'spd':random.uniform(0.4,1.8),'ln':random.randint(4,max(5,self.rows//2)),
                'chars':[random.random() for _ in range(self.rows+20)]})
    def update(self,dt,speed,trail=8,count=100,size=1.0):
        super().update(dt,speed,trail,count,size)
        for d in self.drops:
            d['ln']=max(3,int(trail*size))
            d['y']+=d['spd']*speed*dt*14
            if d['y']-d['ln']>self.rows:
                d['y']=random.uniform(-8,-1)
                d['spd']=random.uniform(0.4,1.8)
            if random.random()<0.08:
                d['chars'][random.randint(0,len(d['chars'])-1)]=random.random()
    def get_cells(self):
        cells=[]
        for col,d in enumerate(self.drops):
            head=int(d['y'])
            for i in range(d['ln']):
                row=head-i
                if 0<=row<self.rows:
                    cells.append((col,row,d['chars'][row%len(d['chars'])],1.0-i/d['ln']))
        return cells

class SineWave(Animation):
    def _init(self): self.t=0.0
    def update(self,dt,speed,trail=8,count=100,size=1.0):
        super().update(dt,speed,trail,count,size)
        self.t+=dt*speed
    def get_cells(self):
        cells=[]; t=self.t
        for w in range(3):
            freq=0.08+w*0.04; a=self.rows*0.35*((w+1)/3)*self.size
            phase=t*(2.0+w*0.7)+w*1.5
            for c in range(self.cols):
                y=self.rows/2+math.sin(c*freq+phase)*a*(.6+.4*math.sin(t*.3+w))
                for dr in range(-1,2):
                    r=int(y)+dr
                    if 0<=r<self.rows:
                        cells.append((c,r,(c/max(1,self.cols)+w/3+t*.1)%1.0,
                            (1.0-abs(dr)*.35)*(.5+.5*(1-w/3))))
        return cells

class SpiralVortex(Animation):
    def _init(self):
        self.t=0.0; self.pts=[]
        for _ in range(200):
            self.pts.append({'a':random.uniform(0,math.tau),
                'r':random.uniform(0,1),'spd':random.uniform(0.3,1.5)})
    def update(self,dt,speed,trail=8,count=100,size=1.0):
        super().update(dt,speed,trail,count,size)
        self.t+=dt*speed
        for p in self.pts[:max(10,count)]:
            p['a']+=p['spd']*speed*dt*1.5
            p['r']+=dt*speed*0.15
            if p['r']>1.2: p['r']=random.uniform(0,.1); p['a']=random.uniform(0,math.tau)
    def get_cells(self):
        cells=[]; cx,cy=self.cols/2,self.rows/2; mr=min(cx,cy)*.9*self.size
        for p in self.pts:
            x=cx+math.cos(p['a']+self.t*.5)*p['r']*mr*1.5
            y=cy+math.sin(p['a']+self.t*.5)*p['r']*mr
            c,r=int(x),int(y)
            if 0<=c<self.cols and 0<=r<self.rows:
                cells.append((c,r,(p['a']/math.tau+self.t*.05)%1.0,max(.1,1.0-p['r']*.7)))
        return cells

class BouncingParticles(Animation):
    def _init(self):
        self.pts=[]
        for _ in range(200):
            self.pts.append({'x':random.uniform(0,max(1,self.cols)),
                'y':random.uniform(0,max(1,self.rows)),
                'vx':random.uniform(-10,10),'vy':random.uniform(-10,10),
                'ci':random.random(),'trail':[]})
    def update(self,dt,speed,trail=8,count=100,amp=0.5):
        for p in self.pts[:max(5,count)]:
            p['x']+=p['vx']*speed*dt; p['y']+=p['vy']*speed*dt
            if p['x']<0: p['x']=0; p['vx']*=-1
            if p['x']>=self.cols: p['x']=self.cols-1; p['vx']*=-1
            if p['y']<0: p['y']=0; p['vy']*=-1
            if p['y']>=self.rows: p['y']=self.rows-1; p['vy']*=-1
            p['trail'].append((int(p['x']),int(p['y'])))
            while len(p['trail'])>trail: p['trail'].pop(0)
    def get_cells(self):
        cells=[]
        for p in self.pts:
            for i,(c,r) in enumerate(p['trail']):
                if 0<=c<self.cols and 0<=r<self.rows:
                    cells.append((c,r,p['ci'],(i+1)/max(1,len(p['trail']))*.5))
            c,r=int(p['x']),int(p['y'])
            if 0<=c<self.cols and 0<=r<self.rows:
                cells.append((c,r,p['ci'],1.0))
        return cells

class DriftingSnow(Animation):
    def _init(self):
        self.fl=[]
        for _ in range(300):
            self.fl.append({'x':random.uniform(0,max(1,self.cols)),
                'y':random.uniform(-self.rows,self.rows),
                'vy':random.uniform(1,4),'vx':random.uniform(-.5,.5),
                'ci':random.random(),'sz':random.uniform(.3,1.0)})
    def update(self,dt,speed,trail=8,count=100,amp=0.5):
        wind=math.sin(time.time()*.3)*2
        for f in self.fl[:max(10,count)]:
            f['y']+=f['vy']*speed*dt*6
            f['x']+=(f['vx']+wind*.3)*speed*dt*3
            f['x']+=math.sin(f['y']*.15+f['ci']*10)*dt*speed
            if f['y']>self.rows: f['y']=random.uniform(-3,-1); f['x']=random.uniform(0,max(1,self.cols))
            if f['x']<0: f['x']+=self.cols
            if f['x']>=self.cols: f['x']-=self.cols
    def get_cells(self):
        cells=[]
        for f in self.fl:
            c,r=int(f['x']),int(f['y'])
            if 0<=c<self.cols and 0<=r<self.rows:
                cells.append((c,r,f['ci'],f['sz']))
        return cells

class CellularAutomata(Animation):
    def _init(self):
        self.grid=[[random.random()<.3 for _ in range(self.cols)] for _ in range(self.rows)]
        self.age=[[0]*self.cols for _ in range(self.rows)]; self.acc=0.0
    def update(self,dt,speed,trail=8,count=100,amp=0.5):
        self.acc+=dt*speed*5.0
        while self.acc>=1.0: self.acc-=1.0; self._step()
    def _step(self):
        ng=[[False]*self.cols for _ in range(self.rows)]
        na=[[0]*self.cols for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                n=sum(self.grid[(r+dr)%self.rows][(c+dc)%self.cols]
                    for dr in(-1,0,1) for dc in(-1,0,1) if(dr,dc)!=(0,0))
                if self.grid[r][c]: ng[r][c]=n in(2,3)
                else: ng[r][c]=n==3
                if ng[r][c]: na[r][c]=self.age[r][c]+1
        if random.random()<.15:
            for _ in range(max(1,self.cols*self.rows//200)):
                ng[random.randint(0,self.rows-1)][random.randint(0,self.cols-1)]=True
        self.grid,self.age=ng,na
    def get_cells(self):
        cells=[]
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c]:
                    t=min(1.0,self.age[r][c]/20.0)
                    cells.append((c,r,(self.age[r][c]*.05)%1.0,.3+.7*(1.0-t)))
        return cells

class WarpTunnel(Animation):
    def _init(self):
        self.stars=[self._ns() for _ in range(300)]
    def _ns(self):
        return{'x':random.uniform(-1.5,1.5),'y':random.uniform(-1.5,1.5),
               'z':random.uniform(.5,8),'ci':random.random()}
    def update(self,dt,speed,trail=8,count=100,size=1.0):
        super().update(dt,speed,trail,count,size)
        for s in self.stars:
            s['z']-=speed*dt*4.0
            if s['z']<.1: s.update(self._ns()); s['z']=random.uniform(5,8)
    def get_cells(self):
        cells=[]; cx,cy=self.cols/2,self.rows/2
        for s in self.stars:
            if s['z']<=.1: continue
            sx=cx+s['x']/s['z']*cx*1.5; sy=cy+s['y']/s['z']*cy
            c,r=int(sx),int(sy)
            if 0<=c<self.cols and 0<=r<self.rows:
                cells.append((c,r,s['ci'],max(.1,1.0-s['z']/8.0)))
        return cells

ANIM_CLASSES=[MatrixRain,SineWave,SpiralVortex,BouncingParticles,
              DriftingSnow,CellularAutomata,WarpTunnel]

class Layer:
    def __init__(self,ai=0,cs="classic",pal="matrix",spd=1.0,opa=255,trail=8,count=100,size=1.0):
        self.anim_idx=ai; self.charset=cs; self.palette=pal
        self.speed=spd; self.opacity=opa; self.trail=trail; self.count=count; self.size=size
        self.anim=ANIM_CLASSES[ai]()
    def set_anim(self,i): self.anim_idx=i; self.anim=ANIM_CLASSES[i]()
    def to_dict(self):
        return{'ai':self.anim_idx,'cs':self.charset,'pal':self.palette,
               'spd':self.speed,'opa':self.opacity,'trail':self.trail,'count':self.count,'sz':self.size}
    @staticmethod
    def from_dict(d):
        return Layer(d.get('ai',0),d.get('cs','classic'),d.get('pal','matrix'),
                     d.get('spd',1.0),d.get('opa',255),d.get('trail',8),d.get('count',100),d.get('sz',1.0))


class App:
    def __init__(self):
        info=pygame.display.Info()
        self.ww=int(info.current_w*.82); self.wh=int(info.current_h*.82)
        self.screen=pygame.display.set_mode((self.ww,self.wh),pygame.RESIZABLE)
        pygame.display.set_caption("SCREENER: ASCII Screensaver Maker")
        self.clock=pygame.time.Clock(); self.running=True; self.mode='edit'
        self.font_name=MONO_FONT
        self.ui_font=load_font(UI_FS)
        self.cw=self.ui_font.size("A")[0]; self.ch_=self.ui_font.get_height()
        self.afs=DEF_F; self.af=load_font(DEF_F)
        self.acw=self.af.size("A")[0]; self.ach=self.af.get_height()
        self.layers=[Layer()]; self.sel=0
        self.drag=None; self.finput=None; self.itxt=""
        self.bg_idx=0; self.color_cycle=False; self.cycle_t=0.0
        self.fs_w=info.current_w; self.fs_h=info.current_h
        self._sl=[]; self._ar={}; self._cr={}; self._pr={}; self._lr={}; self._br={}
        self._cir=None
        self._bgr={}; self._ccr=None
        self.pal_offset = 0

    def run(self):
        while self.running:
            dt=min(self.clock.tick(FPS)/1000.0,.05)
            if self.mode=='edit': self._ee(); self._ue(dt); self._re()
            else: self._es(); self._us(dt); self._rs()
            pygame.display.flip()
        pygame.quit()

    def _cl(self):
        return self.layers[self.sel] if 0<=self.sel<len(self.layers) else None

    def _rbf(self):
        self.af=load_font(self.afs)
        self.acw=self.af.size("A")[0]; self.ach=self.af.get_height()
        self.ui_font=load_font(UI_FS)
        self.cw=self.ui_font.size("A")[0]; self.ch_=self.ui_font.get_height()
        _cc_clear()

    def _lo(self):
        w,h=self.screen.get_size()
        lw=max(220,int(w*.22)); rw=max(220,int(w*.22)); cw_=w-lw-rw
        return{'lx':0,'lw':lw,'cx':lw,'cw':cw_,'rx':lw+cw_,'rw':rw,
               'w':w,'h':h,'pw':cw_-20,'ph':int(h*.52)}

    def _dp(self,s,x,y,w,h,t="",c=C_BORDER):
        pygame.draw.rect(s,C_PANEL,(x,y,w,h)); pygame.draw.rect(s,c,(x,y,w,h),1)
        if t:
            ts=self.ui_font.render(f" {t} ",True,C_HI)
            pygame.draw.line(s,C_PANEL,(x+10,y),(x+12+ts.get_width(),y))
            s.blit(ts,(x+11,y-self.ch_//2))

    def _dt(self,s,t,x,y,c=C_TEXT):
        r=self.ui_font.render(str(t),True,c); s.blit(r,(x,y)); return r.get_width()

    def _db(self,s,t,x,y,w,h,hov=False,tc=C_TEXT):
        pygame.draw.rect(s,C_BTN_H if hov else C_BTN,(x,y,w,h),border_radius=3)
        pygame.draw.rect(s,C_DIM,(x,y,w,h),1,border_radius=3)
        ts=self.ui_font.render(t,True,tc)
        s.blit(ts,(x+(w-ts.get_width())//2,y+(h-ts.get_height())//2))

    def _ds(self,s,lbl,x,y,w,val,vmin,vmax,key):
        self._dt(s,lbl,x,y,C_TEXT)
        by=y+self.ch_+2; bh=14; fr=(val-vmin)/max(.001,vmax-vmin)
        pygame.draw.rect(s,C_SL_BG,(x,by,w,bh),border_radius=4)
        fw=int(fr*w)
        if fw>0: pygame.draw.rect(s,C_SL_FG,(x,by,fw,bh),border_radius=4)
        pygame.draw.circle(s,C_HI,(x+fw,by+bh//2),7)
        vt=f"{val:.1f}" if isinstance(val,float) else str(int(val))
        self._dt(s,vt,x+w+8,by-2,C_ACCENT)
        return(x,by,w,bh,vmin,vmax,key)

    def _sh(self,si,mx,my):
        return si[0]<=mx<=si[0]+si[2] and si[1]-4<=my<=si[1]+si[3]+4

    def _sv(self,si,mx):
        return si[4]+max(0,min(1,(mx-si[0])/si[2]))*(si[5]-si[4])

    def _ee(self):
        mx,my=pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: self.running=False
            elif ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_ESCAPE: self.running=False
                elif self.finput=='charset':
                    if ev.key==pygame.K_BACKSPACE: self.itxt=self.itxt[:-1]
                    elif ev.key==pygame.K_RETURN:
                        self.finput=None
                        if self.itxt:
                            CHAR_SETS['custom']=self.itxt
                            if 'custom' not in CS_NAMES: CS_NAMES.append('custom')
                            L=self._cl()
                            if L: L.charset='custom'
                    elif ev.unicode and ev.unicode.isprintable(): self.itxt+=ev.unicode
            elif ev.type==pygame.MOUSEBUTTONDOWN:
                if ev.button==1: self._hc(mx,my)
                elif ev.button==4: self.pal_offset=max(0,self.pal_offset-1)
                elif ev.button==5: self.pal_offset=min(len(PAL_NAMES)-10,self.pal_offset+1)
            elif ev.type==pygame.MOUSEBUTTONUP: self.drag=None
            elif ev.type==pygame.MOUSEMOTION and self.drag: self._hd(mx,my)
            elif ev.type==pygame.VIDEORESIZE: self.ww,self.wh=ev.w,ev.h

    def _hc(self,mx,my):
        L=self._cl(); self.finput=None
        for si in self._sl:
            if self._sh(si,mx,my): self.drag=si; self._hd(mx,my); return
        for i,r in self._ar.items():
            if r.collidepoint(mx,my) and L: L.set_anim(i); return
        for n,r in self._cr.items():
            if r.collidepoint(mx,my) and L: L.charset=n; return
        for n,r in self._pr.items():
            if r.collidepoint(mx,my) and L: L.palette=n; return
        for i,r in self._lr.items():
            if r.collidepoint(mx,my): self.sel=i; return
        for n,r in self._br.items():
            if r.collidepoint(mx,my): self._ba(n); return
        for n,r in self._bgr.items():
            if r.collidepoint(mx,my): self.bg_idx=BG_NAMES.index(n); return
        if self._cir and self._cir.collidepoint(mx,my): self.finput='charset'; return
        if self._ccr and self._ccr.collidepoint(mx,my): self.color_cycle=not self.color_cycle; return

    def _hd(self,mx,my):
        if not self.drag: return
        val=self._sv(self.drag,mx); k=self.drag[6]; L=self._cl()
        if k=='speed' and L: L.speed=round(val,2)
        elif k=='opacity' and L: L.opacity=int(val)
        elif k=='trail' and L: L.trail=int(val)
        elif k=='count' and L: L.count=int(val)
        elif k=='font_size':
            ns=int(val)
            if ns!=self.afs: self.afs=ns; self._rbf()
        elif k=='anim_size' and L: L.size=round(val,2)

    def _ba(self,n):
        if n=='play': self._ess()
        elif n=='add': self.layers.append(Layer()); self.sel=len(self.layers)-1
        elif n=='del':
            if len(self.layers)>1: self.layers.pop(self.sel); self.sel=min(self.sel,len(self.layers)-1)
        elif n=='rand': self._rnd()
        elif n=='save': self._sav()
        elif n=='load': self._ld()

    def _rnd(self):
        L=self._cl()
        if not L: return
        L.set_anim(random.randint(0,len(ANIM_CLASSES)-1))
        L.charset=random.choice(CS_NAMES); L.palette=random.choice(PAL_NAMES)
        L.speed=round(random.uniform(.3,2.5),2); L.opacity=random.randint(150,255)
        L.trail=random.randint(3,15); L.count=random.randint(30,250)
        self.afs=random.choice([12,14,16,18,20]); self._rbf()

    def _sav(self):
        d={'layers':[l.to_dict() for l in self.layers],'fs':self.afs,
           'bg':self.bg_idx,'cc':self.color_cycle}
        try:
            with open(SAVE_FILE,'w') as f: json.dump(d,f,indent=2)
        except Exception as e: print(f"Save err: {e}")

    def _ld(self):
        try:
            with open(SAVE_FILE) as f: d=json.load(f)
            self.layers=[Layer.from_dict(x) for x in d.get('layers',[{}])]
            if not self.layers: self.layers=[Layer()]
            self.sel=0; self.afs=d.get('fs',DEF_F)
            self._rbf()
            self.bg_idx=d.get('bg',0); self.color_cycle=d.get('cc',False)
        except Exception as e: print(f"Load err: {e}")

    def _ue(self,dt):
        lo=self._lo()
        pc=max(1,(lo['pw']-4)//max(1,self.acw)); pr=max(1,(lo['ph']-4)//max(1,self.ach))
        for layer in self.layers:
            layer.anim.resize(pc,pr)
            layer.anim.update(dt,layer.speed,layer.trail,layer.count,layer.size)
        if self.color_cycle: self.cycle_t+=dt*.3

    def _render_anim(self,surf,cols,rows,bg):
        surf.fill(bg)
        used=set()
        for layer in self.layers:
            if layer.opacity<=0: continue
            cells=layer.anim.get_cells()
            cs=CHAR_SETS.get(layer.charset,CHAR_SETS['classic'])
            pal=COLOR_PALETTES.get(layer.palette,list(COLOR_PALETTES.values())[0])
            if self.color_cycle:
                shift=self.cycle_t%1.0
                pal=pal[int(shift*len(pal)):]+pal[:int(shift*len(pal))]
            bri=layer.opacity/255.0
            for col,row,ci,intensity in cells:
                if col<0 or col>=cols or row<0 or row>=rows: continue
                if (col,row) in used: continue
                used.add((col,row))
                if isinstance(ci,str): ch=ci; cidx=.5
                else: ch=cs[int(ci*len(cs))%len(cs)]; cidx=ci
                pc_=palc(pal,cidx); fc=sc(pc_,bri*intensity)
                if fc[0]+fc[1]+fc[2]<8: continue
                surf.blit(rc(self.af,ch,fc),(col*self.acw,row*self.ach))

    def _re(self):
        s=self.screen; s.fill(C_BG); lo=self._lo(); mx,my=pygame.mouse.get_pos()
        self._sl=[]; self._ar={}; self._cr={}; self._pr={}
        self._lr={}; self._br={}; self._bgr={}
        L=self._cl(); lx=lo['lx']+6; pw=lo['lw']-12
        ly = 8
        s.set_clip(pygame.Rect(0,0,lo['lw'],lo['h']))

        self._dp(s,lx,ly,pw,len(ANIM_NAMES)*(self.ch_+2)+30,"ANIMATION")
        iy=ly+14
        for i,nm in enumerate(ANIM_NAMES):
            r=pygame.Rect(lx+2,iy,pw-4,self.ch_+1); self._ar[i]=r
            sel=L and L.anim_idx==i; hov=r.collidepoint(mx,my)
            if sel: pygame.draw.rect(s,C_ACTIVE,r)
            elif hov: pygame.draw.rect(s,C_HOVER,r)
            self._dt(s,("▸ " if sel else "  ")+nm,lx+6,iy,C_ACCENT if sel else(C_HI if hov else C_TEXT))
            iy+=self.ch_+2

        cy=iy+10
        self._dp(s,lx,cy,pw,len(CS_NAMES)*(self.ch_+2)+48,"CHARSET")
        iy=cy+14
        for nm in CS_NAMES:
            r=pygame.Rect(lx+2,iy,pw-4,self.ch_+1); self._cr[nm]=r
            sel=L and L.charset==nm; hov=r.collidepoint(mx,my)
            if sel: pygame.draw.rect(s,C_ACTIVE,r)
            elif hov: pygame.draw.rect(s,C_HOVER,r)
            self._dt(s,("▸ " if sel else "  ")+nm,lx+6,iy,C_ACCENT if sel else C_TEXT)
            iy+=self.ch_+2
        iy+=2; self._dt(s,"Custom:",lx+6,iy,C_DIM); iy+=self.ch_
        ir=pygame.Rect(lx+6,iy,pw-16,self.ch_+4); self._cir=ir
        pygame.draw.rect(s,(20,20,30),ir)
        pygame.draw.rect(s,C_ACCENT if self.finput=='charset' else C_DIM,ir,1)
        d=self.itxt[-20:] if len(self.itxt)>20 else self.itxt
        if self.finput=='charset': d+="│"
        self._dt(s,d,ir.x+3,ir.y+2,C_HI)

        py_=iy+self.ch_+14
        vis_pal=12
        pal_h=vis_pal*(self.ch_+4)+26
        self._dp(s,lx,py_,pw,pal_h,"PALETTE (scroll)")
        iy=py_+14
        for nm in PAL_NAMES[self.pal_offset:self.pal_offset+vis_pal]:
            r=pygame.Rect(lx+2,iy,pw-4,self.ch_+3); self._pr[nm]=r
            sel=L and L.palette==nm; hov=r.collidepoint(mx,my)
            if sel: pygame.draw.rect(s,C_ACTIVE,r)
            elif hov: pygame.draw.rect(s,C_HOVER,r)
            cols_=COLOR_PALETTES[nm]; sw_=min(8,(pw-120)//max(1,len(cols_)))
            for j,c_ in enumerate(cols_):
                pygame.draw.rect(s,c_,(lx+8+j*sw_,iy+2,sw_-1,self.ch_-2))
            self._dt(s,f" {'▸' if sel else ' '} {nm}",lx+8+len(cols_)*sw_+2,iy,
                     C_ACCENT if sel else C_TEXT)
            iy+=self.ch_+4
        s.set_clip(None)

        px,p_y=lo['cx']+10,8; pw_p,ph_p=lo['pw'],lo['ph']
        self._dp(s,px,p_y,pw_p,ph_p+6,"PREVIEW")
        ps=pygame.Surface((pw_p-4,ph_p-4))
        pc=max(1,(pw_p-4)//max(1,self.acw)); pr=max(1,(ph_p-4)//max(1,self.ach))
        bg=BG_COLORS[BG_NAMES[self.bg_idx]]
        self._render_anim(ps,pc,pr,bg)
        s.blit(ps,(px+2,p_y+2))

        sy=p_y+ph_p+16; sl_w=lo['cw']-80
        if L:
            self._sl.append(self._ds(s,"Speed",px+10,sy,sl_w,L.speed,.1,3.0,'speed'))
            sy+=self.ch_+22
            is_particle = L.anim_idx in [0, 3, 4, 6]
            is_wave = L.anim_idx in [1, 2]
            
            if L.anim_idx in [0, 3]:
                self._sl.append(self._ds(s,"Trail Length",px+10,sy,sl_w,L.trail,1,20,'trail'))
                sy+=self.ch_+22
            
            if L.anim_idx in [0, 2, 3, 4, 6]:
                self._sl.append(self._ds(s,"Particle Count",px+10,sy,sl_w,L.count,10,300,'count'))
                sy+=self.ch_+22
            if is_wave:
                self._sl.append(self._ds(s,"Effect Size",px+10,sy,sl_w,L.size,.1,3.0,'anim_size'))
                sy+=self.ch_+22
            self._sl.append(self._ds(s,"Layer Opacity",px+10,sy,sl_w,L.opacity,0,255,'opacity'))
            sy+=self.ch_+22
            
        self._sl.append(self._ds(s,"Global Font Size",px+10,sy,sl_w,self.afs,MIN_F,MAX_F,'font_size'))

        s.set_clip(pygame.Rect(lo['rx'],0,lo['rw'],lo['h']))
        rx=lo['rx']+6; rw=lo['rw']-12; ry=8
        lp_h=len(self.layers)*(self.ch_+2)+50
        self._dp(s,rx,ry,rw,lp_h,"LAYERS")
        iy=ry+14
        for i,la in enumerate(self.layers):
            r=pygame.Rect(rx+2,iy,rw-4,self.ch_+1); self._lr[i]=r
            sel=i==self.sel; hov=r.collidepoint(mx,my)
            if sel: pygame.draw.rect(s,C_ACTIVE,r)
            elif hov: pygame.draw.rect(s,C_HOVER,r)
            an=ANIM_NAMES[la.anim_idx] if la.anim_idx<len(ANIM_NAMES) else "?"
            self._dt(s,f"{'▸ ' if sel else '  '}L{i+1}: {an}",rx+6,iy,C_ACCENT if sel else C_TEXT)
            iy+=self.ch_+2
        iy+=4; bw=(rw-16)//2
        br1=pygame.Rect(rx+4,iy,bw,self.ch_+6); self._br['add']=br1
        self._db(s,"+ Add",br1.x,br1.y,br1.w,br1.h,br1.collidepoint(mx,my),C_ACCENT)
        br2=pygame.Rect(rx+8+bw,iy,bw,self.ch_+6); self._br['del']=br2
        self._db(s,"- Del",br2.x,br2.y,br2.w,br2.h,br2.collidepoint(mx,my),C_DANGER)

        oy=ry+lp_h+14
        self._dp(s,rx,oy,rw,self.ch_*4+70,"OPTIONS")
        iy=oy+14
        ccr=pygame.Rect(rx+6,iy,rw-16,self.ch_+2); self._ccr=ccr
        self._dt(s,f"{'☑' if self.color_cycle else '☐'} Color Cycle",rx+8,iy,
                C_ACCENT if self.color_cycle else C_TEXT); iy+=self.ch_+8
        self._dt(s,"Background:",rx+8,iy,C_DIM); iy+=self.ch_
        for i,bn in enumerate(BG_NAMES):
            if iy>oy+self.ch_*4+60: break
            r=pygame.Rect(rx+8,iy,rw-20,self.ch_+1); self._bgr[bn]=r
            sel=i==self.bg_idx; hov=r.collidepoint(mx,my)
            if sel: pygame.draw.rect(s,C_ACTIVE,r)
            elif hov: pygame.draw.rect(s,C_HOVER,r)
            pygame.draw.rect(s,BG_COLORS[bn],(rx+10,iy+2,12,self.ch_-4))
            pygame.draw.rect(s,C_DIM,(rx+10,iy+2,12,self.ch_-4),1)
            self._dt(s,f" {bn}",rx+24,iy,C_ACCENT if sel else C_TEXT)
            iy+=self.ch_+2


        by_=oy+self.ch_*4+84; bh=self.ch_+8
        for lbl,key in[("Randomize",'rand'),("Save",'save'),("Load",'load')]:
            br=pygame.Rect(rx+8,by_,rw-20,bh); self._br[key]=br
            self._db(s,lbl,br.x,br.y,br.w,br.h,br.collidepoint(mx,my)); by_+=bh+4
        by_+=4; br=pygame.Rect(rx+8,by_,rw-20,bh+6); self._br['play']=br
        hov=br.collidepoint(mx,my); pc_=(0,255,120) if hov else C_PLAY
        pygame.draw.rect(s,(10,40,20),br,border_radius=4)
        pygame.draw.rect(s,pc_,br,2,border_radius=4)
        ts=self.ui_font.render("PLAY",True,pc_)
        s.blit(ts,(br.x+(br.w-ts.get_width())//2,br.y+(br.h-ts.get_height())//2))
        s.set_clip(None)

    def _ess(self):
        self.mode='screensaver'
        self.screen=pygame.display.set_mode((self.fs_w,self.fs_h),pygame.FULLSCREEN)
        _cc_clear()

    def _xss(self):
        self.mode='edit'
        self.screen=pygame.display.set_mode((self.ww,self.wh),pygame.RESIZABLE)
        _cc_clear()

    def _es(self):
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: self.running=False
            elif ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_ESCAPE: self.running=False
                else: self._xss()
            elif ev.type==pygame.MOUSEBUTTONDOWN: self._xss()

    def _us(self,dt):
        w,h=self.screen.get_size()
        sc_=max(1,w//max(1,self.acw)); sr=max(1,h//max(1,self.ach))
        for la in self.layers:
            la.anim.resize(sc_,sr); la.anim.update(dt,la.speed,la.trail,la.count,la.size)
        if self.color_cycle: self.cycle_t+=dt*.3

    def _rs(self):
        s=self.screen; w,h=s.get_size()
        sc_=max(1,w//max(1,self.acw)); sr=max(1,h//max(1,self.ach))
        bg=BG_COLORS[BG_NAMES[self.bg_idx]]
        self._render_anim(s,sc_,sr,bg)

if __name__=='__main__':
    App().run()
