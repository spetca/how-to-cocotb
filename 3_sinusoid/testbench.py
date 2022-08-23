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
    dut.din.value = 0
    cnt_clks = 0
    dut_dout = 0

    # start clocks
    cocotb.start_soon(Clock(dut.clk, 1, units="ms").start())
    
    # Reset DUT
    dut.reset.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.reset.value = 0

    run_this_many_clocks = 500
    # process stuff every rising edge
    for samp in range(run_this_many_clocks-1):
        await RisingEdge(dut.clk)
        dut_dout = dut.dout.value.signed_integer
        assert dut_dout == last_sample, "Adder result is incorrect: %d != %d" % (dut_dout, last_sample)
        last_sample = dut.din.value.signed_integer
        dut.din <= wave(127, 100,samp)



       

        

