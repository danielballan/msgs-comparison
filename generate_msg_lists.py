import asyncio
import os
import sys
from bluesky.examples import det, motor, motor1, motor2, MockFlyer, det1, det2
from bluesky.plans import (Count, AbsScanPlan, AbsListScanPlan, DeltaListScanPlan,
                           InnerProductAbsScanPlan, OuterProductAbsScanPlan)


count_with_flyers = Count([det])
count_with_flyers.flyers = [MockFlyer(det, motor, loop=asyncio.new_event_loop())]
mf = count_with_flyers.flyers[0]
mf.root = mf

plans = {'count-one-det': 'Count([det])',
         'count-two-dets': 'Count([det1, det2], 2)',
         'count-with-flyers': 'count_with_flyers',
         'ascan': 'AbsScanPlan([det], motor, 1, 5, 3)',
         'list-scan': 'AbsListScanPlan([det], motor, [1, 3, 8])',
         'dscan-from-8': 'DeltaListScanPlan([det], motor, [1, 3, 8])',
         'inner': 'InnerProductAbsScanPlan([det], 2, motor1, 1, 2, motor2, 10, 20)',
         'outer': 'OuterProductAbsScanPlan([det], motor1, 1, 2, 2, motor2, 10, 20, 2, '
                                  'False)'}


def main(path):
    for name, plan in plans.items():
        with open(os.path.join(path, name), 'w') as f:
            f.write(plan + "\n")
            for msg in list(eval(plan)):
                if 'group' in msg.kwargs:
                    msg.kwargs['group'] = 'PLACEHOLDER'
                f.write(repr(msg) + "\n")

    
if __name__ == '__main__':
    main(sys.argv[1])
