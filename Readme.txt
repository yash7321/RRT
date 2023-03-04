1.To run the python script,initially create a virtual environment to download the required external modules

Install pip first 
Command for installing pip - sudo apt-get install python3-pip


Now create a virtual environment
Use the command - python3 -m venv myenv 

myenv is just the name of the virtual environment,you can use any name 

Activate the virtual environment
Use the command - source myenv/bin/activate

where source is the location of the directory in which myenv is present

Now use the command - pip install -r requirements.txt 
to download the required modules

Now Use  the command -  python3 index.py  in the same command prompt where virtual environment is active to run the file 


Input Specifications:

An example of giving inputs to the above python code

Enter Start Point - Provide X and Y Coordinate 0 0
Enter Final Point - Provide X and Y Coordinate 8 8
Enter Number of Obstacles to be placed 3
2 2 1
5 5 1
8 1 1
Enter Maximum X Coordinate 10
Enter Maximum Y Coordinate 10
Enter Step Size Value 0.5


For the simplicity purposes we are assuming that all the obstacles are circle in shape and each obstacle is denoted by their center of circle coordinates and its radius
In the above inputs we have given 3 obstacles and next 3 lines were for the description of each obstacle
The first line 2 2 1 denotes that the obstacle center is at (2,2) and the radius of circle is 1

We are assuming that the starting and final point lies in the first quadrant to reduce the work space in which we have to explore.