from world import World
from vision import Vision
from decision import DecisionMaker
import sys

world = World()

error = False
if len(sys.argv) >= 3:
    if sys.argv[1] == 'true':
        debug_mode = True
    elif sys.argv[1] == 'false':
        debug_mode = False
    else:
        error = True
    try:
        image_width = int(sys.argv[2])
    except:
        error = True
if len(sys.argv) < 3 or error is True:
    debug_mode = False
    image_width = 600

vision = Vision(0, image_width, debug_mode, world)

decision_maker = DecisionMaker(world)

try:
    while True:
        vision.update()

        decision_maker.make_decision()
except:
    vision.finish()
    decision_maker.finish()
