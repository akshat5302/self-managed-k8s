import pulumi
import sys
import os

# Add the infrastructure directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'infrastructure'))

# Import and run the main infrastructure
from main import main

if __name__ == "__main__":
    main() 