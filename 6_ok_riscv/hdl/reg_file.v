// General info about reg_file: 
// 2 read, 1 write possible in this module

module reg_file(
    input clk, 
    input reset,
    input write_enable_i, 
    input [4:0] write_address_i, 
    input [31:0] write_data_i, 
    input [4:0] read_addr1_i,
    input [4:0] read_addr2_i,
    output reg [31:0] read_out1_o,
    output reg [31:0] read_out2_o
    );

// RISV RV32E has 32 bit x 16 registers
reg [31:0] registers [0:16-1];

// handle reads of registers
always @(*)
begin
    if(~reset) 
    begin
        if(read_addr1_i)
        begin 
            read_out1_o = registers[read_addr1_i]; 
        end

        if(read_addr2_i) 
        begin
            read_out2_o = registers[read_addr2_i]; 
        end
    end
end

//handle write of registers
always @(posedge clk)
begin
    if(~reset)
    begin 
        if(write_enable_i)
        begin
            if(write_address_i)
            begin
                registers[write_address_i] <= write_data_i;
            end
        end
    end
end

endmodule
