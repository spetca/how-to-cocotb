# Simple tests for an sinusoid module
import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge,FallingEdge
import numpy as np

# as a non-generator
def wave(amp, f,smp): 
    sample = int((np.rint(120*np.sin(2*np.pi*f/1e3*smp))))
    return sample

@cocotb.test()
async def pass_thru_test(dut):
    # intialize 
    last_sample = 0
    next_sample = 0
    dut.din.value = 0
    cnt_clks = 0
    dut_dout = 0
    run_this_many_clocks = 500
    # start clocks
    cocotb.start_soon(Clock(dut.clk, 1, units="ms").start())
    
    # Reset DUT
    await RisingEdge(dut.clk) # syncrhonize with clock
    dut.reset.value = 0
    for _ in range(20):
        await RisingEdge(dut.clk)
        last_sample = 0
        next_sample = 0
    dut.reset.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
        last_sample = 0
        next_sample = 0
    dut.reset.value = 0

    await RisingEdge(dut.clk)
    # process stuff every rising edge
    for samp in range(run_this_many_clocks-1):
        await RisingEdge(dut.clk)
        if(dut.reset.value==0):
            # get the output at the rising edge
            dut_dout = dut.dout.value.signed_integer
            # does the current dout = the last sample in
            assert dut_dout == last_sample, "sine passthru result is incorrect: DUT: %d != LAST SAMPLE: %d" % (dut_dout, last_sample)
            # this goes after the assertion because last_sample shouldnt update on the first clock? 
            last_sample = next_sample
            # assign din a new value
            next_sample = wave(127, 100,samp)
            dut.din.value = next_sample



       

        

