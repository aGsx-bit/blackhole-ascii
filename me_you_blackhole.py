import math as m
import time

import numpy as np

__author__ = "Mahamad (aGsx / @aGsx-bit)"
__copyright__ = "Copyright (c) 2026 Mahamad (aGsx / @aGsx-bit)"
__license__ = "Attribution Open Source (see LICENSE)"

SIZE = 9
FPS = 30
SS = 1
ASPECT = 1.08
MAXROWS = 88
CW_GLYPH = 6
CH_GLYPH = 10
TK_MS = 16.0
QL = 24

NP = 32768

T_INTRO_END = 6.60
T_IGNITE = 0.80
T_HOLE1 = 1.35
T_DISK = 3.90
T_COLLAPSE1 = 12.10
T_EAT1_END = 15.65
T_RE_EXP = 16.55
T_HOLE2 = 18.45
T_RE_IN = 20.05
T_EAT2_END = 27.35
T_BH_FINAL = 28.00
T_FADEOUT = 28.15
T_BH_LOOP = 30.60
T_FINAL = T_INTRO_END + T_BH_FINAL
T_LOOP = T_INTRO_END + T_BH_LOOP
BEAT_PERIOD = 2.0 / 3.0

RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
NR = len(RAMP) - 1
CIDX = {c: i for i, c in enumerate(RAMP)}

_FONT5X9 = {
    " ": (0, 0, 0, 0, 0, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 0, 4, 4, 0),
    "'": (4, 4, 8, 0, 0, 0, 0, 0, 0),
    "`": (8, 4, 2, 0, 0, 0, 0, 0, 0),
    "^": (0, 4, 10, 17, 0, 0, 0, 0, 0),
    '"': (10, 10, 0, 0, 0, 0, 0, 0, 0),
    ",": (0, 0, 0, 0, 0, 0, 4, 4, 8),
    ":": (0, 0, 4, 4, 0, 0, 4, 4, 0),
    ";": (0, 0, 4, 4, 0, 0, 4, 4, 8),
    "I": (0, 14, 4, 4, 4, 4, 4, 14, 0),
    "l": (0, 12, 4, 4, 4, 4, 4, 14, 0),
    "!": (0, 4, 4, 4, 4, 4, 0, 4, 0),
    "i": (0, 4, 0, 12, 4, 4, 4, 14, 0),
    ">": (0, 8, 4, 2, 1, 2, 4, 8, 0),
    "<": (0, 2, 4, 8, 16, 8, 4, 2, 0),
    "~": (0, 0, 0, 10, 21, 0, 0, 0, 0),
    "+": (0, 0, 4, 4, 31, 4, 4, 0, 0),
    "_": (0, 0, 0, 0, 0, 0, 0, 0, 31),
    "-": (0, 0, 0, 0, 14, 0, 0, 0, 0),
    "?": (0, 14, 17, 1, 2, 4, 0, 4, 0),
    "]": (0, 14, 2, 2, 2, 2, 2, 14, 0),
    "[": (0, 14, 8, 8, 8, 8, 8, 14, 0),
    "}": (0, 12, 4, 4, 2, 4, 4, 12, 0),
    "{": (0, 6, 4, 4, 8, 4, 4, 6, 0),
    "1": (0, 4, 12, 4, 4, 4, 4, 14, 0),
    ")": (8, 4, 2, 2, 2, 2, 2, 4, 8),
    "(": (2, 4, 8, 8, 8, 8, 8, 4, 2),
    "|": (4, 4, 4, 4, 4, 4, 4, 4, 4),
    "\\": (0, 16, 8, 8, 4, 2, 2, 1, 0),
    "/": (0, 1, 2, 2, 4, 8, 8, 16, 0),
    "t": (0, 8, 8, 28, 8, 8, 9, 6, 0),
    "f": (0, 6, 9, 8, 28, 8, 8, 8, 0),
    "j": (0, 2, 0, 6, 2, 2, 18, 12, 0),
    "r": (0, 0, 0, 22, 25, 16, 16, 16, 0),
    "x": (0, 0, 0, 17, 10, 4, 10, 17, 0),
    "n": (0, 0, 0, 30, 17, 17, 17, 17, 0),
    "u": (0, 0, 0, 17, 17, 17, 17, 15, 0),
    "v": (0, 0, 0, 17, 17, 17, 10, 4, 0),
    "c": (0, 0, 0, 14, 17, 16, 17, 14, 0),
    "z": (0, 0, 0, 31, 2, 4, 8, 31, 0),
    "X": (0, 17, 17, 10, 4, 10, 17, 17, 0),
    "Y": (0, 17, 17, 10, 4, 4, 4, 4, 0),
    "U": (0, 17, 17, 17, 17, 17, 17, 14, 0),
    "J": (0, 7, 2, 2, 2, 18, 18, 12, 0),
    "C": (0, 14, 17, 16, 16, 16, 17, 14, 0),
    "L": (0, 16, 16, 16, 16, 16, 16, 31, 0),
    "Q": (0, 14, 17, 17, 17, 21, 18, 13, 0),
    "0": (0, 14, 17, 19, 21, 25, 17, 14, 0),
    "O": (0, 14, 17, 17, 17, 17, 17, 14, 0),
    "Z": (0, 31, 1, 2, 4, 8, 16, 31, 0),
    "m": (0, 0, 0, 26, 21, 21, 21, 21, 0),
    "w": (0, 0, 0, 17, 17, 21, 21, 10, 0),
    "q": (0, 0, 0, 15, 17, 15, 1, 1, 0),
    "p": (0, 0, 0, 30, 17, 30, 16, 16, 0),
    "d": (0, 1, 1, 15, 17, 17, 17, 15, 0),
    "b": (0, 16, 16, 30, 17, 17, 17, 30, 0),
    "k": (0, 16, 16, 18, 20, 24, 20, 18, 0),
    "h": (0, 16, 16, 30, 17, 17, 17, 17, 0),
    "a": (0, 0, 0, 14, 1, 15, 17, 15, 0),
    "o": (0, 0, 0, 14, 17, 17, 17, 14, 0),
    "*": (0, 0, 21, 14, 31, 14, 21, 0, 0),
    "#": (0, 10, 10, 31, 10, 31, 10, 10, 0),
    "M": (0, 17, 27, 21, 21, 17, 17, 17, 0),
    "W": (0, 17, 17, 17, 21, 21, 27, 17, 0),
    "&": (0, 12, 18, 18, 12, 21, 18, 13, 0),
    "8": (0, 14, 17, 17, 14, 17, 17, 14, 0),
    "%": (0, 25, 26, 2, 4, 8, 11, 19, 0),
    "B": (0, 30, 17, 17, 30, 17, 17, 30, 0),
    "@": (0, 14, 17, 23, 21, 23, 16, 14, 0),
    "$": (4, 15, 20, 14, 5, 5, 30, 4, 0),
}

GLYPH_MASK = np.zeros((len(RAMP), CH_GLYPH, CW_GLYPH, 1), dtype=np.uint8)
for _i, _ch in enumerate(RAMP):
    _rows = _FONT5X9[_ch]
    for _r in range(9):
        _bits = _rows[_r]
        for _c in range(5):
            if (_bits >> (4 - _c)) & 1:
                GLYPH_MASK[_i, _r, _c, 0] = 1
GLYPH_BG = ((1 - GLYPH_MASK) * np.array([5, 5, 9], dtype=np.uint8)).astype(np.uint8)

rng = np.random.RandomState(19681)

ME_COL_BASE = np.array([0.56, 0.24, 0.88], dtype=np.float32)
ME_COL_HIGH = np.array([0.88, 0.56, 1.00], dtype=np.float32)
YOU_COL_BASE = np.array([0.04, 0.84, 1.00], dtype=np.float32)
YOU_COL_HIGH = np.array([0.74, 0.97, 1.00], dtype=np.float32)
GOLD_CORE = np.array([1.00, 0.72, 0.20], dtype=np.float32)
GOLD_BRIGHT = np.array([1.00, 0.90, 0.52], dtype=np.float32)


def _sd_cap(px, py, ax, ay, bx, by, r):
    pax, pay = px - ax, py - ay
    bax, bay = bx - ax, by - ay
    h = np.clip((pax * bax + pay * bay) / (bax * bax + bay * bay + 1e-9), 0.0, 1.0)
    return np.sqrt((pax - bax * h) ** 2 + (pay - bay * h) ** 2) - r


def _sd_me(x, y):
    r_st = 0.0076
    cxm, cy = -0.435, 0.055
    d_m = np.minimum(
        np.minimum(_sd_cap(x, y, cxm - 0.072, cy - 0.105, cxm - 0.072, cy + 0.105, r_st),
                   _sd_cap(x, y, cxm - 0.072, cy + 0.105, cxm, cy - 0.015, r_st)),
        np.minimum(_sd_cap(x, y, cxm, cy - 0.015, cxm + 0.072, cy + 0.105, r_st),
                   _sd_cap(x, y, cxm + 0.072, cy + 0.105, cxm + 0.072, cy - 0.105, r_st)),
    )
    cxe, cye = -0.220, 0.015
    re = np.sqrt(((x - cxe) / 0.055) ** 2 + ((y - cye) / 0.062) ** 2)
    d_ring = np.abs(re - 1.0) * 0.058 - r_st
    cut_e = (x > cxe + 0.002) & (y < cye - 0.002) & (y > cye - 0.048)
    d_ring = np.where(cut_e, 0.05, d_ring)
    d_bar = _sd_cap(x, y, cxe - 0.051, cye + 0.008, cxe + 0.051, cye + 0.008, r_st * 0.85)
    d_e = np.minimum(d_ring, d_bar)
    return np.minimum(d_m, d_e)


def _sd_you(x, y):
    r_st = 0.0076
    cxy, cy = 0.105, -0.045
    d_y = np.minimum(
        np.minimum(_sd_cap(x, y, cxy - 0.062, cy + 0.105, cxy, cy - 0.005, r_st),
                   _sd_cap(x, y, cxy + 0.062, cy + 0.105, cxy, cy - 0.005, r_st)),
        _sd_cap(x, y, cxy, cy - 0.005, cxy, cy - 0.105, r_st),
    )
    cxo, cyo = 0.265, -0.085
    ro = np.sqrt(((x - cxo) / 0.055) ** 2 + ((y - cyo) / 0.062) ** 2)
    d_o = np.abs(ro - 1.0) * 0.058 - r_st
    cxu, cyu = 0.425, -0.085
    d_u_l = _sd_cap(x, y, cxu - 0.051, cyu + 0.060, cxu - 0.051, cyu - 0.012, r_st)
    d_u_r = _sd_cap(x, y, cxu + 0.051, cyu + 0.060, cxu + 0.051, cyu - 0.064, r_st)
    ru = np.sqrt((x - cxu) ** 2 + (y - (cyu - 0.012)) ** 2)
    d_u_arc = np.where(y <= cyu - 0.012, np.abs(ru - 0.051) - r_st, 0.05)
    d_u = np.minimum(np.minimum(d_u_l, d_u_r), d_u_arc)
    return np.minimum(d_y, np.minimum(d_o, d_u))


def _sample_sdf_word(sd_fn, xmin, xmax, ymin, ymax, count, yaw_deg=0.0, z_shift=0.0, cx_pivot=0.0):
    n_cand = count * 36
    px = rng.uniform(xmin, xmax, size=n_cand).astype(np.float32)
    py = rng.uniform(ymin, ymax, size=n_cand).astype(np.float32)
    d = sd_fn(px, py)

    core_idx = np.nonzero(d < 0.0)[0]
    edge_idx = np.nonzero((d < 0.0) & (d >= -0.0034))[0]

    n_front = int(count * 0.68)
    n_wall = count - n_front
    sel_f = core_idx[rng.randint(0, len(core_idx), size=n_front)]
    sel_w = edge_idx[rng.randint(0, len(edge_idx), size=n_wall)]
    sel = np.concatenate([sel_f, sel_w])

    lx = px[sel]
    ly = py[sel]
    d_sel = d[sel]

    depth_half = 0.038
    spine_norm = np.clip(-d_sel[:n_front] / 0.0076, 0.0, 1.0)
    z_f = (-depth_half - 0.004 * spine_norm).astype(np.float32)
    z_w = rng.uniform(-depth_half + 0.003, depth_half, size=n_wall).astype(np.float32)
    lz = np.concatenate([z_f, z_w])

    z_norm = np.clip((depth_half - lz[n_front:]) / (2.0 * depth_half), 0.0, 1.0)
    light_dir = np.clip(0.5 + 0.5 * ((ly[n_front:] - ymin) / max(ymax - ymin, 1e-4)), 0.0, 1.0)
    front_shade = (0.82 + 0.18 * spine_norm).astype(np.float32)
    wall_shade = (0.18 + 0.22 * (z_norm ** 1.35) + 0.08 * light_dir).astype(np.float32)
    shade = np.concatenate([front_shade, wall_shade]).astype(np.float32)

    ang = m.radians(yaw_deg)
    ca, sa = m.cos(ang), m.sin(ang)
    rx = lx - cx_pivot
    wx = cx_pivot + rx * ca + lz * sa
    wz = -rx * sa + lz * ca + z_shift

    pos = np.stack([wx, ly, wz], axis=1).astype(np.float32)
    return pos, shade


N_HALF = NP // 2
POS_ME, SPINE_ME = _sample_sdf_word(_sd_me, -0.54, -0.14, -0.10, 0.20, N_HALF, yaw_deg=10.0, z_shift=-0.02, cx_pivot=-0.33)
POS_YOU, SPINE_YOU = _sample_sdf_word(_sd_you, 0.01, 0.51, -0.18, 0.10, NP - N_HALF, yaw_deg=-10.0, z_shift=-0.02, cx_pivot=0.265)
POS_WORDS = np.vstack([POS_ME, POS_YOU]).astype(np.float32)
INTRO_SPINE = np.concatenate([SPINE_ME, SPINE_YOU]).astype(np.float32) #                                                    Love U Sheto
IS_ME = np.zeros(NP, dtype=bool)
IS_ME[:N_HALF] = True
POS_SCATTER = (POS_WORDS + rng.randn(NP, 3) * 0.14).astype(np.float32)

TOR_H = (np.clip(POS_WORDS[:, 1] / 0.14, -1.0, 1.0) * 0.45 + rng.randn(NP) * 0.06).astype(np.float32)
TOR_RAD_NORM = (0.68 + 0.34 * rng.rand(NP)).astype(np.float32)
TOR_JIT_ANG = (rng.randn(NP) * 0.22).astype(np.float32)
TOR_PHASE0 = np.where(IS_ME, m.pi, 0.0).astype(np.float32) + TOR_JIT_ANG
INTRO_LUM = (0.14 + 1.48 * INTRO_SPINE) * np.where(IS_ME, 1.24, 1.0).astype(np.float32)
INTRO_COL_MIX = np.clip(0.14 * rng.rand(NP) + 0.86 * INTRO_SPINE, 0.0, 1.0).astype(np.float32)

N_BRIDGE = 240
_bu = np.linspace(0.0, 1.0, N_BRIDGE, dtype=np.float32)
BRIDGE_T = rng.rand(N_BRIDGE).astype(np.float32)
BRIDGE_JIT = (rng.randn(N_BRIDGE, 2) * 0.015).astype(np.float32)

_u0 = rng.rand(NP).astype(np.float32)
_phi0 = (rng.rand(NP) * 2.0 * m.pi).astype(np.float32)
_cost0 = (rng.rand(NP) * 2.0 - 1.0).astype(np.float32)
_sint0 = np.sqrt(np.maximum(1.0 - _cost0 * _cost0, 0.0)).astype(np.float32)
_rad0 = (0.35 + 6.40 * (_u0 ** 0.72)).astype(np.float32)
P0_POS = np.stack(
    [_rad0 * _sint0 * np.cos(_phi0), _rad0 * _sint0 * np.sin(_phi0), _rad0 * _cost0], axis=1
).astype(np.float32)
P0_VEL = (rng.randn(NP, 3) * 0.35).astype(np.float32) + P0_POS * 0.16
P0_CHAR = rng.randint(12, NR + 1, size=NP).astype(np.int32)
P0_KEEP = rng.rand(NP) < 0.14
_c0_pick = rng.rand(NP).astype(np.float32)
P0_COL = np.where(
    _c0_pick[:, None] < 0.55,
    np.array([0.94, 0.96, 1.00], dtype=np.float32),
    np.where(
        _c0_pick[:, None] < 0.82,
        np.array([0.56, 0.74, 1.00], dtype=np.float32),
        np.array([0.84, 0.66, 0.96], dtype=np.float32),
    ),
).astype(np.float32)
P0_BRI = (0.72 + 0.95 * (rng.rand(NP) ** 1.2)).astype(np.float32)

_is_star1 = rng.rand(NP) < 0.24
_ur1 = rng.rand(NP).astype(np.float32)
R1_CLOUD = (0.05 + 1.85 * (_ur1 ** 0.74)).astype(np.float32)
_disk_r1 = (0.05 + 1.32 * (_ur1 ** 0.70)).astype(np.float32)
_star_r1 = (0.95 + 2.75 * (_ur1 ** 0.60)).astype(np.float32)
R1_BASE = np.where(_is_star1, _star_r1, _disk_r1).astype(np.float32)

ARM1 = (np.arange(NP, dtype=np.int32) % 3).astype(np.float32)
_ang_unif1 = (rng.rand(NP) * 2.0 * m.pi).astype(np.float32)
_ang_jit1 = (rng.randn(NP) * 0.36).astype(np.float32)
A1_SPIRAL = (ARM1 * (2.0 * m.pi / 3.0) + 3.15 * np.log(R1_BASE + 0.18) + _ang_jit1).astype(np.float32)
_in_ring1 = rng.rand(NP) < 0.30
A1_SPIRAL = np.where(_in_ring1, _ang_unif1, A1_SPIRAL).astype(np.float32)
A1_MIX = np.sin(_ang_unif1 - A1_SPIRAL)

_star_cost = (rng.rand(NP) * 2.0 - 1.0).astype(np.float32)
_star_y = (_star_r1 * _star_cost * 0.90).astype(np.float32)
Z1_NOISE = np.clip(rng.randn(NP), -2.0, 2.0).astype(np.float32)
P1_STREAK = (1.10 + 0.65 * rng.rand(NP)).astype(np.float32)
P1_OUTLIER = rng.rand(NP) < 0.045
R1_EAT_RATE = (0.34 + 0.32 * (1.0 - np.clip(R1_BASE / 2.2, 0.0, 1.0)) + 0.08 * rng.rand(NP)).astype(np.float32)
STAR1_Y = _star_y
IS_STAR1 = _is_star1
_st1_pick = rng.rand(NP).astype(np.float32)
STAR1_COL = np.where(
    _st1_pick[:, None] < 0.44,
    np.array([0.94, 0.96, 1.00], dtype=np.float32),
    np.where(
        _st1_pick[:, None] < 0.74,
        np.array([0.58, 0.78, 1.00], dtype=np.float32),
        np.where(
            _st1_pick[:, None] < 0.90,
            np.array([0.90, 0.54, 0.96], dtype=np.float32),
            np.array([1.00, 0.76, 0.56], dtype=np.float32),
        ),
    ),
).astype(np.float32)

_ur2 = rng.rand(NP).astype(np.float32)
R2_BASE = (0.06 + 1.80 * (_ur2 ** 0.70)).astype(np.float32)
ARM2 = (np.arange(NP, dtype=np.int32) % 4).astype(np.float32)
_arm_jit2 = (rng.randn(NP) * (0.28 + 0.20 * np.clip(R2_BASE / 1.75, 0.0, 1.0))).astype(np.float32)
A2_BASE = (ARM2 * (m.pi * 0.5) - 2.35 * np.log(R2_BASE + 0.22) + _arm_jit2).astype(np.float32)
Z2_NOISE = np.clip(rng.randn(NP), -2.2, 2.2).astype(np.float32)
P2_LUM = (1.15 + 0.65 * rng.rand(NP)).astype(np.float32)
K_RE = (0.64 + 0.26 * (1.0 - np.clip(R2_BASE / 1.78, 0.0, 1.0)) + 0.05 * rng.rand(NP)).astype(np.float32)
P2_OUTLIER = rng.rand(NP) < 0.015

_QUAD_COLS = np.array(
    [
        [1.00, 0.78, 0.20],
        [0.16, 0.90, 1.00],
        [0.24, 0.44, 1.00],
        [0.86, 0.24, 0.96],
    ],
    dtype=np.float32,
)
_p2_ang0 = (ARM2 * (m.pi * 0.5) + _arm_jit2 * 0.45 + 0.65) % (2.0 * m.pi)
_qf = (_p2_ang0 / (m.pi * 0.5)) % 4.0
_qi0 = np.floor(_qf).astype(np.int32) % 4
_qi1 = (_qi0 + 1) % 4
_qfrac = (_qf - np.floor(_qf)).astype(np.float32)
_qfrac = _qfrac * _qfrac * (3.0 - 2.0 * _qfrac)
P2_COL = (_QUAD_COLS[_qi0] * (1.0 - _qfrac)[:, None] + _QUAD_COLS[_qi1] * _qfrac[:, None]).astype(np.float32)

NSTARS = 1100
STAR_UR = rng.rand(NSTARS).astype(np.float32)
STAR_UC = rng.rand(NSTARS).astype(np.float32)
STAR_PHASE = (rng.rand(NSTARS) * 2.0 * m.pi).astype(np.float32)
STAR_BRI = (0.48 + 0.65 * rng.rand(NSTARS)).astype(np.float32)
STAR_R = None
STAR_C = None

S = {"last": 0.0}
CW = CW_GLYPH
CH = CH_GLYPH
ROWS = MAXROWS
COLS = 158
W = 948
H = 880
XC = None
YC = None
RC = None
HSC = None
PPM_HDR = b""
Q_TO_U8 = None


def ss_scalar(a, b, x):
    t = min(max((x - a) / (b - a), 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


def ss(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def mix(a, b, k):
    return a + (b - a) * k


def interp_keys(keys, t):
    if t <= keys[0][0]:
        return keys[0][1]
    if t >= keys[-1][0]:
        return keys[-1][1]
    for i in range(len(keys) - 1):
        t0, v0 = keys[i]
        t1, v1 = keys[i + 1]
        if t <= t1:
            k = ss_scalar(t0, t1, t)
            return v0 + (v1 - v0) * k
    return keys[-1][1]


def init(cw, ch, rows):
    global CW, CH, ROWS, COLS, W, H, XC, YC, RC, HSC, PPM_HDR, Q_TO_U8, STAR_R, STAR_C
    CW = CW_GLYPH
    CH = CH_GLYPH
    ROWS = MAXROWS // 2 * 2
    COLS = int(ROWS * CH * ASPECT / CW) // 2 * 2
    W, H = COLS * CW, ROWS * CH
    PPM_HDR = f"P6\n{W} {H}\n255\n".encode("ascii")
    Q_TO_U8 = np.array([v * 255 // (QL - 1) for v in range(QL)], dtype=np.uint8)

    xs = (np.arange(COLS, dtype=np.float32) + 0.5) * CW
    ys = (np.arange(ROWS, dtype=np.float32) + 0.5) * CH
    XC = (((xs - W / 2) / H)[None, :] * np.ones((ROWS, 1), np.float32)).astype(np.float32)
    YC = (((ys - H / 2) / H)[:, None] * np.ones((1, COLS), np.float32)).astype(np.float32)
    RC = np.sqrt(XC * XC + YC * YC).astype(np.float32)

    rr, cc = np.mgrid[0:ROWS, 0:COLS]
    HSC = (((rr * 73856093) ^ (cc * 19349663) ^ 0x5BD1E995) % 1009 / 1009.0).astype(np.float32)
    STAR_R = np.clip((STAR_UR * ROWS).astype(np.int32), 0, ROWS - 1)
    STAR_C = np.clip((STAR_UC * COLS).astype(np.int32), 0, COLS - 1)
    reset()


def reset():
    S["last"] = 0.0


def pulse(t_bh):
    if t_bh < 1.85:
        return 0.0
    if t_bh < T_RE_EXP:
        gate = ss_scalar(1.85, 2.55, t_bh) * (1.0 - ss_scalar(14.30, 15.30, t_bh))
        u = ((t_bh - 2.00) % BEAT_PERIOD) / BEAT_PERIOD
    else:
        gate = ss_scalar(16.55, 16.85, t_bh) * (1.0 - ss_scalar(26.60, 27.55, t_bh))
        u = ((t_bh - 16.65) % BEAT_PERIOD) / BEAT_PERIOD
    if gate <= 0.0:
        return 0.0
    if u < 0.09:
        env = ss_scalar(0.0, 0.09, u)
    elif u < 0.68:
        env = m.exp(-(u - 0.09) * 5.2) * (1.0 - ss_scalar(0.50, 0.68, u))
    else:
        env = 0.0
    return gate * env


def camera_basis(t_bh):
    elev_keys = [
        (0.0, 14.0),
        (1.6, 52.0),
        (4.0, 30.0),
        (5.9, 16.0),
        (7.1, 20.0),
        (8.2, 34.0),
        (9.3, 52.0),
        (10.2, 66.0),
        (11.1, 32.0),
        (12.2, 24.0),
        (14.5, 28.0),
        (16.5, 60.0),
        (19.5, 68.0),
        (23.5, 62.0),
        (28.0, 56.0),
    ]
    roll_keys = [
        (0.0, 0.0),
        (3.5, -5.0),
        (6.0, 9.0),
        (7.2, -10.0),
        (8.5, -14.0),
        (10.0, 4.0),
        (11.3, 6.0),
        (12.4, -7.0),
        (14.5, 2.0),
        (16.5, 0.0),
        (20.0, -4.0),
        (24.0, 5.0),
        (28.0, 0.0),
    ]
    dist_keys = [
        (0.0, 2.35),
        (1.2, 1.50),
        (4.0, 1.48),
        (6.5, 1.56),
        (10.0, 1.66),
        (12.5, 1.56),
        (16.0, 1.62),
        (17.0, 1.44),
        (21.0, 1.56),
        (28.0, 1.62),
    ]
    elev = m.radians(interp_keys(elev_keys, t_bh))
    roll = m.radians(interp_keys(roll_keys, t_bh))
    dist = interp_keys(dist_keys, t_bh)
    azim = 0.14 * t_bh if t_bh < T_RE_EXP else 0.78 + 0.07 * (t_bh - T_RE_EXP)

    ce, se = m.cos(elev), m.sin(elev)
    ca, sa = m.cos(azim), m.sin(azim)
    cam_pos = np.array([dist * ce * sa, dist * se, -dist * ce * ca], dtype=np.float32)

    fwd = -cam_pos / max(np.linalg.norm(cam_pos), 1e-6)
    world_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    right = np.cross(world_up, fwd)
    rn = np.linalg.norm(right)
    if rn < 1e-5:
        right = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    else:
        right /= rn
    up = np.cross(fwd, right)

    cr, sr = m.cos(roll), m.sin(roll)
    right_r = right * cr + up * sr
    up_r = -right * sr + up * cr
    return cam_pos, right_r.astype(np.float32), up_r.astype(np.float32), fwd.astype(np.float32), elev


def blackhole_radius_world(t_bh, p_bh=0.0):
    if t_bh < T_HOLE1:
        return 0.0
    if t_bh < T_RE_EXP:
        keys1 = [
            (T_HOLE1, 0.0),
            (2.00, 0.035),
            (3.00, 0.068),
            (4.10, 0.078),
            (6.00, 0.080),
            (11.50, 0.082),
            (13.80, 0.092),
            (15.20, 0.142),
            (16.20, 0.162),
        ]
        base = interp_keys(keys1, t_bh)
        return base * (1.0 + 0.34 * p_bh)
    keys2 = [
        (T_RE_EXP, 0.018),
        (17.90, 0.050),
        (18.60, 0.016),
        (19.20, 0.028),
        (20.10, 0.046),
        (21.10, 0.070),
        (22.20, 0.090),
        (23.50, 0.105),
        (25.20, 0.128),
        (27.50, 0.168),
        (29.50, 0.172),
    ]
    base = interp_keys(keys2, t_bh)
    p_scale = p_bh * ss_scalar(19.1, 20.4, t_bh)
    return base * (1.0 + 0.34 * p_scale)


def bloom_cells(cells, gain=0.22):
    b = np.clip(cells - 0.40, 0.0, None)
    b2 = b.reshape(ROWS // 2, 2, COLS // 2, 2, 3).mean((1, 3))
    for _ in range(2):
        b2 = (
            b2
            + np.roll(b2, 1, 0)
            + np.roll(b2, -1, 0)
            + np.roll(b2, 1, 1)
            + np.roll(b2, -1, 1)
        ) * 0.20
    up2 = np.repeat(np.repeat(b2, 2, 0), 2, 1)
    return cells + up2 * gain


def phase1_state(t_bh):
    r_bh_base = blackhole_radius_world(t_bh, 0.0)
    k_ign = ss_scalar(0.65, 1.45, t_bh)
    k_arm = ss_scalar(4.20, 7.40, t_bh)
    k_flat = ss_scalar(3.60, 6.00, t_bh)

    if t_bh <= T_COLLAPSE1:
        r = (R1_CLOUD * (1.0 - k_flat) + R1_BASE * k_flat).astype(np.float32)
        collapse_twist = np.zeros(NP, dtype=np.float32)
        fade_eat = np.ones(NP, dtype=np.float32)
    else:
        dt_c = t_bh - T_COLLAPSE1
        uw = dt_c + 0.35 * (1.0 - m.exp(-dt_c / 0.65))
        r_sq = np.maximum(R1_BASE * R1_BASE - R1_EAT_RATE * uw * 1.15, 0.0)
        r = np.sqrt(r_sq).astype(np.float32)
        collapse_twist = (1.55 * (np.sqrt(R1_BASE) - np.sqrt(r))).astype(np.float32)
        fade_eat = np.clip((r - r_bh_base * 0.96) / 0.045, 0.0, 1.0).astype(np.float32)

    omega = (0.50 + 0.85 / ((r + 0.22) ** 0.85)).astype(np.float32)
    ang_base = A1_SPIRAL + 0.45 * (1.0 - k_arm) * A1_MIX
    ang = (ang_base + omega * (t_bh - 0.8) * 0.55 + collapse_twist).astype(np.float32)

    z_puff = 0.42 * (1.0 - 0.95 * k_flat)
    z_disk = (0.016 + z_puff * (0.35 + 0.65 * np.clip(r / 1.4, 0.0, 1.0))) * Z1_NOISE
    z_star = STAR1_Y * np.clip(r / (R1_BASE + 1e-4), 0.15, 1.0)
    z_all = np.where(IS_STAR1, z_star * k_flat + z_disk * (1.0 - k_flat), z_disk)
    if t_bh > T_COLLAPSE1:
        z_all *= np.clip(r / (R1_BASE + 1e-4), 0.18, 1.0)

    P_disk = np.stack([r * np.cos(ang), z_all, r * np.sin(ang)], axis=1).astype(np.float32)

    if k_ign < 1.0:
        P_exp = P0_POS + P0_VEL * min(t_bh, 1.2)
        P = P_exp * (1.0 - k_ign) + P_disk * k_ign
    else:
        P = P_disk

    warm_k = ss_scalar(1.65, 5.40, t_bh)
    u = np.clip((r - r_bh_base) / 1.18, 0.0, 1.0)

    c_cool_in = np.array([0.92, 0.82, 0.74], dtype=np.float32)
    c_cool_mid = np.array([0.48, 0.68, 0.92], dtype=np.float32)
    c_cool_out = np.array([0.36, 0.52, 0.78], dtype=np.float32)
    col_cool = np.where(
        u[:, None] < 0.28,
        mix(c_cool_in, c_cool_mid, (u / 0.28)[:, None]),
        mix(c_cool_mid, c_cool_out, ((u - 0.28) / 0.72)[:, None]),
    )

    c_w0 = np.array([1.00, 0.76, 0.52], dtype=np.float32)
    c_w1 = np.array([1.00, 0.40, 0.12], dtype=np.float32)
    c_w2 = np.array([0.88, 0.20, 0.42], dtype=np.float32)
    c_w3 = np.array([0.48, 0.20, 0.66], dtype=np.float32)
    col_warm = np.where(
        u[:, None] < 0.22,
        mix(c_w0, c_w1, (u / 0.22)[:, None]),
        np.where(
            u[:, None] < 0.54,
            mix(c_w1, c_w2, ((u - 0.22) / 0.32)[:, None]),
            mix(c_w2, c_w3, ((u - 0.54) / 0.46)[:, None]),
        ),
    )
    col_disk = mix(col_cool, col_warm, warm_k)
    star_col_mix = ss_scalar(4.4, 6.2, t_bh)
    col = np.where(
        IS_STAR1[:, None] & (R1_BASE[:, None] > 1.15) & (star_col_mix > 0.01),
        mix(col_disk, STAR1_COL, star_col_mix * 0.85),
        col_disk,
    )

    if k_ign < 1.0:
        col = mix(P0_COL, col, k_ign)

    bri = P1_STREAK * fade_eat
    if t_bh < 1.15:
        bri = np.where(P0_KEEP, P0_BRI, 0.0) * (1.0 - k_ign) + bri * k_ign
    if t_bh > 14.30:
        late_clear = ss_scalar(14.30, 15.55, t_bh)
        bri = bri * (1.0 - 0.82 * late_clear)

    alive = (r > r_bh_base * 0.90) if t_bh >= T_HOLE1 else np.ones(NP, dtype=bool)
    if t_bh >= T_EAT1_END:
        alive &= False

    return P, col, bri, alive, r_bh_base, k_ign


def phase2_state(t_bh):
    r_bh_base = blackhole_radius_world(t_bh, 0.0)
    v = t_bh - T_RE_EXP

    burst = 1.0 - m.exp(-v / 0.30)
    r_burst = (0.03 + (R2_BASE - 0.03) * burst).astype(np.float32)

    cav_open = ss_scalar(18.1, 19.7, t_bh)
    r_cav_target = 0.28 * cav_open
    r_after_cav = np.maximum(r_burst, r_cav_target + 0.14 * R2_BASE).astype(np.float32)

    if t_bh <= T_RE_IN:
        r = r_after_cav
        in_twist = np.zeros(NP, dtype=np.float32)
        fade_eat = np.ones(NP, dtype=np.float32)
        spin = 0.30 * v
    else:
        v_in = T_RE_IN - T_RE_EXP
        burst_in = 1.0 - m.exp(-v_in / 0.30)
        r_burst_in = (0.03 + (R2_BASE - 0.03) * burst_in).astype(np.float32)
        cav_in = ss_scalar(18.1, 19.7, T_RE_IN)
        r_start = np.maximum(r_burst_in, 0.28 * cav_in + 0.14 * R2_BASE).astype(np.float32)

        u = t_bh - T_RE_IN
        uw = u + 0.45 * (1.0 - m.exp(-u / 0.65))
        r_sq = np.maximum(r_start * r_start - K_RE * uw * 0.72, 0.0)
        r = np.sqrt(r_sq).astype(np.float32)
        in_twist = (-0.85 * (np.sqrt(r_start) - np.sqrt(r))).astype(np.float32)
        fade_eat = np.clip((r - r_bh_base * 0.96) / 0.045, 0.0, 1.0).astype(np.float32)
        spin = 0.30 * v_in + 0.44 * u

    ang = (A2_BASE + spin + 0.22 / (r + 0.25) * min(v, 2.0) * 0.12 + in_twist).astype(np.float32)
    z_disk = (0.020 * Z2_NOISE * (0.4 + 0.6 * np.clip(r / 1.5, 0.0, 1.0))).astype(np.float32)
    P = np.stack([r * np.cos(ang), z_disk, r * np.sin(ang)], axis=1).astype(np.float32)

    core_k = np.clip(1.0 - (r - r_bh_base) / 0.16, 0.0, 0.26)[:, None]
    col = mix(P2_COL, np.array([1.00, 0.84, 0.62], dtype=np.float32), core_k)
    bri = P2_LUM * fade_eat * ss_scalar(0.0, 0.20, v)
    if t_bh > 25.2:
        out_cut = ss_scalar(25.2, 27.1, t_bh)
        bri = bri * np.where(P2_OUTLIER, 0.85, 1.0 - 0.72 * out_cut)

    if t_bh < T_RE_IN:
        alive = r > max(r_bh_base * 0.90, 0.26 * cav_open)
    else:
        alive = r > r_bh_base * 0.90
    if t_bh >= T_EAT2_END:
        alive &= False

    return P, col, bri, alive, r_bh_base, 1.0


def _splat_bilinear(ri_f, ci_f, wb, rgb_w):
    r0 = np.floor(ri_f).astype(np.int32)
    c0 = np.floor(ci_f).astype(np.int32)
    fr = (ri_f - r0).astype(np.float32)
    fc = (ci_f - c0).astype(np.float32)

    ncell = ROWS * COLS
    sb = np.zeros(ncell, dtype=np.float32)
    sr = np.zeros(ncell, dtype=np.float32)
    sg = np.zeros(ncell, dtype=np.float32)
    sbl = np.zeros(ncell, dtype=np.float32)

    for dr, wr in ((0, 1.0 - fr), (1, fr)):
        rr = r0 + dr
        mr = (rr >= 0) & (rr < ROWS)
        for dc, wc in ((0, 1.0 - fc), (1, fc)):
            cc = c0 + dc
            valid = mr & (cc >= 0) & (cc < COLS)
            if not np.any(valid):
                continue
            w = wb[valid] * wr[valid] * wc[valid]
            flat = rr[valid] * COLS + cc[valid]
            sb += np.bincount(flat, weights=w, minlength=ncell)
            sr += np.bincount(flat, weights=rgb_w[valid, 0] * w, minlength=ncell)
            sg += np.bincount(flat, weights=rgb_w[valid, 1] * w, minlength=ncell)
            sbl += np.bincount(flat, weights=rgb_w[valid, 2] * w, minlength=ncell)

    bri_cell = (sb / (1.0 + 0.45 * sb)).reshape(ROWS, COLS)
    col_raw = np.stack([sr, sg, sbl], axis=-1).reshape(ROWS, COLS, 3) / np.maximum(sb.reshape(ROWS, COLS, 1), 1e-5)
    bri_grid = bri_cell * 1.15
    col_grid = col_raw * np.clip(bri_grid, 0.0, 1.32)[..., None]
    return bri_grid, col_grid


def _splat_crisp(ri, ci, wb, rgb_w, cz_w, ch_w, accum_gain=0.22, need_sort=False):
    win = (ri >= 0) & (ri < ROWS) & (ci >= 0) & (ci < COLS) & (wb > 0.03)
    bri_grid = np.zeros((ROWS, COLS), dtype=np.float32)
    col_grid = np.zeros((ROWS, COLS, 3), dtype=np.float32)
    idx_override = np.full((ROWS, COLS), -1, dtype=np.int32)
    if not np.any(win):
        return bri_grid, col_grid, idx_override

    ri_w = ri[win]
    ci_w = ci[win]
    wb_w = wb[win]
    rgb_win = rgb_w[win]

    if need_sort:
        order = np.argsort(-cz_w[win])
        ro = ri_w[order]
        co = ci_w[order]
        bo = wb_w[order]
        bri_grid[ro, co] = bo
        col_grid[ro, co] = rgb_win[order] * np.minimum(bo, 1.65)[:, None]
        idx_override[ro, co] = ch_w[win][order]
        return bri_grid, col_grid, idx_override

    flat = ri_w * COLS + ci_w
    ncell = ROWS * COLS
    sb = np.bincount(flat, weights=wb_w, minlength=ncell).reshape(ROWS, COLS)
    sr = np.bincount(flat, weights=rgb_win[:, 0] * wb_w, minlength=ncell).reshape(ROWS, COLS)
    sg = np.bincount(flat, weights=rgb_win[:, 1] * wb_w, minlength=ncell).reshape(ROWS, COLS)
    sbl = np.bincount(flat, weights=rgb_win[:, 2] * wb_w, minlength=ncell).reshape(ROWS, COLS)

    bri_boost = sb / (1.0 + 0.40 * sb) * (1.0 + accum_gain)
    col_avg = np.stack([sr, sg, sbl], axis=-1) / np.maximum(sb[..., None], 1e-5)
    col_grid = col_avg * np.clip(bri_boost, 0.0, 1.65)[..., None]
    return bri_boost, col_grid, idx_override


def render_intro(t):
    k_cryst = ss_scalar(0.0, 0.55, t)
    k_vortex = ss_scalar(1.90, 3.30, t)
    k_pull = ss_scalar(3.20, 5.55, t)
    k_gold = ss_scalar(3.90, 5.75, t)
    k_burst = ss_scalar(5.75, T_INTRO_END, t)

    az_intro = m.radians(-16.0 + 32.0 * ss_scalar(0.0, 2.20, t)) * (1.0 - ss_scalar(2.20, 4.40, t))
    elev = m.radians(9.0 + 23.0 * ss_scalar(1.60, 5.40, t) * (1.0 - k_burst) + 13.0 * k_burst)
    dist = (1.56 - 0.12 * ss_scalar(1.80, 5.60, t)) * (1.0 - k_burst) + 2.35 * k_burst
    ce, se = m.cos(elev), m.sin(elev)
    ca, sa = m.cos(az_intro), m.sin(az_intro)
    cam_pos = np.array([dist * ce * sa, dist * se, -dist * ce * ca], dtype=np.float32)
    fwd = -cam_pos / max(np.linalg.norm(cam_pos), 1e-6)
    world_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    right = np.cross(world_up, fwd)
    right = (right / max(np.linalg.norm(right), 1e-6)).astype(np.float32)
    up = np.cross(fwd, right).astype(np.float32)

    bob = 0.010 * m.sin(t * 2.4)
    P_start = POS_SCATTER * (1.0 - k_cryst) + POS_WORDS * k_cryst
    P_start = P_start.copy()
    P_start[:N_HALF, 1] += bob
    P_start[N_HALF:, 1] -= bob

    if k_vortex > 0.001:
        y_t = TOR_H * (1.0 - 0.94 * k_pull)
        h_frac = np.clip((TOR_H + 0.48) / 0.96, 0.0, 1.0)
        r_funnel_base = (0.12 + 0.52 * (h_frac ** 1.45)) * TOR_RAD_NORM
        r_tor = r_funnel_base * (1.0 - 0.65 * k_pull)
        u_t = max(0.0, t - 1.90)
        omega = 2.6 + 3.0 * (1.0 - h_frac) + 4.8 * k_pull
        ang_tor = TOR_PHASE0 + u_t * omega - 2.8 * h_frac
        sway = (0.055 * (1.0 - k_pull) * np.sin(u_t * 3.2 + h_frac * 2.6)).astype(np.float32)
        P_tor = np.stack([r_tor * np.cos(ang_tor) + sway, y_t, r_tor * np.sin(ang_tor)], axis=1).astype(np.float32)
        P = P_start * (1.0 - k_vortex) + P_tor * k_vortex
    else:
        P = P_start

    if k_burst > 0.001:
        P = P * (1.0 - k_burst) + P0_POS * k_burst

    col_me = mix(ME_COL_BASE, ME_COL_HIGH, INTRO_COL_MIX[:, None])
    col_you = mix(YOU_COL_BASE, YOU_COL_HIGH, INTRO_COL_MIX[:, None])
    p_col = np.where(IS_ME[:, None], col_me, col_you)
    if k_gold > 0.001:
        r_cur = np.sqrt(P[:, 0] ** 2 + P[:, 2] ** 2)
        core_proximity = np.exp(-r_cur * 2.4)[:, None]
        gold_target = mix(GOLD_CORE, GOLD_BRIGHT, core_proximity)
        gold_amt = np.clip(k_gold * (0.45 + 0.65 * core_proximity), 0.0, 1.0)
        p_col = mix(p_col, gold_target, gold_amt)
    if k_burst > 0.001:
        p_col = mix(p_col, P0_COL, k_burst)

    b_intro = INTRO_LUM * (1.0 + 0.55 * ss_scalar(5.35, 5.85, t) * (1.0 - k_burst))
    if k_burst > 0.001:
        b_sparse = np.where(P0_KEEP, P0_BRI, 0.0)
        b_intro = b_intro * (1.0 - k_burst) + b_sparse * k_burst

    rel = P - cam_pos[None, :]
    cx = rel @ right
    cy = rel @ up
    cz = rel @ fwd
    fov = 1.44
    in_front = cz > 0.25

    bri_grid = np.zeros((ROWS, COLS), dtype=np.float32)
    col_grid = np.zeros((ROWS, COLS, 3), dtype=np.float32)
    idx_override = np.full((ROWS, COLS), -1, dtype=np.int32)

    if np.any(in_front):
        cx = cx[in_front]
        cy = cy[in_front]
        cz = cz[in_front]
        c_rgb = p_col[in_front]
        b_val = b_intro[in_front] * np.clip(1.65 / np.maximum(cz, 0.35), 0.50, 1.70)
        ch_val = P0_CHAR[in_front]

        sx = fov * cx / cz
        sy = -fov * cy / cz
        dx_c = W / H * 0.5
        ci = np.round((sx + dx_c) * (COLS / (W / H)) - 0.5).astype(np.int32)
        ri = np.round((sy + 0.5) * ROWS - 0.5).astype(np.int32)
        use_sort = (k_vortex < 0.85) or (k_burst > 0.35)
        bri_grid, col_grid, idx_override = _splat_crisp(
            ri, ci, b_val, c_rgb, cz, ch_val, accum_gain=0.22 * (1.0 - k_burst) * k_vortex, need_sort=use_sort
        )

    star_vis_intro = (1.0 - k_burst) * 0.85
    if star_vis_intro > 0.02:
        sc = STAR_C
        sr = STAR_R
        sb_tw = STAR_BRI * star_vis_intro * (0.55 + 0.45 * np.sin(t * 2.1 + STAR_PHASE))
        empty = bri_grid[sr, sc] < 0.05
        bri_grid[sr[empty], sc[empty]] += sb_tw[empty] * 0.55
        star_c = np.array([0.68, 0.72, 0.96], dtype=np.float32)
        col_grid[sr[empty], sc[empty]] += (sb_tw[empty] * 0.55)[:, None] * star_c[None, :]

    bridge_vis = ss_scalar(0.55, 1.15, t) * (1.0 - ss_scalar(1.85, 2.65, t))
    if bridge_vis > 0.02:
        bu = (BRIDGE_T + t * 0.38) % 1.0
        bx = -0.14 + 0.21 * bu + BRIDGE_JIT[:, 0]
        by = 0.015 - 0.08 * bu + 0.045 * np.sin(bu * m.pi) + BRIDGE_JIT[:, 1]
        bz = (0.04 - 0.07 * bu) + 0.03 * np.sin(bu * m.pi)
        bp = np.stack([bx, by, bz], axis=1) - cam_pos[None, :]
        bcx = bp @ right
        bcy = bp @ up
        bcz = bp @ fwd
        in_fb = bcz > 0.25
        bsx = fov * bcx[in_fb] / bcz[in_fb]
        bsy = -fov * bcy[in_fb] / bcz[in_fb]
        dx_c = W / H * 0.5
        bci = np.round((bsx + dx_c) * (COLS / (W / H)) - 0.5).astype(np.int32)
        bri_row = np.round((bsy + 0.5) * ROWS - 0.5).astype(np.int32)
        valid_b = (bri_row >= 0) & (bri_row < ROWS) & (bci >= 0) & (bci < COLS)
        if np.any(valid_b):
            br_v = bri_row[valid_b]
            bc_v = bci[valid_b]
            bu_v = bu[in_fb][valid_b]
            b_str = bridge_vis * np.sin(bu_v * m.pi) * 0.65
            b_col = mix(ME_COL_HIGH, YOU_COL_HIGH, bu_v[:, None])
            bri_grid[br_v, bc_v] = np.maximum(bri_grid[br_v, bc_v], b_str)
            col_grid[br_v, bc_v] = np.maximum(col_grid[br_v, bc_v], b_col * b_str[:, None])

    flash_k = ss_scalar(5.60, 5.90, t) * (1.0 - ss_scalar(5.95, 6.45, t))
    if flash_k > 0.01:
        core_glow = np.exp(-(RC / 0.085) ** 2) * flash_k * 1.45
        col_grid += core_glow[..., None] * GOLD_BRIGHT[None, None, :]
        bri_grid += core_glow

    col_grid = bloom_cells(col_grid, gain=0.26 * k_vortex * (1.0 - 0.4 * k_burst))
    peak = np.maximum(col_grid, 0.0)
    max_px = peak.max(axis=-1, keepdims=True)
    cells = np.clip(peak / (1.0 + 0.46 * max_px), 0.0, 1.0)

    lum = 0.30 * cells[..., 0] + 0.60 * cells[..., 1] + 0.10 * cells[..., 2]
    cmax = cells.max(axis=-1)
    li = np.clip(0.24 * lum + 0.76 * np.maximum(cmax, np.clip(bri_grid * 0.72, 0.0, 1.0)), 0.0, 1.0) ** 0.70

    ri_out = np.clip((li + (HSC - 0.5) * 0.05) * NR, 0, NR).astype(np.int32)
    ri_out = np.where(cmax < 0.030, 0, ri_out)
    if k_burst > 0.35:
        has_ovr = (idx_override > 0) & (cmax >= 0.030)
        ri_out = np.where(has_ovr, idx_override, ri_out)

    fg = np.clip(cells * 1.24, 0.0, 1.0).astype(np.float32)
    q = np.clip((fg * (QL - 0.01)).astype(np.int16), 0, QL - 1)
    return ri_out, q


def render_cells(t, dt=0.0):
    t = float(t) % T_LOOP
    S["last"] = t

    if t < T_INTRO_END:
        return render_intro(t)

    t_bh = t - T_INTRO_END
    cam_pos, right, up, fwd, elev = camera_basis(t_bh)
    p_bh = pulse(t_bh)

    if t_bh < T_RE_EXP:
        P, p_col, p_bri, alive, r_bh_base, k_ign = phase1_state(t_bh)
        lens_amp = ss_scalar(3.6, 5.8, t_bh) * (1.0 - ss_scalar(13.8, 15.2, t_bh)) * (max(0.0, m.cos(elev)) ** 1.5)
        sparse_mode = t_bh < 0.88
    else:
        P, p_col, p_bri, alive, r_bh_base, k_ign = phase2_state(t_bh)
        lens_amp = 0.14 * (max(0.0, m.cos(elev)) ** 1.6) * (1.0 - ss_scalar(25.2, 27.0, t_bh))
        sparse_mode = False

    rel_bh = -cam_pos
    bh_cx = float(np.dot(rel_bh, right))
    bh_cy = float(np.dot(rel_bh, up))
    bh_cz = float(np.dot(rel_bh, fwd))
    fov = 1.44
    hsx = fov * bh_cx / max(bh_cz, 0.2)
    hsy = -fov * bh_cy / max(bh_cz, 0.2)
    r_bh_base_scr = fov * r_bh_base / max(bh_cz, 0.2)
    r_bh_scr = fov * blackhole_radius_world(t_bh, p_bh) / max(bh_cz, 0.2)

    P_act = P[alive]
    col_act = p_col[alive]
    bri_act = p_bri[alive]
    ch_act = P0_CHAR[alive]

    bri_grid = np.zeros((ROWS, COLS), dtype=np.float32)
    col_grid = np.zeros((ROWS, COLS, 3), dtype=np.float32)
    idx_override = np.full((ROWS, COLS), -1, dtype=np.int32)

    if len(P_act) > 0:
        rel = P_act - cam_pos[None, :]
        cx = rel @ right
        cy = rel @ up
        cz = rel @ fwd

        in_front = cz > 0.26
        if np.any(in_front):
            cx = cx[in_front]
            cy = cy[in_front]
            cz = cz[in_front]
            c_rgb = col_act[in_front]
            b_val = bri_act[in_front]
            ch_val = ch_act[in_front]

            sx = fov * cx / cz
            sy = -fov * cy / cz

            if r_bh_base_scr > 0.015 and lens_amp > 0.01:
                behind = cz > bh_cz
                dx = sx - hsx
                dy = sy - hsy
                dp = np.sqrt(dx * dx + dy * dy) + 1e-5
                r_e = r_bh_base_scr * 1.10
                dp_lens = 0.5 * (dp + np.sqrt(dp * dp + 4.0 * r_e * r_e * lens_amp))
                need_lens = behind & (dp < r_e * 2.2)
                if np.any(need_lens):
                    ux = dx[need_lens] / dp[need_lens]
                    uy = dy[need_lens] / dp[need_lens]
                    sign_flip = np.where((np.abs(uy) < 0.25) & ((np.arange(len(ux)) & 1) == 1), -1.0, 1.0)
                    uy = uy * sign_flip
                    sx[need_lens] = hsx + ux * dp_lens[need_lens]
                    sy[need_lens] = hsy + uy * dp_lens[need_lens]
                    arch_boost = 1.0 + 0.65 * lens_amp * np.exp(-((dp_lens[need_lens] - r_e) / 0.036) ** 2)
                    b_val[need_lens] *= arch_boost

            depth_scale = np.clip(1.85 / np.maximum(cz, 0.35), 0.45, 1.80).astype(np.float32)
            doppler = 1.0 + 0.14 * np.clip(-(sx - hsx) * 1.4, -1.0, 1.0) * (1.0 - 0.5 * ss_scalar(0.0, 1.0, abs(m.sin(elev))))
            w_bri = b_val * depth_scale * doppler

            dx_c = W / H * 0.5
            ci_f = (sx + dx_c) * (COLS / (W / H)) - 0.5
            ri_f = (sy + 0.5) * ROWS - 0.5
            early_cloud = (not sparse_mode) and (t_bh < 4.90)

            if early_cloud:
                in_b = (ri_f >= -1.0) & (ri_f < ROWS) & (ci_f >= -1.0) & (ci_f < COLS)
                if np.any(in_b):
                    bri_s, col_s = _splat_bilinear(ri_f[in_b], ci_f[in_b], w_bri[in_b] * 0.62, c_rgb[in_b])
                    k_blend = ss_scalar(3.90, 4.90, t_bh)
                    if k_blend > 0.01:
                        ci = np.round(ci_f).astype(np.int32)
                        ri = np.round(ri_f).astype(np.int32)
                        bri_c, col_c, idx_override = _splat_crisp(
                            ri, ci, w_bri, c_rgb, cz, ch_val, accum_gain=0.30, need_sort=False
                        )
                        bri_grid = bri_s * (1.0 - k_blend) + bri_c * k_blend
                        col_grid = col_s * (1.0 - k_blend) + col_c * k_blend
                    else:
                        bri_grid, col_grid = bri_s, col_s
            else:
                ci = np.round(ci_f).astype(np.int32)
                ri = np.round(ri_f).astype(np.int32)
                accum_g = 0.0 if sparse_mode else 0.30
                bri_grid, col_grid, idx_override = _splat_crisp(
                    ri, ci, w_bri, c_rgb, cz, ch_val, accum_gain=accum_g, need_sort=sparse_mode
                )
                if not sparse_mode:
                    nb_cnt = (
                        (bri_grid > 0.18).astype(np.int32)
                        + (np.roll(bri_grid, 1, 1) > 0.18)
                        + (np.roll(bri_grid, -1, 1) > 0.18)
                        + (np.roll(bri_grid, 1, 0) > 0.18)
                        + (np.roll(bri_grid, -1, 0) > 0.18)
                    )
                    gap_fill = (bri_grid < 0.04) & (nb_cnt >= 3)
                    if np.any(gap_fill):
                        avg_b = (np.roll(bri_grid, 1, 1) + np.roll(bri_grid, -1, 1)) * 0.42
                        avg_c = (np.roll(col_grid, 1, 1) + np.roll(col_grid, -1, 1)) * 0.42
                        bri_grid = np.where(gap_fill, avg_b, bri_grid)
                        col_grid = np.where(gap_fill[..., None], avg_c, col_grid)

    if (not sparse_mode) and (t_bh < 4.90):
        k_fade_sm = 1.0 - ss_scalar(3.80, 4.90, t_bh)
        h_k = 0.24 * k_fade_sm
        v_k = 0.12 * k_fade_sm
        c_k = max(0.24, 1.0 - 2.0 * h_k - 2.0 * v_k)
        sm_b = (
            bri_grid * c_k
            + (np.roll(bri_grid, 1, 1) + np.roll(bri_grid, -1, 1)) * h_k
            + (np.roll(bri_grid, 1, 0) + np.roll(bri_grid, -1, 0)) * v_k
        )
        sm_c = (
            col_grid * c_k
            + (np.roll(col_grid, 1, 1) + np.roll(col_grid, -1, 1)) * h_k
            + (np.roll(col_grid, 1, 0) + np.roll(col_grid, -1, 0)) * v_k
        )
        bri_grid = bri_grid * (1.0 - k_fade_sm) + np.maximum(bri_grid * 0.90, sm_b * 1.10) * k_fade_sm
        col_grid = col_grid * (1.0 - k_fade_sm) + np.where(bri_grid[..., None] > sm_b[..., None] * 1.10, col_grid, sm_c * 1.10) * k_fade_sm

    star_vis = (
        ss_scalar(3.5, 5.5, t_bh) * (1.0 - ss_scalar(14.2, 15.6, t_bh))
        + ss_scalar(17.0, 18.5, t_bh) * (1.0 - ss_scalar(25.5, 27.0, t_bh))
    )
    if star_vis > 0.02:
        sc = STAR_C
        sr = STAR_R
        sb_tw = STAR_BRI * star_vis * (0.70 + 0.30 * np.sin(t_bh * 2.3 + STAR_PHASE))
        empty = bri_grid[sr, sc] < 0.08
        bri_grid[sr[empty], sc[empty]] += sb_tw[empty]
        star_col = np.array([0.75, 0.74, 0.96], dtype=np.float32)
        col_grid[sr[empty], sc[empty]] += sb_tw[empty, None] * star_col[None, :]

    dist = np.sqrt((XC - hsx) ** 2 + (YC - hsy) ** 2)
    cell_px = 1.0 / ROWS

    if r_bh_scr > 0.008:
        if lens_amp > 0.05:
            ang_c = np.arctan2(YC - hsy, XC - hsx)
            vert_w = np.abs(np.sin(ang_c)) ** 1.4
            arch_r = r_bh_base_scr * 1.15
            arch_g = np.exp(-((dist - arch_r) / 0.022) ** 2) * vert_w * lens_amp * 0.65
            arch_col = np.array([1.00, 0.66, 0.38], dtype=np.float32)
            col_grid += arch_g[..., None] * arch_col[None, None, :]
            bri_grid += arch_g * 0.72

        shadow_cut = ss(r_bh_scr - 0.8 * cell_px, r_bh_scr + 0.35 * cell_px, dist)
        col_grid *= shadow_cut[..., None]
        bri_grid *= shadow_cut

        if t_bh < T_RE_EXP:
            ring_only_vis = ss_scalar(13.8, 15.2, t_bh)
            ring_fade = 0.35 + 0.65 * ring_only_vis
            ring_bright = (0.75 + 0.45 * ring_only_vis) * (1.0 + 0.55 * p_bh)
            p_ring = p_bh
        else:
            ring_fade = ss_scalar(18.5, 19.4, t_bh) * (0.78 + 0.22 * ss_scalar(25.2, 27.0, t_bh))
            p_ring = p_bh * ss_scalar(19.1, 20.4, t_bh)
            ring_bright = 1.15 * (1.0 + 0.55 * p_ring)

        ring_only = (14.8 <= t_bh < T_RE_EXP) or t_bh >= 26.2
        ring_w = (0.0095 if ring_only else 0.0105) * (1.0 + 0.25 * p_ring)
        ring_prof = np.exp(-((dist - (r_bh_scr + 0.25 * cell_px)) / ring_w) ** 2) * ring_bright * ring_fade
        ang_ring = np.arctan2(YC - hsy, XC - hsx)
        ring_shimmer = 1.0 + 0.05 * np.sin(3.0 * ang_ring + t_bh * 2.2)
        ring_col = np.array([0.96, 0.78, 0.54], dtype=np.float32)
        col_grid += (ring_prof * ring_shimmer)[..., None] * ring_col[None, None, :]
        bri_grid += ring_prof * ring_shimmer

    end_fade = 1.0 - ss_scalar(T_FADEOUT, T_BH_LOOP - 1.0, t_bh)
    col_grid *= end_fade
    bri_grid *= end_fade

    col_grid = bloom_cells(col_grid, gain=0.14 if sparse_mode else 0.24)
    peak = np.maximum(col_grid, 0.0)
    max_px = peak.max(axis=-1, keepdims=True)
    cells = np.clip(peak / (1.0 + 0.48 * max_px), 0.0, 1.0)

    lum = 0.30 * cells[..., 0] + 0.60 * cells[..., 1] + 0.10 * cells[..., 2]
    cmax = cells.max(axis=-1)
    li = np.clip(0.42 * lum + 0.58 * np.maximum(cmax, np.clip(bri_grid * 0.74, 0.0, 1.0)), 0.0, 1.0) ** 0.72

    ring_only = (14.8 <= t_bh < T_RE_EXP) or t_bh >= 26.2
    dither_amp = 0.025 if ring_only else 0.052
    ri = np.clip((li + (HSC - 0.5) * dither_amp) * NR, 0, NR).astype(np.int32)
    cutoff = 0.050 if ring_only else 0.030
    ri = np.where(cmax < cutoff, 0, ri)

    if sparse_mode:
        has_ovr = (idx_override > 0) & (cmax >= cutoff)
        ri = np.where(has_ovr, idx_override, ri)

    fg = np.clip(cells * 1.22, 0.0, 1.0).astype(np.float32)
    q = np.clip((fg * (QL - 0.01)).astype(np.int16), 0, QL - 1)
    return ri, q


def render_ppm_bytes(idx, q):
    fg_u8 = Q_TO_U8[q]
    rgb = (GLYPH_MASK[idx] * fg_u8[:, :, None, None, :] + GLYPH_BG[idx]).transpose(0, 2, 1, 3, 4).reshape(H, W, 3)
    return PPM_HDR + rgb.tobytes()


def main():
    import tkinter as tk

    print("Run: me_you_blackhole")
    print(f"particles: {NP} | 3d camera | {FPS} fps")

    root = tk.Tk()
    root.title("Me & You -> Blackhole")
    root.resizable(False, False)
    init(CW_GLYPH, CH_GLYPH, MAXROWS)
    scr_w, scr_h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{W}x{H}+{(scr_w - W) // 2}+{max(0, (scr_h - H) // 2 - 20)}")
    cv = tk.Canvas(root, width=W, height=H, bg="#050509", highlightthickness=0)
    cv.pack()

    photo = tk.PhotoImage(width=W, height=H)
    cv.create_image(0, 0, anchor="nw", image=photo)
    st = {"t0": time.perf_counter(), "paused": False, "pause_t": 0.0, "after_id": None}

    def draw_at(t_val, dt_val=0.0):
        idx, q = render_cells(t_val, dt_val)
        photo.configure(data=render_ppm_bytes(idx, q))

    def quit_app(_=None):
        if st["after_id"] is not None:
            try:
                root.after_cancel(st["after_id"])
            except Exception:
                pass
        root.destroy()

    def restart(_=None):
        st["t0"] = time.perf_counter()
        st["pause_t"] = 0.0
        st["paused"] = False
        reset()
        draw_at(0.0, 0.0)

    def toggle_pause(_=None):
        now = time.perf_counter()
        if st["paused"]:
            st["t0"] = now - st["pause_t"]
            S["last"] = st["pause_t"]
            st["paused"] = False
        else:
            st["pause_t"] = now - st["t0"]
            st["paused"] = True

    def go_final(_=None):
        now = time.perf_counter()
        st["t0"] = now - T_FINAL
        st["pause_t"] = T_FINAL
        S["last"] = T_FINAL
        draw_at(T_FINAL, 0.0)

    root.protocol("WM_DELETE_WINDOW", quit_app)
    root.bind("<Escape>", quit_app)
    root.bind("r", restart)
    root.bind("R", restart)
    root.bind("<space>", toggle_pause)
    root.bind("a", go_final)
    root.bind("A", go_final)

    def tick():
        if st["paused"]:
            st["after_id"] = root.after(40, tick)
            return
        t0 = time.perf_counter()
        t = t0 - st["t0"]
        dt = min(max(t - S["last"], 0.0), 0.1)
        draw_at(t, dt)
        el = (time.perf_counter() - t0) * 1000
        st["after_id"] = root.after(max(1, int(1000 / FPS - el)), tick)

    st["after_id"] = root.after(50, tick)
    root.mainloop()


if __name__ == "__main__":
    main()
