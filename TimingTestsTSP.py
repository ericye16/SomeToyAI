#!/usr/bin/env python
# timing tests for travelling salesman

from __future__ import print_function
import timeit
import TravellingSales

bruteForce = timeit.timeit('TravellingSales.bruteForce()',
                           'from __main__ import TravellingSales',
                           number = 1000)

HeldKarpDynamic = timeit.timeit('TravellingSales.HeldKarpDynamic()',
                                'from __main__ import TravellingSales',
                                number = 1000)

print('Brute force: %f' % bruteForce)
#1.289

print('Held-Karp Dynamic: %f' % HeldKarpDynamic)
#0.036
