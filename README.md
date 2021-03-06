# PyChain
Catanane Chain Building Script

Kevin Feezel
University of Akron

How to Run:

	Option 1: Prompts
	
		Syntax: python pychain.py
	
	Option 2: Input File
		
		Syntax: python pychain.py *pychain input filename*
	
		Notes:
		
		- Line numbers matter in the upper section of the pychain_input file ("-=-=-=" divide the sections)
		- Line numbers do not matter in the middle section, the code indexes based on "Chains" if identical or "Chain_1" (whatever number) if non-identical
		
		- Assure that only one space lies between the distance and number of points when specifying parameters
		
		- The number of chains specified in the top section of the script will override the the number of parameters specified in the middle section of the input file.
		- If non-identical is specified and (for example) the script is set to build 2 chain links, if 4 (for example) chain parameters are entered with correct formatting- 
			the script will only build 2 chains with the first two sets of parameters.


Scope:		
	
	This script will create uniform, or non-uniform, 3D circular catanane chains.  These chains are not connected; the edge points are placed at the mid-point of R, or the diameter, if a chain is adjacent. 

	- The chains can be placed on the x,y, or z axis as specified during input.
	- The number of atoms per link and the number of links in the chain are also parameters.
		- Links are the interlocking circular parts that compose the chain. 
	- The distance between atoms is also a parameter assigned during input. 
		
	The outptut is a lammpsdata file.


Suggestions:

	If you have any questions, comments, or suggestions on how to modify this code, please direct them to kaf128@zips.uakron.edu
	

Acknowledgement:

	If this code is used, in whole or part, in research and/or a publication, please acknowledge with author's name and university: Kevin Feezel (University of Akron) .
		
	If this code is used, in whole or part, to create other scripts or added to a library, please credit the author.
