import sys

from pylint.lint import Run

min_score = 10

results = Run(['driloader', 'tests'], exit=False)
global_note = results.linter.stats['global_note']

if global_note >= min_score:
    print('Minimum score reached! min_score = {}'.format(str(min_score)))
else:
    print('Minimum score not reached! min_score = {}'.format(str(min_score)))
    sys.exit(1)
