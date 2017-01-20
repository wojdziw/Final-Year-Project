import numpy as np
import matplotlib.pyplot as plt
import os.path

printDual = os.path.isfile("../models/snapshots/net1_losses.npy")
printSingle = os.path.isfile("../models/snapshots/net12_losses.npy")

if printDual:

	y1 = np.load("../models/snapshots/net1_losses.npy")
	y2 = np.load("../models/snapshots/net2_losses.npy")

	x = range(y1.shape[0])

	plt.figure(1)

	plt.subplot(311)
	plt.plot(x, y1)
	plt.yscale('log')
	plt.title('Net1 losses', fontsize=10)
	plt.grid(True)


	plt.subplot(312)
	plt.plot(x, y2)
	plt.yscale('linear')
	plt.ylim(0.58, 1)
	plt.title('Net2 losses', fontsize=10)
	plt.grid(True)

if printSingle:

	y3 = np.load("../models/snapshots/net12_losses.npy")

	x = range(y3.shape[0])

	plt.subplot(313)
	plt.plot(x, y3)
	plt.yscale('linear')
	plt.ylim(0, 3)
	plt.title('Net12 losses', fontsize=10)
	plt.grid(True)

# plt.show()
plt.savefig('../images/losses.png', fontsize=10)
plt.close()
