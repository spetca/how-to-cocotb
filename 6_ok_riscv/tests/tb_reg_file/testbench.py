# Simple tests for an fir_filter module
import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge

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

class Driver:
    def __init__(self,dut):
        self.dut = dut

    @cocotb.coroutine
    async def drive(self):
        while True:
            await RisingEdge(self.dut.clk)
            self.dut.write_data_i.value = 5
            self.dut.write_address_i.value = 14
            self.dut.read_addr1_i.value = 14


class OutputMonitor:
    def __init__(self,dut):
        self.dut = dut

    @cocotb.coroutine
    async def monitor(self):
        while True:
            await RisingEdge(self.dut.clk)


@cocotb.test()
async def write_test(dut):
    #initialize
    dut.write_enable_i.value = 1

    reset_clocks = 1 # to ensure we only monitor after resets
    # start clock
    cocotb.start_soon(Clock(dut.clk, 1, units="ms").start())
    
    # Reset DUT
    reset_driver = ResetDriver(dut, reset_clocks)
    cocotb.fork(reset_driver.drive())

    # Reset DUT
    driver = Driver(dut)
    cocotb.fork(driver.drive())

    for samp in range(20):
        await RisingEdge(dut.clk)
        print(dut.read_out1_o.value)
        if(dut.reset.value.is_resolvable):
            if(dut.reset.value==0):
                if(dut.read_out1_o.value.is_resolvable):
                    assert dut.read_out1_o.value == 5, "result is incorrect: %d != %d" % (dut.read_out1_o.value, 5)

        
        
        

                     

        

