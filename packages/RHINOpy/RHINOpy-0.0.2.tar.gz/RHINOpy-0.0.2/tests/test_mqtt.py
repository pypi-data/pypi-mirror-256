import sys
sys.path.append("E:\\Moritz\\OneDrive\\Projekt_RHINO\\RHINOpy")
import RHINOpy as rp
import time
import numpy as np


MAX_FPS = 60
TIME = 1 / MAX_FPS



# p = rp.MQTTPublisher(rp.urlVAL)
# t = time.time()
# for q in np.linspace(0, 10 * np.pi, 1000):

#     p.publish("RHINO/TM5/q0", str(q))

#     e = time.time() - t
#     time.sleep(TIME)


# rds = rp.RHINODigTwin
# p = rp.MQTTWrapperPublish(rp.urlVAL, rds)

# for q in np.linspace(0, 2 * np.pi, 1000):

#     ld90 = rp.LD90Pose(q*200,q * 500,0)
#     tm5 = rp.TM5Joints([q,0,q,0,0,0])
#     r = rp.RHINODigTwin(ld90, tm5)

#     p.publish(r)

#     time.sleep(TIME)

# print("finished")


# m = rp.MQTTReceiverPoll(rp.ipIOT, "RHINO/LD90/x")
# print(m.receive())


# m = rp.MQTTWrapperRP(rp.ipIOT, rp.LD90Pose)
# print(m.start())


# rp.MQTTPassthrough(rp.ipIOT, rp.urlVAL, "RHINO/#") 