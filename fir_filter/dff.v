module dff
        (input clk,
        input [15:0] d,
        input reset,
        output reg [15:0]   q
        );
    
    always@ (posedge clk)
    begin
        if(reset)
            q = 0;
        else
            q = d;
    end
    
endmodule