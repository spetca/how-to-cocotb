module sine(clk, reset, din, dout);
input clk; 
input signed [7:0] din; 
input reset; 
output signed [7:0] dout; 
reg signed [7:0] dout_reg = 7'b0; 

// passthrough
always @(posedge clk)
begin
    if(reset) 
        dout_reg <= 0;
    else 
        dout_reg <= din;
end
    
assign dout = dout_reg;

// Dump waves
  initial begin
    $dumpfile("dump.vcd");
    $dumpvars(1, sine);
  end
endmodule