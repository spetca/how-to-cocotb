# Simple tests for an adder module
import cocotb
from cocotb.result import TestFailure
import random
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge

async def generate_clock(dut):
    """Generate clock pulses."""
    for cycle in range(20):
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")
    

@cocotb.test()
async def basic_count(dut):
    cocotb.start_soon(Clock(dut.clk, 1, units="ns").start())
    count = 0
    # Reset DUT
    dut.reset.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.reset.value = 0

    for _ in range(50):
        await RisingEdge(dut.clk)
        v_count = dut.count.value
        if v_count.integer != count:
            raise TestFailure(
                "Adder result is incorrect: %s != %s" % (str(dut.count.value), count)) 
        else: # these last two lines are not strictly necessary
            dut.log.info("Ok!")
        count = count + 1
        if(count > 15):
            count = 0

