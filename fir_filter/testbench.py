# Simple tests for an adder module
import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
import numpy as np

# as a non-generator
def wave(amp, f, fs, smp): 
    sample = int((np.rint(amp*np.sin(2.0*np.pi*f/fs*smp))))
    return sample

@cocotb.test()
async def pass_thru_test(dut):
    cocotb.start_soon(Clock(dut.clk, 1, units="ms").start())
    new_sample = 0
    last_sample = 0
    dut.din.value = 0
    
    # Reset DUT
    #dut.reset.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
    #dut.reset.value = 0

    run_this_many_clocks = 500 #1clk per ms
    for samp in range(run_this_many_clocks-1):
        await RisingEdge(dut.clk)
        #dut_dout = dut.dout.value
        new_sample = wave(60, 20, 1000,samp)
        dut.din.value = new_sample; 
        #assert dut_dout.integer == last_sample, "Adder result is incorrect: %d != %d" % (dut_dout.integer, last_sample)
                     

        

