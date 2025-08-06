module pcileech_bar_impl_AX200_wifi(
    input               rst,
    input               clk,
    // incoming BAR writes:
    input [31:0]        wr_addr,
    input [3:0]         wr_be,
    input [31:0]        wr_data,
    input               wr_valid,
    // incoming BAR reads:
    input  [87:0]       rd_req_ctx,
    input  [31:0]       rd_req_addr,
    input               rd_req_valid,
    input  [31:0]       base_address_register,
    // outgoing BAR read replies:
    output reg [87:0]   rd_rsp_ctx,
    output reg [31:0]   rd_rsp_data,
    output reg          rd_rsp_valid
);

    reg [87:0]      drd_req_ctx;
    reg [31:0]      drd_req_addr;
    reg             drd_req_valid;

    reg [31:0]      dwr_addr;
    reg [31:0]      dwr_data;
    reg             dwr_valid;

    reg [31:0]      data_32;

    time number = 0;

    always @ (posedge clk) begin
        if (rst)
            number <= 0;

        number          <= number + 1;
        drd_req_ctx     <= rd_req_ctx;
        drd_req_valid   <= rd_req_valid;
        dwr_valid       <= wr_valid;
        drd_req_addr    <= rd_req_addr;
        rd_rsp_ctx      <= drd_req_ctx;
        rd_rsp_valid    <= drd_req_valid;
        dwr_addr        <= wr_addr;
        dwr_data        <= wr_data;

        if (drd_req_valid) begin
            case (({drd_req_addr[31:24], drd_req_addr[23:16], drd_req_addr[15:08], drd_req_addr[07:00]} - (base_address_register & ~32'h4)) & 32'hFFFF)
//                        32'h0380 : rd_rsp_data <= 32'hD0ABD534;
//                        32'h0384 : rd_rsp_data <= 32'h0000FEC7;
			    default : begin
                    case (({drd_req_addr[31:24], drd_req_addr[23:16], drd_req_addr[15:08], drd_req_addr[07:00]} - (base_address_register & ~32'h4)) & 32'hFFFF)
							32'h0380 : begin
							
								rd_rsp_data[31:24]   <= 8'hD0;  // mac prefix 
								rd_rsp_data[23:16]  <= 8'hAB;  // mac prefix 
								rd_rsp_data[15:08] <= 8'hD5;  // mac prefix
                            rd_rsp_data[7:0] <= ((0 + (number) % (15 + 1 - 0)) << 4) | (0 + (number + 3) % (15 + 1 - 0));
							end
									32'h0384 : begin
									rd_rsp_data[31:16] <= 16'h0000;
									rd_rsp_data[15:8]  <= ((0 + (number + 12) % (15 + 1 - 0)) << 4) | (0 + (number + 15) % (15 + 1 - 0));
									rd_rsp_data[7:0]   <= ((0 + (number + 6) % (15 + 1 - 0)) << 4) | (0 + (number + 9) % (15 + 1 - 0));
									end

			16'h0000 : rd_rsp_data <= 32'h00800000; //设备初始化的值
                                                    //中间已删减，请填写你自己RW出来的
           /* 16'h0380 : rd_rsp_data <= 32'hD0ABD534;
            16'h0384 : rd_rsp_data <= 32'h0000FEC7; */
            16'h0400 : rd_rsp_data <= 32'hA5A5A5A0;
                default : rd_rsp_data <= 32'h00000000;  // realtek G
                    endcase
                end
            endcase
        end else if (dwr_valid) begin
             case (({dwr_addr[31:24], dwr_addr[23:16], dwr_addr[15:08], dwr_addr[07:00]} - (base_address_register & ~32'h4)) & 32'h00FF) //
            endcase
        end else begin
                            rd_rsp_data[7:0]   <= ((0 + (number) % (15 + 1 - 0)) << 4) | (0 + (number + 3) % (15 + 1 - 0));
                            rd_rsp_data[15:8]  <= ((0 + (number + 6) % (15 + 1 - 0)) << 4) | (0 + (number + 9) % (15 + 1 - 0));
                            rd_rsp_data[23:16] <= ((0 + (number + 12) % (15 + 1 - 0)) << 4) | (0 + (number + 15) % (15 + 1 - 0));
                            rd_rsp_data[31:24] <= ((0 + (number) % (15 + 1 - 0)) << 4) | (0 + (number + 3) % (15 + 1 - 0));
        end
    end

endmodule
