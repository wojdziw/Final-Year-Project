import caffe
import os
import numpy as np
import time

GPU_ID = 1
caffe.set_mode_gpu()
caffe.set_device(GPU_ID)

solver = caffe.get_solver('../models/net1_solver.prototxt')

learningRate = 0.0000000001
epochIter = 200
noEpochs = 10

losses = np.zeros(epochIter*noEpochs)

net2_iteration = -1

for net1_iteration in range(noEpochs*epochIter):

	if ((max(0,net1_iteration-10)/epochIter)%2==0 and net1_iteration>=10):
		while True:
			try:
				net2_data = np.load("../comms/data_conv3p.npy")
			except:
				pass
			else:
				break

		for i in range(data_conv3p.shape[0]):
			solver.net.blobs['conv3p'].data[i] = net2_data[i]

		print "Iteration " + str(net1_iteration) + ": full net1 step"
		# do full sweeps on net1 with fixed conv3p
		solver.step(1)
		# make net2 idle

		while(net1_iteration != net2_iteration):
			time.sleep(5)
			print "waiting..."
			try:
				net2_iteration = int(np.load("../comms/net2_iteration.npy"))
			except:
				pass

	elif ((max(0,net1_iteration-10)/epochIter)%2==1):
		print "Iteration " + str(net1_iteration) + ": idling"
		# run forward prop to get a different minibatch
		solver.net.forward()
		# save that to a file
		data_pool2 = solver.net.blobs['pool2'].data
		np.save('../comms/data_pool2', data_pool2)
		# do full sweeps on net2

		while(net1_iteration != net2_iteration):
			time.sleep(5)
			print "waiting..."
			try:
				net2_iteration = int(np.load("../comms/net2_iteration.npy"))
			except:
				pass

	elif (net1_iteration<10):
		solver.net.forward()

		labels = solver.net.blobs['label'].data
		data_pool2 = solver.net.blobs['pool2'].data

		np.save('../comms/data_pool2', data_pool2)
		np.save('../comms/net1_iteration', net1_iteration)
		np.save('../comms/net1_labels', labels)

		while(net1_iteration != net2_iteration):
			time.sleep(5)
			print "waiting..."
			try:
				net2_iteration = int(np.load("../comms/net2_iteration.npy"))
			except:
				pass

		while True:
			try:
				net2_data = np.load("../comms/data_conv3p.npy")
			except:
				pass
			else:
				break

		for i in range(data_conv3p.shape[0]):
			solver.net.blobs['conv3p'].data[i] = net2_data[i]

		solver.net.backward()
		for layer in solver.net.layers:
	    		for blob in layer.blobs:
	        		blob.data[...] -= learningRate*blob.diff


	np.save('../comms/net1_iteration', net1_iteration)

	losses[net1_iteration] = float(solver.net.blobs['loss'].data)
	np.save('../models/snapshots/net1_losses', losses)
