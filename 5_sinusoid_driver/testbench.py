# Simple tests for an fir_filter module
import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge
from scipy.signal import lfilter
import numpy as np

class ResetDriver:
    def __init__(self,dut, reset_clock):
        self.dut = dut
        self.reset_clock = reset_clock
        self.clock_count = 0

    @cocotb.coroutine
    async def drive(self):
        while True:
            await RisingEdge(self.dut.clk)
            if(self.clock_count == self.reset_clock):
                self.dut.reset.value = 1
            else:
                self.dut.reset.value = 0
            self.clock_count += 1

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
    def __init__(self,dut,reset_clock):
        self.dut = dut
        self.reset_clock = reset_clock
        self.clock_count = 0
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
            # dont assert if reset is unresolvable, or we are currently in reset, or we havent reached
            # the reset clcok
            if(self.dut.reset.value.is_resolvable):
                if(self.dut.reset.value.integer == 0):
                    if(self.clock_count > self.reset_clock):
                        dut_dout = self.dut.dout.value.signed_integer
                        assert dut_dout == self.predict[self.pred_cnt], "filter result is incorrect: %d != %d" % (dut_dout, self.predict[self.pred_cnt])
                        self.pred_cnt = self.pred_cnt+1
            self.clock_count = self.clock_count + 1


@cocotb.test()
async def filter_test(dut):
    #initialize
    dut.din.value = 0
    dut.reset.value = 0
    reset_clocks = 10 # to ensure we only monitor after resets
    # start clock
    cocotb.start_soon(Clock(dut.clk, 1, units="ms").start())
    
    # Reset DUT
    reset_driver = ResetDriver(dut, reset_clocks)
    cocotb.fork(reset_driver.drive())

    # start input driver
    driver = SineDriver(dut)
    cocotb.fork(driver.drive())

    # start the output monitor, but only monitor after reset
    monitor = OutputMonitor(dut,reset_clocks)
    cocotb.fork(monitor.monitor())

    run_this_many_clocks = 500 #1clk per ms
    # run through each clock
    for samp in range(run_this_many_clocks-1):
        await RisingEdge(dut.clk)

        
        
        

                     

        

