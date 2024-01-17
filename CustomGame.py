from Assignment3Functions import *
import argparse

parser = argparse.ArgumentParser(description="Enter Options")
parser.add_argument('size', help='size of grid')
parser.add_argument('numtrials', help='number of trials')
parser.add_argument('boardtype', help='Random / Blinker / Glider')
parser.add_argument('animate', help='Animates the simulation (True / False)')
args = parser.parse_args()

RunGame(int(args.size), int(args.numtrials), args.boardtype, args.animate)
input()
