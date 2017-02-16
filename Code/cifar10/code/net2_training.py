import caffe
import os
import numpy as np
import time

GPU_ID = 2
caffe.set_mode_gpu()
caffe.set_device(GPU_ID)

solver = caffe.SGDSolver('../models/net2_solver.prototxt')

epochIter = 100
noEpochs = 20

losses = np.zeros(epochIter*noEpochs)

net1_iteration = -1
np.save('../comms/net1_iteration', net1_iteration)
np.save('../comms/net2_iteration', -1)

for net2_iteration in range(epochIter*noEpochs):

	if ((max(0,net2_iteration-10)/epochIter)%2==0 and net2_iteration>=10):
		print "Iteration " + str(net2_iteration) + ": idling"

		while(net1_iteration != net2_iteration):
			# tiny delay to prevent accessing an open file
			time.sleep(5)
			print "waiting..."
			try:
				net1_iteration = int(np.load("../comms/net1_iteration.npy"))
			except:
				pass

	else:

		# We can only start an iteration once we have data ready from net1
		while(net1_iteration != net2_iteration):
			# tiny delay to prevent accessing an open file
			time.sleep(5)
			print "waiting..."
			try:
				net1_iteration = int(np.load("../comms/net1_iteration.npy"))
			except:
				pass

		# loading the parameters from net1
		while True:
			try:
				data_pool2 = np.load("../comms/data_pool2.npy")
				labels = np.load("../comms/net1_labels.npy")
			except:
				pass
			else:
				break

		net = solver.net
		net.set_input_arrays(data_pool2,labels)

		# run forward and back prop
		solver.step(1)

	data_conv3p = solver.net.blobs['conv3p'].data
	np.save("../comms/data_conv3p", data_conv3p)

	losses[net2_iteration] = float(solver.net.blobs['loss'].data)
	np.save('../models/snapshots/net2_losses', losses)

	if net2_iteration%100==0:
		solver.net.save('../models/snapshots/net2_iter_'+str(net1_iteration)+'.caffemodel')

	print "Iteration " + str(net2_iteration) + "; Loss is: " + str(float(solver.net.blobs['loss'].data))

	np.save('../comms/net2_iteration', net2_iteration)
