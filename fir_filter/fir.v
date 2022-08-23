module fir(clk, din, reset, dout);

input clk; 
input signed [7:0] din; 
input reset; 
output signed [15:0] dout; 
reg    signed [15:0] dout_reg;

// coefficients
wire  signed [7:0]  h0,h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12;
// multiplies
wire  signed [15:0] m0,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12; 
// taps delays
wire  signed [15:0] q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12; 
// adders
wire  signed [15:0] a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12;

// coeffs definition
assign h0  = 0;
assign h1  = 0;
assign h2  = 0;
assign h3  = 0;
assign h4  = 0;
assign h5  = 0;
assign h6  = 1;
assign h7  = 0;
assign h8  = 0;
assign h9  = 0;
assign h10 = 0;
assign h11 = 0;
assign h12 = 0;

// each multiply in the chain
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

// each add in the chain
assign a1  = q1  + m11;
assign a2  = q2  + m10; 
assign a3  = q3  + m9;
assign a4  = q4  + m8; 
assign a5  = q5  + m7;
assign a6  = q6  + m6; 
assign a7  = q7  + m5;
assign a8  = q8  + m4; 
assign a9  = q9  + m3;
assign a10 = q10 + m2; 
assign a11 = q11 + m1;
assign a12 = q12 + m0; 

// delay line
dff dff1( .clk(clk), .reset(reset),.d(m12), .q(q1)); 
dff dff2( .clk(clk), .reset(reset),.d(a1),  .q(q2)); 
dff dff3( .clk(clk), .reset(reset),.d(a2),  .q(q3)); 
dff dff4( .clk(clk), .reset(reset),.d(a3),  .q(q4)); 
dff dff5( .clk(clk), .reset(reset),.d(a4),  .q(q5)); 
dff dff6( .clk(clk), .reset(reset),.d(a5),  .q(q6)); 
dff dff7( .clk(clk), .reset(reset),.d(a6),  .q(q7)); 
dff dff8( .clk(clk), .reset(reset),.d(a7),  .q(q8)); 
dff dff9( .clk(clk), .reset(reset),.d(a8),  .q(q9)); 
dff dff10(.clk(clk), .reset(reset),.d(a9),  .q(q10)); 
dff dff11(.clk(clk), .reset(reset),.d(a10), .q(q11)); 
dff dff12(.clk(clk), .reset(reset),.d(a11), .q(q12)); 

// filter output dout[n] = conv(x[n], h[n])
always @(posedge clk)
begin
  if(reset)
    dout_reg <= 0;
  else
    dout_reg <= a12;
end
assign dout = dout_reg;

// Dump waves
initial begin
  $dumpfile("dump.vcd");
  $dumpvars(1, fir);
end
endmodule