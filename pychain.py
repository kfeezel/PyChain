#!/bin/usr/python

#   PyChain - Catanane Chain Builder
#   Kevin Feezel
#   University of Akron
#   2018
#
#	 command line syntax: python pychain2-4.py *input_file*
#
#	 if no input file is specified, it will prompt for user input
#  
#  if pychain_input file format is not used, the script may not work correctly
#
#  Please check the readme for more information

import math
import sys
import os
import time

__title__ = 'PyChain - Catanane Chain Builder'
__version__ = '2.6'
__author__ = 'Kevin Feezel'
__university__ = 'University of Akron'
__copywrite__ = '2018'

def main():
	
	global num_chains
	global identical
	global axis
	global length

	print('\n%s\n%s\n%s\n%s\n' % (__title__,__author__,__university__,__copywrite__))

	#print("""\nNotes:
	#Greater than 5 points per chain link is recommended.\n""")

	if len(sys.argv) == 2: #input file
		input_ = []

		input_file = open("pychain_input", "r")
		all_ = input_file.read()
		all_input = all_.split('\n')

		with input_file as i:
			for line in all_input:
				input_.append(str((line.split(" "))))

		input_ = input_[:-3]

		params = []

		for each in input_:
			each = each.strip('[]"\/,')
			each = each.strip("''")
			params.append(each)

		if (params[9].lower() == "x"):
			axis = 1
		elif (params[9].lower() == "y"):
			axis = 2
		elif (params[9].lower() == "z"):
			axis = 3
		else:
			print("Please check the 'axis' value. It should be X, Y, or Z.")

		#identical
		if (params[6].lower() == "y"):
			identical = True
		elif (params[6].lower() == "n"):
			identical = False
		else:
			print("\nPlease check the 'identical' value.  It should be Y/N.")
			sys.exit()

		#num_chains
		num_chains = int(params[3])

		#Chain link parameters
		chain_index = 1

		ni_params = []
		if identical == False:
			while chain_index <= num_chains:
				index_ = params.index("Chain_%i" % (chain_index))
				ind = index_ + 1
				param = params[ind]
				new_param = ''.join( char for char in param if char not in "''," )
				ni_params.append("%s" % (new_param))
				chain_index += 1

		elif identical == True:
			index_ = params.index("Chains")
			ind = index_ + 1
			param = params[ind]
			new_param = ''.join( char for char in param if char not in "''," )
			while chain_index <= num_chains:
				ni_params.append("%s" % (new_param))
				chain_index += 1

		valid = True

	elif len(sys.argv) == 1: #user input

		num_chains = input("How many links compose the chain? : ")
		try:
			num_chains = int(num_chains)
		except:
			print("Please enter an integer for the number of chains in the system.")


		identical = input("Are the links identical? ~ Y or N : ")
		identical = identical.lower()
		if (identical == "y"):
			valid = True
			identical = True
			chain_num = 1
			ni_params = []

			length = input("What is the distance between points? (A) : ")
			try:
				length = float(length)
			except:
				print("Please enter a valid number for the length between points.")

			num_points = input("How many points compose one chain \"link\"? : ")
			try:
				num_points = int(num_points)
			except:
				print("Please enter an integer for the number of points per chain.")

			i__t = 0 #iteration variable
			while i__t < num_chains:
				ni_params.append("%f %i" % (length, num_points))
				chain_num += 1
				i__t += 1

		elif (identical == "n"):
			valid = True
			identical = False
			chain_num = 1
			ni_params = []
			while chain_num <= num_chains:
				try:
					length = float(input("What is the distance between points on chain link #%i? (A) : " % (chain_num)))
				except:
					print("Please enter a valid number for the length between points.")
				try:
					num_points = int(input("How many points compose chain \"link\" #%i? : " % (chain_num)))
				except:
					print("Please enter a valid whole number for the number of links.")

				ni_params.append("%f %i" % (length, num_points))
				chain_num += 1

		else:
			print("Please enter Y or N., These chains are assumed to be identical now.")
			identical = True
			length = input("What is the distance between points? (A) : ")
			try:
				length = float(length)
			except:
				print("Please enter a valid number for the length between points.")

			num_points = input("How many points compose one chain \"link\"? : ")
			try:
				num_points = int(num_points)
			except:
				print("Please enter an integer for the number of points per chain.")


		raw_axis = input("What axis would you like the chain to be on? : ")
		if raw_axis.lower() == "x":
			axis = 1
		elif raw_axis.lower() == "y":
			axis = 2
		elif raw_axis.lower() == "z":
			axis = 3

	else: 
		print("\nToo many command line arguments, please check %s for instructions on how to execute this code." % (os.path.basename(__file__)))
		return None
	
	start_time = time.time()
	
	#I/O
	cout = open("cantanane.lammpsdata", "w")
	cout.close()
	cout = open("cantanane.lammpsdata", "a")

	#variables
	first = True
	global output
	output = []
	global bond_types
	bond_types = []
	global angle_types
	angle_types = []

	global angle_type_id
	angle_type_id = 1

	global identical_type_toggle
	identical_type_toggle = False
	global identical_type_toggle_a
	identical_type_toggle_a = False

	def build_chain_templates(length,num_points):
		#maths
		inner_angle = float((360 / num_points)*(math.pi/180))
		other_angles = float(((180 - inner_angle) / 2)*(math.pi/180))
		angle_ = 360 / num_points
		global angle_type_id
		global identical_type_toggle_a
		if identical_type_toggle_a == False:
			angle_types.append("%i %f" % (angle_type_id,angle_))
			angle_type_id += 1
		if identical == True:
			identical_type_toggle_a = True

		#the 2 angles that form the triangle between 2 points and the center
		global R
		R = length / (2*(math.sin(math.pi / num_points)))
		#like the radius


		#define arrays to be used

		global vchain_x
		global vchain_y
		global vchain_z
		vchain_x = []
		vchain_y = []
		vchain_z = []

		global hchain_x
		global hchain_y
		global hchain_z
		hchain_x = []
		hchain_y = []
		hchain_z = []

		#for testing
		#global xyz_out
		#xyz_out = []

		#variables used in this while loop
		iteration = 0
		quadrent = 1

		while iteration < num_points:

			a = inner_angle*int(iteration)

			x_delta = (math.sin(a) * R)
			yz_delta = (math.cos(a) * R)

			x = 0 - x_delta
			#vertical
			vy = 0 - yz_delta
			vz = 0
			#horizontal
			hy = 0
			hz = 0 - yz_delta

			vchain_x.append(x)
			vchain_y.append(vy)
			vchain_z.append(vz)

			hchain_x.append(x)
			hchain_y.append(hy)
			hchain_z.append(hz)
			iteration += 1

			#test_out_h.write("\nC %f %f %f" % (x, hy, hz))
			#test_out_v.write("\nC %f %f %f" % (x, vy, vz))


	global bonds
	bonds = []
	global angles
	angles = []

	if valid == True:
		#variables
		chain_id = 1
		total_atoms = 0
		p_id = 1
		b_id = 1

		for each in ni_params:
			n = each.split()
			n[1] = int(n[1])
			total_atoms += n[1]

		center_calc_x = []

		for param in ni_params:
			new_ = param.split()
			new_[0] = float(new_[0])
			new_[1] = int(new_[1])
			num_points_ = new_[1]
			length_ = new_[0]
			#length, num_points
			build_chain_templates(new_[0],new_[1])

			if identical == True:
				type_ = 1
			elif identical == False:
				type_ = chain_id

			if first == True:
				add_ = 0
				first = False
			elif first == False:
				add_ = (float(max(center_calc_x))) - (old_R/3) + R #distance from 0,0,0 to vertical chain link center


			if chain_id % 2 == 0:
				p_it = 0 #iteration number
				first_ = True #first bond
				first_a = True #first angle
				last_a = False #last angle
				while p_it < new_[1]:
					if axis == 1:
						x = float(vchain_x[p_it]) + add_
						y = float(vchain_y[p_it])
						z = float(vchain_z[p_it])
						center_calc_x.append(x)
					elif axis == 2:
						x = float(vchain_y[p_it])
						y = float(vchain_x[p_it]) + add_
						z = float(vchain_z[p_it])
						center_calc_x.append(y)
					elif axis == 3:
						x = float(vchain_z[p_it])
						y = float(vchain_y[p_it])
						z = float(vchain_x[p_it]) + add_
						center_calc_x.append(z)

					if p_it == (num_points_-1): #determines if last angle
						last_a = True

					if first_a == True:
						a_1 = p_id + (num_points_ - 1)
						a_2 = p_id
						a_3 = p_id + 1
						first_a = False
						angles.append("%i %i %i %i %i" % (p_id, type_, a_1, a_2, a_3))
					elif last_a == True:
						a_1 = p_id - 1
						a_2 = p_id
						a_3 = p_id - (num_points_-1)
						angles.append("%i %i %i %i %i" % (p_id, type_, a_1, a_2, a_3))
					elif (first_a == False) and (last_a == False):
						a_1 = p_id - 1
						a_2 = p_id
						a_3 = p_id + 1
						angles.append("%i %i %i %i %i" % (p_id, type_, a_1, a_2, a_3))

					output.append("%i %i %i %i %f %f %f" % (p_id, chain_id, type_, 0, x, y, z))
					if first_ == False:
						a_ = p_id-1
						b_ = p_id
						bonds.append("%i %i %i %i" % (b_id, type_, a_, b_,))
						b_id += 1
					elif first_ == True:
						a_ = (p_id + num_points_) - 1
						b_ = p_id
						bonds.append("%i %i %i %i" % (b_id, type_, a_, b_,))
						b_id += 1
					p_id += 1
					p_it += 1
					first_ = False

				if identical_type_toggle == False:
					bond_types.append("%i %f" % (chain_id, length_))
				if identical == True:
					identical_type_toggle = True
				chain_id += 1
			else:
				p_it = 0 #iteration number
				first_ = True #first bond
				first_a = True #first angle
				last_a = False #last angle
				while p_it < new_[1]:
					if axis == 1:
						x = float(hchain_x[p_it]) + add_
						y = float(hchain_y[p_it])
						z = float(hchain_z[p_it])
						center_calc_x.append(x)
					elif axis == 2:
						x = float(hchain_y[p_it])
						y = float(hchain_x[p_it]) + add_
						z = float(hchain_z[p_it])
						center_calc_x.append(y)
					elif axis == 3:
						x = float(hchain_z[p_it])
						y = float(hchain_y[p_it])
						z = float(hchain_x[p_it]) + add_
						center_calc_x.append(z)

					if p_it == (num_points_-1): #determines if last angle
						last_a = True

					if first_a == True:
						a_1 = p_id + (num_points_ - 1)
						a_2 = p_id
						a_3 = p_id + 1
						first_a = False
						angles.append("%i %i %i %i %i" % (p_id, type_, a_1, a_2, a_3))
					elif last_a == True:
						a_1 = p_id - 1
						a_2 = p_id
						a_3 = p_id - (num_points_-1)
						angles.append("%i %i %i %i %i" % (p_id, type_, a_1, a_2, a_3))
					elif (first_a == False) and (last_a == False):
						a_1 = p_id - 1
						a_2 = p_id
						a_3 = p_id + 1
						angles.append("%i %i %i %i %i" % (p_id, type_, a_1, a_2, a_3))

					output.append("%i %i %i %i %f %f %f" % (p_id, chain_id, type_, 0, x, y, z))
					if first_ == False:
						a_ = p_id-1
						b_ = p_id
						bonds.append("%i %i %i %i" % (b_id, type_, a_, b_,))
						b_id += 1
					elif first_ == True:
						a_ = (p_id + num_points_) - 1
						b_ = p_id
						bonds.append("%i %i %i %i" % (b_id, type_, a_, b_,))
						b_id += 1
					first_ = False
					p_id += 1
					p_it += 1
				if identical_type_toggle == False:
					bond_types.append("%i %f" % (chain_id, length_))
				if identical == True:
					identical_type_toggle = True
				chain_id += 1
			old_R = R

	#Output

		cout.write("""PYCHAIN LAMMPSDATA FILE

		%i atoms
		%i bonds
		%i angles
		0 dihedrals
		0 impropers

		%i atom types
		%i bond types
		%i angle types
		""" % (total_atoms, len(bonds), len(angles),type_, len(bond_types),len(angle_types)))

		#cout.write("\n\nMasses\n")

		#cout.write("\n\nBOND COEFFS\n")

		#for bt in bond_types:
			#cout.write("\n%s" % (bt))

		#cout.write("\n\nANGLE COEFFS\n")

		#for at in angle_types:
			#cout.write("\n%s" % (at))

		cout.write("\n\nAtoms\n")

		for a in output:
			cout.write("\n%s" % (a))

		cout.write("\n\nBonds\n")

		for b in bonds:
			cout.write("\n%s" % (b))

		cout.write("\n\nAngles\n")

		for c in angles:
			cout.write("\n%s" % (c))

	cout.close()
	
	end_time = time.time()
	
	duration = end_time-start_time
	
	if duration < 60:
		unit = 'seconds'
	elif duration < 3600:
		duration = (duration/60)
		unit = 'minutes'
	else:
		duration = ((duration)/60)/60
		unit = 'hours'
	
	print("\nFinished creating catanane chains in: %f %s." % (duration, unit))
	
if __name__ == '__main__': 

	main()
