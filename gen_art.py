"""
Hand-authored pixel art generator for Finding No-No-Namosh II.
Every sprite is defined as a grid of named color-cells (classic pixel-art
authoring, just done via arrays instead of a mouse), then auto-outlined
(the standard pixel-art technique: silhouette gets a 1px dark border) and
upscaled with nearest-neighbor so it stays crisp/pixelated at game scale.
No AI image generation is used or available here -- every pixel placement
below is explicit.
"""
from PIL import Image
import os

OUT = "/home/claude/nonamosh2/assets"
os.makedirs(OUT, exist_ok=True)

SCALE = 3  # each "art pixel" becomes SCALE x SCALE real pixels

def render_grid(grid, palette, outline_color=(20,14,10,255)):
    """grid: list of rows, each row a list of palette keys or None (transparent).
       Returns an upscaled RGBA image with automatic silhouette outline."""
    h = len(grid); w = len(grid[0])
    base = Image.new("RGBA", (w, h), (0,0,0,0))
    px = base.load()
    filled = set()
    for y,row in enumerate(grid):
        for x,key in enumerate(row):
            if key is not None:
                px[x,y] = palette[key]
                filled.add((x,y))
    # outline pass: any empty neighbor of a filled cell becomes outline color
    outline_img = Image.new("RGBA", (w, h), (0,0,0,0))
    opx = outline_img.load()
    for (x,y) in filled:
        for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx,ny = x+dx,y+dy
            if 0<=nx<w and 0<=ny<h and (nx,ny) not in filled:
                opx[nx,ny] = outline_color
    combined = Image.new("RGBA",(w,h),(0,0,0,0))
    combined.alpha_composite(outline_img)
    combined.alpha_composite(base)
    return combined.resize((w*SCALE, h*SCALE), Image.NEAREST)

def blank(w,h):
    return [[None]*w for _ in range(h)]

def rect(grid, x0,y0,x1,y1,key):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if 0<=y<len(grid) and 0<=x<len(grid[0]):
                grid[y][x]=key

def mirror_h(grid):
    return [list(reversed(row)) for row in grid]

# ============================================================
# AYA  -- grid 12 wide x 16 tall per frame
# Palette per description: black hijab, beige/taupe cardigan,
# white inner shirt, dark navy jeans, black shoes, maroon satchel,
# fair skin, must read clearly against environments.
# ============================================================
AYA_PAL = {
    'hijab':(24,22,26,255), 'hijab_sh':(14,13,16,255),
    'skin':(247,214,181,255), 'skin_sh':(226,185,148,255),
    'eye':(35,28,24,255),
    'cardigan':(196,168,120,255), 'cardigan_sh':(163,136,92,255),
    'shirt':(240,238,230,255),
    'jeans':(31,41,74,255), 'jeans_sh':(20,27,52,255),
    'shoe':(18,16,18,255),
    'satchel':(110,32,32,255), 'satchel_sh':(80,20,20,255),
}

def aya_frame(direction, walk_phase):
    """walk_phase: 0=stand, 1=leg A fwd, 2=stand, 3=leg B fwd.
       Grid is 14 wide x 20 tall for clearer anatomy."""
    g = blank(14,20)

    # --- hijab: rounded top + drape covering shoulders ---
    rect(g,4,0,9,0,'hijab')
    rect(g,3,1,10,2,'hijab')
    rect(g,2,3,11,5,'hijab')
    rect(g,1,5,3,9,'hijab'); rect(g,10,5,12,9,'hijab')   # drape sides to shoulder
    rect(g,1,8,3,9,'hijab_sh'); rect(g,10,8,12,9,'hijab_sh')
    rect(g,2,9,11,9,'hijab_sh')

    # --- face / back of head ---
    if direction=='down':
        rect(g,4,4,9,7,'skin')
        rect(g,4,7,9,7,'skin_sh')
        g[5][4]='eye'; g[5][8]='eye'
    elif direction=='up':
        rect(g,3,3,10,8,'hijab')  # fully covered from behind
        rect(g,3,8,10,8,'hijab_sh')
    else:  # left / right profile
        rect(g,5,4,9,7,'skin')
        rect(g,5,7,9,7,'skin_sh')
        eye_x = 6
        g[5][eye_x]='eye'
        g[6][7]='skin_sh'  # small nose bump

    # --- torso: cardigan over shirt ---
    rect(g,2,10,11,15,'cardigan')
    rect(g,2,15,11,15,'cardigan_sh')
    rect(g,2,10,2,15,'cardigan_sh'); rect(g,11,10,11,15,'cardigan_sh')  # side shading
    rect(g,6,10,7,13,'shirt')  # open collar strip

    # --- arms (subtle sway between phases) ---
    sway = 1 if walk_phase in (1,3) else 0
    rect(g,1,11,1,14+ (0 if walk_phase!=1 else 1),'cardigan')
    rect(g,12,11,12,14+ (0 if walk_phase!=3 else 1),'cardigan')

    # --- satchel (maroon cross-body bag) ---
    if direction=='right':
        rect(g,2,11,3,14,'satchel'); g[14][2]='satchel_sh'
    elif direction=='left':
        rect(g,10,11,11,14,'satchel'); g[14][11]='satchel_sh'
    else:
        rect(g,9,12,10,14,'satchel'); g[14][10]='satchel_sh'

    # --- legs: jeans, animated via forward/back offset ---
    lift_a = 1 if walk_phase==1 else 0
    lift_b = 1 if walk_phase==3 else 0
    rect(g,4,16,6,18-lift_a,'jeans')
    rect(g,4,18-lift_a,6,18-lift_a,'jeans_sh')
    rect(g,7,16,9,18-lift_b,'jeans')
    rect(g,7,18-lift_b,9,18-lift_b,'jeans_sh')
    rect(g,4,18-lift_a,6,19-lift_a,'shoe')
    rect(g,7,18-lift_b,9,19-lift_b,'shoe')

    if direction=='right':
        g = mirror_h(g)
    return render_grid(g, AYA_PAL)

# ============================================================
# NAMOSH -- black & white cat. grid 12 wide x 8 tall per frame.
# ============================================================
NAMOSH_PAL = {
    'black':(20,20,22,255), 'black_sh':(10,10,12,255),
    'white':(244,244,240,255), 'white_sh':(214,214,208,255),
    'eye':(232,196,64,255), 'nose':(224,140,168,255),
}

def namosh_frame(direction, walk_phase):
    """Side-view quadruped silhouette (used for left/right and reused,
       mirrored/compressed, for down/up), grid 18 wide x 12 tall."""
    g = blank(18,12)

    if direction in ('left','right'):
        # tail (curls up at the back)
        rect(g,15,3,16,3,'black'); rect(g,16,2,17,2,'black'); rect(g,16,1,16,1,'black')
        # body (black back, white belly)
        rect(g,4,3,15,7,'black')
        rect(g,5,6,14,8,'white')
        rect(g,5,8,14,8,'white_sh')
        # head
        rect(g,1,1,7,6,'black')
        rect(g,1,4,6,7,'white')      # muzzle/chin
        # ears
        rect(g,1,0,2,1,'black'); rect(g,5,0,6,1,'black')
        # face details
        g[3][3]='eye'
        g[4][2]='nose'
        # legs, animated: front pair + back pair alternate
        step = 1 if walk_phase in (1,3) else 0
        back_step = 1 - step
        rect(g,5,9,6,11-step,'black')
        rect(g,5,11-step,6,11-step,'white')
        rect(g,12,9,13,11-back_step,'black')
        rect(g,12,11-back_step,13,11-back_step,'white')
        rect(g,8,9,9,11-back_step,'white')
        rect(g,10,9,11,11-step,'white')
    else:
        # simplified front/back view: compact chibi top-down cat
        rect(g,3,4,14,10,'black')      # rounded body
        rect(g,5,7,12,10,'white')      # belly
        rect(g,2,1,6,4,'black'); rect(g,11,1,15,4,'black')  # ears (triangular block)
        rect(g,3,2,5,3,'white_sh')  if False else None
        if direction=='down':
            g[6][7]='eye'; g[6][10]='eye'; g[7][8]='nose'; g[7][9]='nose'
        step = 1 if walk_phase in (1,3) else 0
        rect(g,5,10,7,11-step,'white')
        rect(g,10,10,12,11-(1-step),'white')

    if direction=='right':
        g = mirror_h(g)
    return render_grid(g, NAMOSH_PAL)

# ============================================================
# TILESET -- 16x16 art-pixel tiles (i.e. 1 art-pixel == 1 tile-pixel here,
# rendered directly at higher internal detail via a finer sub-grid).
# ============================================================
def make_tile(grid16, palette):
    return render_grid(grid16, palette, outline_color=(0,0,0,0))  # no outline for terrain

def grass_tile(variant=0):
    g = blank(16,16)
    rect(g,0,0,15,15,'base')
    blades = [(2,2),(5,4),(9,3),(12,6),(3,9),(7,11),(11,10),(14,13),(1,13),(6,7)]
    if variant: blades = [(x+1,y+2) for x,y in blades]
    for (x,y) in blades:
        if 0<=x<16 and 0<=y<16: g[y][x]='blade'
    pal = {'base':(90,181,96,255) if not variant else (84,174,90,255), 'blade':(66,150,72,255)}
    return make_tile(g,pal)

def water_tile(frame=0):
    g = blank(16,16)
    rect(g,0,0,15,15,'base')
    wave_rows = [3,9] if frame==0 else [5,11]
    for wy in wave_rows:
        rect(g,0,wy,15,wy,'wave')
    pal = {'base':(38,120,196,255),'wave':(120,196,232,255)}
    return make_tile(g,pal)

def path_tile():
    g = blank(16,16); rect(g,0,0,15,15,'base')
    for (x,y) in [(2,3),(9,2),(5,8),(12,10),(3,13),(13,5)]:
        g[y][x]='pebble'
    pal={'base':(196,168,112,255),'pebble':(168,138,88,255)}
    return make_tile(g,pal)

def wall_tile():
    g = blank(16,16); rect(g,0,0,15,15,'stone')
    for y in range(0,16,4):
        for x in range(0,16,8):
            ox = 4 if (y//4)%2 else 0
            rect(g,(x+ox)%16,y,min((x+ox)%16+6,15),y,'mortar')
    pal={'stone':(74,68,86,255),'mortar':(52,48,62,255)}
    return make_tile(g,pal)

def wood_tile():
    g = blank(16,16); rect(g,0,0,15,15,'plank')
    for x in range(0,16,4): rect(g,x,0,x,15,'seam')
    pal={'plank':(150,108,66,255),'seam':(122,86,50,255)}
    return make_tile(g,pal)

def sand_tile():
    g = blank(16,16); rect(g,0,0,15,15,'base')
    for (x,y) in [(3,4),(10,7),(6,11),(13,2),(1,9)]:
        g[y][x]='speck'
    pal={'base':(224,204,150,255),'speck':(202,180,126,255)}
    return make_tile(g,pal)

def crystal_water_tile(frame=0):
    g = blank(16,16); rect(g,0,0,15,15,'base')
    rows = [2,7,12] if frame==0 else [4,9,14]
    for r in rows: rect(g,0,r,15,r,'shine')
    pal={'base':(70,214,201,255),'shine':(180,246,238,255)}
    return make_tile(g,pal)

def grotto_floor_tile():
    g = blank(16,16); rect(g,0,0,15,15,'base')
    for (x,y) in [(2,2),(9,5),(5,10),(12,13)]: g[y][x]='fleck'
    pal={'base':(58,74,36,255),'fleck':(78,98,48,255)}
    return make_tile(g,pal)

def fence_tile():
    g = blank(16,16)
    rect(g,1,4,14,6,'rail'); rect(g,1,10,14,12,'rail')
    rect(g,2,1,3,15,'post'); rect(g,11,1,12,15,'post')
    pal={'rail':(150,108,66,255),'post':(108,76,44,255)}
    return make_tile(g,pal)

def rug_tile():
    g = blank(16,16); rect(g,0,0,15,15,'base')
    rect(g,2,2,13,13,'inner'); rect(g,4,4,11,11,'core')
    pal={'base':(150,42,42,255),'inner':(178,60,52,255),'core':(150,42,42,255)}
    return make_tile(g,pal)

def dark_stone_tile():
    g = blank(16,16); rect(g,0,0,15,15,'base')
    for (x,y) in [(2,3),(9,2),(5,8),(12,10)]: g[y][x]='fleck'
    pal={'base':(38,46,74,255),'fleck':(52,62,92,255)}
    return make_tile(g,pal)

def door_tile():
    g = blank(16,16); rect(g,3,1,12,15,'frame'); rect(g,5,3,10,15,'door')
    pal={'frame':(60,42,24,255),'door':(255,207,92,255)}
    return make_tile(g,pal)

def void_tile():
    g = blank(16,16); rect(g,0,0,15,15,'v')
    return make_tile(g,{'v':(13,18,32,255)})


def build_sheet(images, cols):
    if not images: return Image.new("RGBA",(1,1))
    w,h = images[0].size
    rows = (len(images)+cols-1)//cols
    sheet = Image.new("RGBA",(w*cols,h*rows),(0,0,0,0))
    for i,im in enumerate(images):
        x = (i%cols)*w; y=(i//cols)*h
        sheet.paste(im,(x,y),im)
    return sheet, (w,h)

def main():
    # --- Aya spritesheet: rows = directions [down,up,left,right], cols = 4 walk frames
    directions = ['down','up','left','right']
    aya_frames = []
    for d in directions:
        for phase in range(4):
            aya_frames.append(aya_frame(d,phase))
    sheet,fs = build_sheet(aya_frames, 4)
    sheet.save(f"{OUT}/aya_spritesheet.png")
    print("aya frame size", fs, "sheet", sheet.size)

    namosh_frames = []
    for d in directions:
        for phase in range(4):
            namosh_frames.append(namosh_frame(d,phase))
    sheet2, fs2 = build_sheet(namosh_frames, 4)
    sheet2.save(f"{OUT}/namosh_spritesheet.png")
    print("namosh frame size", fs2, "sheet", sheet2.size)

    # --- Tileset: fixed index order matching game TILE_MAP legend
    tiles = [
        grass_tile(0), grass_tile(1),      # 0 grass, 1 grass variant
        water_tile(0), water_tile(1),      # 2,3 water anim
        path_tile(),                       # 4
        wall_tile(),                       # 5
        wood_tile(),                       # 6
        sand_tile(),                       # 7
        crystal_water_tile(0), crystal_water_tile(1),  # 8,9
        grotto_floor_tile(),               # 10
        fence_tile(),                      # 11
        rug_tile(),                        # 12
        dark_stone_tile(),                 # 13
        door_tile(),                       # 14
        void_tile(),                       # 15
    ]
    tsheet, tfs = build_sheet(tiles, 4)
    tsheet.save(f"{OUT}/tileset.png")
    print("tile size", tfs, "tileset sheet", tsheet.size)

if __name__=="__main__":
    main()
