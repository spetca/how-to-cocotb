# Simple tests for an adder module
import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
def adder_basic_test(dut):
    """Test for 5 + 10"""
    yield Timer(2)
    
    dut.A = 5 
    dut.B = 10
    
    yield Timer(2)
    
    assert dut.X == 15, "Adder result is incorrect: %s != 15" % str(dut.X)


@cocotb.test()
def adder_randomised_test(dut):
    """Test for adding 2 random numbers multiple times"""
    yield Timer(2)
    
    for i in range(10):
        A = random.randint(0, 15)
        B = random.randint(0, 15)
        
        dut.A = A
        dut.B = B
        
        yield Timer(2)
        
        # check to make sure DUT == Predictor
        assert dut.X == (A+B), "Randomised test failed with: %s + %s = %s" % (dut.A, dut.B, dut.X)
       
