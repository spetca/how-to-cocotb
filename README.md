# cocotb for absolute idiots

So you read all of 2 free websites on SystemVerilog. You looked through the convoluted mess of documentaiton that is UVM. Feeling dumb? Me too. I think [cocotb](https://docs.cocotb.org/en/stable/) is here to save us, but even cocotb is still a little over my head since I don't work in python everyday. 

This repo is a synoposis on how to use cocotb for absolute idiots. Or, perhaps, how to use cocotb as a signal processing engineer. 

As a DSP engineer, you probably just want to shove a sinusoid through a verilog module and check the output. This repo aims to be a short intro on how to do that - how to do "easy" things like:

  - setup a clock
  - reset a module
  - assign some configuration ports to particular values
  - shove some interesting data through the module
  - check that the data out is correct
  
 Eventually, we will work towards more complicated things and maybe one day even figure out how to do everything the *right* way. 
  
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

## Description of Each Directory

### 1. adder
  
  This is the adder example from cocotb repo that just performs A+B. The main benefit here is an example of how to use the makefile to attach your verilog module and simulator. 
  
### 2. counter

This is just a verilog module that increments a signal +1 every clock. This example demos how to reset a module at the beginning of a sim. See testbench lines `14-17`

### 3. sinusoid

This is a super simple verilog module that passes through a sinusoid delayed by one clock. This example demos how to push a sine wave through your testbench. Not sure if there is a better way to do this. Please advise if you know.

### 4. fir_filter

Similar to sinusoid, but with a more complex verilog module. 

### 5. simple_driver

a more complex class based driver that utilizes `fork`. This also contains an example of creating a monitor class as well. Currently this is a bit of a mess and if you have some advice on how to better implement things please put the advice in the issues of this repo

### 6. configurable_fir

TODO similar to **4**, but with configuration ports. 
