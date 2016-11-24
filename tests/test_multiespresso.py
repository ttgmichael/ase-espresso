
from espresso import Espresso, Multiespresso

from ase.build import molecule
from ase.neb import NEB
from ase.optimize.fire import FIRE as QuasiNewton

# Optimise molecule
initial = molecule('C2H6')
initial.set_calculator(EMT())
relax = QuasiNewton(initial)
relax.run(fmax=0.05)

# Create final state
final = initial.copy()
final.positions[2:5] = initial.positions[[3, 4, 2]]

# Generate blank images
images = [initial]

for i in range(9):
    images.append(initial.copy())

for image in images:
    image.set_calculator(Espresso())

images.append(final)

# Run IDPP interpolation
neb = NEB(images)
neb.interpolate()

# Run NEB calculation
qn = QuasiNewton(neb, trajectory='ethane_linear.traj',
                 logfile='ethane_linear.log')
qn.run(fmax=0.05)
