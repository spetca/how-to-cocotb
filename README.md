# cocotb

This repo is a synoposis on how to use cocotb for absolute idiots. 

## Impetus

As a DSP engineer, I just want to shove a sinusoid through a verilog module most of the time. This repo aims to be a short intro on how to use cocotb to: 

  - setup a clock
  - reset a module
  - assign some configuration ports to particular values
  - shove some interesting data through the module
  
## Dependencies

  - [icarus verilog simulator](http://iverilog.icarus.com/) for simulating verilog
  - [gtkwave](http://gtkwave.sourceforge.net/) for viewing waveforms from simulation
  - python 
    
  ## How to run
  
  All examples contain a make file which can be run by simply typing 
  
  `make`
  
  or 
  
  `make COCOTB_RESOLVE_X=ZEROS`
  
  if you care aboue how X's are returned
