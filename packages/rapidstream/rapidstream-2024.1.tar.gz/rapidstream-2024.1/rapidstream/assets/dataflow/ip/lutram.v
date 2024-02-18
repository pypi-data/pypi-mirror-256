// Copyright 2024 RapidStream Design Automation, Inc.
// All Rights Reserved.

`timescale 1 ns / 1 ps

module RAM_S2P_LUTRAM_1R1W (
    address0,
    ce0,
    q0,

    address1,
    ce1,
    d1,
    we1,

    reset,
    clock
);

parameter DataWidth = 32;
parameter AddressWidth = 5;
parameter AddressRange = 32;

input[AddressWidth-1:0] address0;
input ce0;
output reg[DataWidth-1:0] q0;

input[AddressWidth-1:0] address1;
input ce1;
input[DataWidth-1:0] d1;
input we1;

input reset;
input clock;

(* ram_style = "distributed" *) reg [DataWidth-1:0] ram[0:AddressRange-1];

always @(posedge clock)
begin
    if (ce1) begin
        if (we1)
            ram[address1] <= d1;
    end

    if (ce0) begin
        q0 <= ram[address0];
    end
end

endmodule
