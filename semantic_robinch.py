# Rappel des types struct.pack usuelles :
# B  unsigned char
# H  unsigned short
# I  unsigned int
# b  signed char
# h  signed short
# i  signed int
# f  float

# yymmjjhhmm
version = 1404111942

class Common(Proto):
    def __init__(self):
        print("Common")
        super(Common, self)

    unimplemented = Packet(251, "pic")
    test = Packet(252, "both", [
            ("B", "B"),
            ("H", "H"),
            ("I", "I"),
            ("b", "b"),
            ("h", "h"),
            ("i", "i"),
            ("f", "f")
        ])
    error = Packet(253, "pic")
    getId = Packet(254, "arm")
    id = Packet(255, "pic", [
            ("id", "B")
        ])

class Asserv(Proto):
    type = 1

########### Messages d'asserv et d'odo ##########
    stop = Packet(1, "arm")
    ausecours = Packet(1, "arm")
    block = Packet(2, "arm")
    done = Packet(3, "pic")
    mode = Packet(4, "pic", [
        ("delta", "h"),
        ("alpha", "h"),
        ])
    getPIDErr = Packet(5, "arm")
    PIDErr = Packet(6, "pic", [
        ("deltaErr", "f"),
        ("deltaDeriv", "f"),
        ("deltaInte", "f"),
        ("alphaErr", "f"),
        ("alphaDeriv", "f"),
        ("alphaInte", "f"),
        ])
    getOrders = Packet(7, "arm")
    Orders = Packet(8, "pic", [
        ("deltaOrder", "f"),
        ("alphaOrder", "f"),
        ("leftOrder", "h"),
        ("rightOrder", "h"),
        ("effectiveLeftOrder", "h"),
        ("effectiveRightOrder", "h"),
        ])
    getMotionOrders = Packet(9, "arm")
    MotionOrders = Packet(29, "pic", [
        ("deltaX", "f"),
        ("deltaV", "f"),
        ("deltaA", "f"),
        ("alphaX", "f"),
        ("alphaV", "f"),
        ("alphaA", "f"),
        ])

    step = Packet(10, "pic", [
        ("period", "f"),
        ("ticsG", "i"),
        ("ticsD", "i"),
        ("consignG", "i"),
        ("consignD", "i")
        ])

    setEpsilons = Packet(11, "arm", [
        ("dist", "f"),
        ("speed", "f"),
        ("theta", "f"),
        ("omega", "f")
        ])

    dist = Packet(12, "arm", [
        ("dist", "f"),
        ("vMax", "f"),
        ("aMax", "f"),
        ])

    rot = Packet(13, "arm", [
        ("rot", "f"),
        ("vMax", "f"),
        ("aMax", "f"),
        ])

    distFree = Packet(14, "arm", [
        ("dist", "f")
        ])

    rotFree = Packet(15, "arm", [
        ("rot", "f")
        ])

    distRot = Packet(16, "arm", [
        ("dist", "f"),
        ("rot", "f"),
        ("vDistMax", "f"),
        ("aDistMax", "f"),
        ("vRotMax", "f"),
        ("aRotMax", "f")
        ])

    reachX = Packet(17, "arm", [
        ("x", "f"),
        ("vMax", "f"),
        ("aMax", "f")
        ])

    reachY = Packet(18, "arm", [
        ("y", "f"),
        ("vMax", "f"),
        ("aMax", "f")
        ])

    reachTheta = Packet(19, "arm", [
        ("theta", "f"),
        ("vMax", "f"),
        ("aMax", "f")
        ])

    speed = Packet(20, "arm", [
        ("speed", "f"),
        ("aMax", "f"),
        ("dMax", "f")
        ])

    speedFree = Packet(21, "arm", [
        ("speed", "f")
        ])

    omega = Packet(22, "arm", [
        ("omega", "f"),
        ("aMax", "f"),
        ("dMax", "f")
        ])

    omegaFree = Packet(23, "arm", [
        ("omega", "f")
        ])

    speedOmega = Packet(24, "arm", [
        ("speed", "f"),
        ("omega", "f"),
        ("aDistMax", "f"),
        ("dDistMax", "f"),
        ("aRotMax", "f"),
        ("dRotMax", "f")
        ])

    getX = Packet(30, "arm")
    setX = Packet(31, "arm", [("x", "f")])
    X = Packet(32, "pic", [("x", "f")])

    getY = Packet(33, "arm")
    setY = Packet(34, "arm", [("y", "f")])
    Y = Packet(35, "pic", [("y", "f")])

    getTheta = Packet(36, "arm")
    setTheta = Packet(37, "arm", [("theta", "f")])
    theta = Packet(38, "pic", [("theta", "f")])

    getPos = Packet(39, "arm")
    pos = Packet(40, "pic", [
        ("x", "f"),
        ("y", "f"),
        ("theta", "f")
        ])

    setTicByMeter = Packet(41, "arm", [("tic_by_meter", "I")])
    setSpacing = Packet(42, "arm", [("spacing", "f")])

    odoBroadcastOn = Packet(43, "arm")
    odoBroadcastOff = Packet(44, "arm")
    odoBroadcastToggle = Packet(45, "arm")
    odoDelay = Packet(46, "arm", [("delay", "I")])

    setXTheta = Packet(47, "arm", [("x", "f"), ("theta", "f")])
    setYTheta = Packet(48, "arm", [("y", "f"), ("theta", "f")])
    setXYTheta = Packet(49, "arm", [("x", "f"), ("y", "f"), ("theta", "f")])
    setXY = Packet(50, "arm", [("x", "f"), ("y", "f")])
    
    ########## Message de debut de match et autres (50<n<60)###########

    start = Packet(51, "pic", [("color", "i")])

    ########## Message pour sick (61<n<70)##############

    sick = Packet(61, 'pic', [("id", "B")])
    freepath = Packet(62, 'pic', [("id", "B")])
    sickThreshold = Packet(63, 'arm', [
        ("id", "B"),
        ('threshold', "H")
        ])
    
    ########### Message de lance balles (>70) ############

    launchBalls = Packet(71, "arm", [
        ("amount_left", "H")
        ])
    setBalls = Packet(74, "arm", [
        ("amount", "H")
        ])
    doneLaunch = Packet(72, "pic")
    doneBall = Packet(75, "pic")
    stopLaunch = Packet(73, "arm")
    

class Turret(Proto):
    type = 8
    on = Packet(1, "arm")
    off = Packet(2, "arm")
    getPos = Packet(10, "arm", [
        ("id", "B")
    ])
    pos = Packet(11, "pic", [
        ("id", "B"),
        ("distance", "B"),
        ("angle", "B")
    ])


# Rappel des types struct.pack usuelles :
# B  unsigned char
# H  unsigned short
# I  unsigned int
# b  signed char
# h  signed short
# i  signed int
# f  float
