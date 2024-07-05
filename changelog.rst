FioWAT changelog
================

This document describes notable changes to the FioWAT.


1.0.0 - 2023.11.13
-------------------

Added architecture support:

* Initial support for x86_64 in Static IPET, but with non accurate instructions weight


Changed:

* FioWAT run faster because this code was refactored
* The Constraint Solver use owner opt pass to map the IR code to internal graph
* EVT analysis added
* Dynamic GA analysis added
* WPEVT analysis added


Fixed:

* Bugs in loop analyzer
* Bug in IPET


0.9.0 - 2023.08.20
-------------------

Added architecture support:

* Support for AVR in Static and Dynamic analysis


Changed:

* Constraint Solver use LLVM code coverage to map the execution with worst path
* Static IPET analysis added
* Hybrid IPET analysis added
* Input Generator added


Fixed:

* Bugs in Constraint Solver using ".lcov file"