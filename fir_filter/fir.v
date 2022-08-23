module fir(clk, din, reset, dout);
input clk; 
input [7:0] din; 
input reset; 
output reg [15:0] dout; 

wire signed [7:0] h0,h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12;
wire signed [15:0] m0,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12; 
wire signed [15:0] q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12; 
wire signed [15:0] a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12;

assign h0 = 2;
assign h1 = 0;
assign h2 = -9;
assign h3 = -10;
assign h4 = 20;
assign h5 = 74;
assign h6 = 102;
assign h7 = 74;
assign h8 = 20;
assign h9 = -10;
assign h10 = -9;
assign h11 = 0;
assign h12 = 2;


assign m12 = h12 * din; 
assign m11 = h11 * din; 
assign m10 = h10 * din; 
assign m9  = h9  * din; 
assign m8  = h8  * din; 
assign m7  = h7  * din; 
assign m6  = h6  * din; 
assign m5  = h5  * din; 
assign m4  = h4  * din; 
assign m3  = h3  * din; 
assign m2  = h2  * din; 
assign m1  = h1  * din; 
assign m0  = h0  * din; 


assign a1  = q1 + m11;
assign a2  = q2 + m10; 
assign a3  = q3 + m9;
assign a4  = q4 + m8; 
assign a5  = q5 + m7;
assign a6  = q6 + m6; 
assign a7  = q7 + m5;
assign a8  = q8 + m4; 
assign a9  = q9 + m3;
assign a10 = q10 + m2; 
assign a11 = q11 + m1;
assign a12 = q12 + m0; 

dff dff1(.clk(clk),  .d(m12),.reset(reset),  .q(q1)); 
dff dff2(.clk(clk),  .d(a1), .reset(reset),  .q(q2)); 
dff dff3(.clk(clk),  .d(a2), .reset(reset),  .q(q3)); 
dff dff4(.clk(clk),  .d(a3), .reset(reset),  .q(q4)); 
dff dff5(.clk(clk),  .d(a4), .reset(reset),  .q(q5)); 
dff dff6(.clk(clk),  .d(a5), .reset(reset),  .q(q6)); 
dff dff7(.clk(clk),  .d(a6), .reset(reset),  .q(q7)); 
dff dff8(.clk(clk),  .d(a7), .reset(reset),  .q(q8)); 
dff dff9(.clk(clk),  .d(a8), .reset(reset),  .q(q9)); 
dff dff10(.clk(clk), .d(a9), .reset(reset),  .q(q10)); 
dff dff11(.clk(clk), .d(a10),.reset(reset),  .q(q11)); 
dff dff12(.clk(clk), .d(a11),.reset(reset),  .q(q12)); 

// passthrough
always @(posedge clk)
      dout <= a12;

// Dump waves
  initial begin
    $dumpfile("dump.vcd");
    $dumpvars(1, fir);
  end
endmodule