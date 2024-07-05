#############################
FiOWAT
#############################

This package implements the FiOWAT, a new tools for calculating WCET. To use FiOWAT, first you need to install it.

Dependencies
============

FiOWAT package requires:

- Python (>= 3.8)
- freezegun==1.2.2 (Just for tests)
- matplotlib==3.7.1
- numpy==1.24.3
- pandas>=2.0.3
- Pillow==9.5.0
- progress==1.6
- PuLP==2.7.0
- pygad==3.0.1
- pyserial==3.5
- PyYAML==6.0.1
- reportlab==4.0.4
- scipy>=1.1.0
- statsmodels==0.14.0
- z3-solver==4.10.2.0


- LLVM (== 16.0.0)
- CBMC (>= 5.11)


Installation from source
========================

Currently, FiOWAT can only be installed from source via its github repository::
    
    >>> git clone https://github.com/daniel-cin/TCC-PES
    ... cd TCC-PES
    ... pip install -r requirements.txt
    ... pip install .

The LLVM-16 can be installed on Linux using this pipeline::

    >>> wget https://apt.llvm.org/llvm.sh
    ... chmod +x llvm.sh
    ... sudo ./llvm.sh 16 all