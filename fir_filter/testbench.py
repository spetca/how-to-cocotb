# Simple tests for an adder module
import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge
from scipy.signal import lfilter
import numpy as np

# as a non-generator
def wave(amp, f, fs, smp): 
    sample = int((np.rint(amp*np.sin(2.0*np.pi*f/fs*smp))))
    return sample

def predictor(amp,f,fs,clks):
    coefs = np.array([-1,2,2,-9,-3,38,67,38,-3,-9,2,2,-1])
    clks  = np.arange(0,clks)
    signal = np.rint(amp*np.sin(2.0*np.pi*f/fs*clks))
    output = lfilter(coefs,1.0,signal)
    return output

@cocotb.test()
async def filter_test(dut):
    #initialize
    dut.din.value = 0
    fs = 1000
    amp0 = 60
    f0 = 100
    num_clks = 500

    # sample bit accurate predictor values
    dout_pred = predictor(amp0,f0,fs,num_clks)

    cocotb.start_soon(Clock(dut.clk, 1, units="ms").start())
    
    cnt = 0
    pred_cnt = 0
    # Reset DUT
    dut.reset.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.reset.value = 0

    run_this_many_clocks = num_clks #1clk per ms

    # run through each clock
    for samp in range(run_this_many_clocks-1):
        await RisingEdge(dut.clk)
        # get the output at rising edge
        dut_dout = dut.dout.value.signed_integer
        # feed a new input in
        dut.din.value  = wave(amp0, f0, fs,samp) 

        # wait until reset is over, then start the assertion checking
        if(cnt>1):
            assert dut_dout == dout_pred[pred_cnt], "Adder result is incorrect: %d != %d" % (dut_dout, dout_pred[pred_cnt])
            pred_cnt = pred_cnt+1
        cnt = cnt + 1
        
        

                     

        

