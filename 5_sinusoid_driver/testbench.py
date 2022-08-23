# Simple tests for an fir_filter module
import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge
from scipy.signal import lfilter
import numpy as np


# driver class
class SineDriver:
    def __init__(self,dut):
        self.dut = dut
        self.f = 100
        self.fs = 1000
        self.amp = 60
        self.clk_cnt = 0
    def sample(self):
        return int((np.rint(self.amp*np.sin(2.0*np.pi*self.f/self.fs*self.clk_cnt))))

    @cocotb.coroutine
    async def drive(self):
        while True:
            await RisingEdge(self.dut.clk)
            print(self.clk_cnt, self.dut.din.value)
            self.dut.din.value = self.sample()
            self.clk_cnt += 1

class OutputMonitor:
    def __init__(self,dut):
        self.dut = dut
        self.predict = 0
        self.cnt = 0
        self.pred_cnt = 0
        self.fs = 1000
        self.amp = 60
        self.f = 100
        self.num_clks = 500
        self.coefs = np.array([-1,2,2,-9,-3,38,67,38,-3,-9,2,2,-1])
        self.clks  = np.arange(0,self.num_clks)
        self.signal = np.rint(self.amp*np.sin(2.0*np.pi*self.f/self.fs*self.clks))
        self.predict = lfilter(self.coefs,1.0,self.signal)
        print(self.predict)

    @cocotb.coroutine
    async def monitor(self):
        while True:
            await RisingEdge(self.dut.clk)

            # wait until reset is over, then start the assertion checking
            if(self.dut.reset.value.integer==0):
                if(self.cnt > 1):
                    dut_dout = self.dut.dout.value.signed_integer
                    assert dut_dout == self.predict[self.pred_cnt], "Adder result is incorrect: %d != %d" % (dut_dout, self.predict[self.pred_cnt])
                    self.pred_cnt = self.pred_cnt+1
            self.cnt = self.cnt + 1


@cocotb.test()
async def filter_test(dut):
    #initialize
    dut.din.value = 0
    
    # start clock
    cocotb.start_soon(Clock(dut.clk, 1, units="ms").start())
    
    # Reset DUT
    dut.reset.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.reset.value = 0

    # start input driver
    driver = SineDriver(dut)
    cocotb.fork(driver.drive())

    # start the output monitor 
    monitor = OutputMonitor(dut)
    cocotb.fork(monitor.monitor())

    run_this_many_clocks = 500 #1clk per ms
    # run through each clock
    for samp in range(run_this_many_clocks-1):
        await RisingEdge(dut.clk)

        
        
        

                     

        

