# Simple tests for an adder module
import cocotb
from cocotb.result import TestFailure
import random
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge
import numpy as np
from fxpmath import Fxp

# as a non-generator
def wave(amp, f,smp): 
    sample = int((np.rint(120*np.sin(2*np.pi*f/1e3*smp))))
    return sample

@cocotb.test()
async def basic_count(dut):
    cocotb.start_soon(Clock(dut.clk, 1, units="ms").start())
    count = 0
    sample = 0
    new_sample = 0
    last_sample = 0
    dut.din.value = 0
    # Reset DUT
    dut.reset.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.reset.value = 0

    run_this_many_clocks = 500#1clk per ms
    for samp in range(run_this_many_clocks-1):
        await RisingEdge(dut.clk)
        dut_dout = dut.dout.value
        last_sample = new_sample
        new_sample = wave(127, 100,samp)
        print(new_sample,last_sample, dut_dout.integer)
        dut.din.value = new_sample; 
        #assert dut_dout.integer == last_sample, "Adder result is incorrect: %d != %d" % (dut_dout.integer, last_sample)
                     

        

