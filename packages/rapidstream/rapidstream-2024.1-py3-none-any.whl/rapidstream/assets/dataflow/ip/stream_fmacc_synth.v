// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2022.2 (lin64) Build 3671981 Fri Oct 14 04:59:54 MDT 2022
// Date        : Wed Nov  1 13:06:29 2023
// Host        : inglewood running 64-bit Ubuntu 22.04.3 LTS
// Command     : write_verilog stream_fmacc_no_dsp_synth.v
// Design      : stream_fmacc
// Purpose     : This is a Verilog netlist of the current design or from a specific cell of the design. The output is an
//               IEEE 1364-2001 compliant Verilog HDL file that contains netlist information obtained from the input
//               design files.
// Device      : xcvc1902-vsvd1760-3HP-e-S
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

(* CORE_GENERATION_INFO = "stream_fmacc_stream_fmacc,hls_ip_2022_2,{HLS_INPUT_TYPE=cxx,HLS_INPUT_FLOAT=0,HLS_INPUT_FIXED=0,HLS_INPUT_PART=xcvc1902-vsvd1760-3HP-e-S,HLS_INPUT_CLOCK=4.000000,HLS_INPUT_ARCH=others,HLS_SYN_CLOCK=2.844000,HLS_SYN_LAT=-1,HLS_SYN_TPT=none,HLS_SYN_MEM=0,HLS_SYN_DSP=0,HLS_SYN_FF=110,HLS_SYN_LUT=99,HLS_VERSION=2022_2}" *) (* ap_ST_fsm_state1 = "4'b0001" *) (* ap_ST_fsm_state2 = "4'b0010" *)
(* ap_ST_fsm_state3 = "4'b0100" *) (* ap_ST_fsm_state4 = "4'b1000" *) (* hls_module = "yes" *)
(* STRUCTURAL_NETLIST = "yes" *)
module stream_fmacc
   (ap_clk,
    ap_rst_n,
    ap_start,
    ap_done,
    ap_idle,
    ap_ready,
    data_in_dout,
    data_in_empty_n,
    data_in_read,
    weighted_sum_din,
    weighted_sum_full_n,
    weighted_sum_write,
    run_critical_path,
    run_post_bucket_delayed_z);
  input ap_clk;
  input ap_rst_n;
  input ap_start;
  output ap_done;
  output ap_idle;
  output ap_ready;
  input [64:0]data_in_dout;
  input data_in_empty_n;
  output data_in_read;
  output [31:0]weighted_sum_din;
  input weighted_sum_full_n;
  output weighted_sum_write;
  input run_critical_path;
  input run_post_bucket_delayed_z;

  wire \<const0> ;
  wire \<const1> ;
  wire VCC_2;
  wire acc0;
  wire [31:0]add1_fu_42_p4;
  wire \ap_CS_fsm[3]_i_4_n_0 ;
  wire \ap_CS_fsm_reg_n_0_[0] ;
  wire ap_CS_fsm_state2;
  wire ap_CS_fsm_state3;
  wire ap_CS_fsm_state4;
  wire [3:0]ap_NS_fsm;
  wire ap_NS_fsm1;
  wire ap_NS_fsm13_out;
  wire ap_clk;
  wire ap_clk_IBUF;
  wire ap_clk_IBUF_BUFG;
  wire ap_done;
  wire ap_idle;
  wire ap_idle_OBUF;
  wire ap_ready;
  wire ap_ready_OBUF;
  wire ap_rst_n;
  wire ap_rst_n_IBUF;
  wire ap_rst_n_inv;
  wire ap_start;
  wire ap_start_IBUF;
  wire [64:0]data_in_dout;
  wire [64:0]data_in_dout_IBUF;
  wire data_in_empty_n;
  wire data_in_empty_n_IBUF;
  wire data_in_read;
  wire data_in_read_OBUF;
  wire grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg;
  wire grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg0;
  wire grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg_i_1_n_0;
  wire \icmp_ln25_reg_191[0]_i_1_n_0 ;
  wire [1:0]loop_idx_2_fu_101_p2;
  wire [1:0]loop_idx_2_reg_183;
  wire [1:0]loop_idx_fu_56;
  wire [1:1]p_0_in;
  wire run_critical_path;
  wire run_critical_path_IBUF;
  wire run_post_bucket_delayed_z;
  wire run_post_bucket_delayed_z_IBUF;
  wire run_post_bucket_delayed_z_not_reg_178;
  wire \run_post_bucket_delayed_z_not_reg_178[0]_i_1_n_0 ;
  wire [31:0]weighted_sum_din;
  wire [31:0]weighted_sum_din_OBUF;
  wire weighted_sum_full_n;
  wire weighted_sum_full_n_IBUF;
  wire weighted_sum_write;
  wire weighted_sum_write_OBUF;

  GND GND
       (.G(\<const0> ));
  VCC VCC
       (.P(\<const1> ));
  VCC VCC_1
       (.P(VCC_2));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[0]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[0]),
        .Q(weighted_sum_din_OBUF[0]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[10]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[10]),
        .Q(weighted_sum_din_OBUF[10]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[11]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[11]),
        .Q(weighted_sum_din_OBUF[11]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[12]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[12]),
        .Q(weighted_sum_din_OBUF[12]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[13]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[13]),
        .Q(weighted_sum_din_OBUF[13]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[14]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[14]),
        .Q(weighted_sum_din_OBUF[14]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[15]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[15]),
        .Q(weighted_sum_din_OBUF[15]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[16]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[16]),
        .Q(weighted_sum_din_OBUF[16]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[17]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[17]),
        .Q(weighted_sum_din_OBUF[17]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[18]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[18]),
        .Q(weighted_sum_din_OBUF[18]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[19]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[19]),
        .Q(weighted_sum_din_OBUF[19]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[1]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[1]),
        .Q(weighted_sum_din_OBUF[1]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[20]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[20]),
        .Q(weighted_sum_din_OBUF[20]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[21]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[21]),
        .Q(weighted_sum_din_OBUF[21]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[22]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[22]),
        .Q(weighted_sum_din_OBUF[22]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[23]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[23]),
        .Q(weighted_sum_din_OBUF[23]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[24]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[24]),
        .Q(weighted_sum_din_OBUF[24]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[25]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[25]),
        .Q(weighted_sum_din_OBUF[25]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[26]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[26]),
        .Q(weighted_sum_din_OBUF[26]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[27]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[27]),
        .Q(weighted_sum_din_OBUF[27]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[28]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[28]),
        .Q(weighted_sum_din_OBUF[28]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[29]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[29]),
        .Q(weighted_sum_din_OBUF[29]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[2]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[2]),
        .Q(weighted_sum_din_OBUF[2]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[30]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[30]),
        .Q(weighted_sum_din_OBUF[30]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[31]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[31]),
        .Q(weighted_sum_din_OBUF[31]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[3]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[3]),
        .Q(weighted_sum_din_OBUF[3]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[4]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[4]),
        .Q(weighted_sum_din_OBUF[4]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[5]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[5]),
        .Q(weighted_sum_din_OBUF[5]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[6]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[6]),
        .Q(weighted_sum_din_OBUF[6]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[7]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[7]),
        .Q(weighted_sum_din_OBUF[7]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[8]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[8]),
        .Q(weighted_sum_din_OBUF[8]),
        .R(weighted_sum_write_OBUF));
  FDRE #(
    .INIT(1'b0))
    \acc_reg[9]
       (.C(ap_clk_IBUF_BUFG),
        .CE(acc0),
        .D(add1_fu_42_p4[9]),
        .Q(weighted_sum_din_OBUF[9]),
        .R(weighted_sum_write_OBUF));
  (* SOFT_HLUTNM = "soft_lutpair2" *)
  LUT5 #(
    .INIT(32'h4F444444))
    \ap_CS_fsm[0]_i_1
       (.I0(ap_start_IBUF),
        .I1(\ap_CS_fsm_reg_n_0_[0] ),
        .I2(loop_idx_fu_56[0]),
        .I3(loop_idx_fu_56[1]),
        .I4(ap_CS_fsm_state2),
        .O(ap_NS_fsm[0]));
  (* SOFT_HLUTNM = "soft_lutpair3" *)
  LUT5 #(
    .INIT(32'hF888F8F8))
    \ap_CS_fsm[1]_i_1
       (.I0(ap_start_IBUF),
        .I1(\ap_CS_fsm_reg_n_0_[0] ),
        .I2(ap_CS_fsm_state4),
        .I3(weighted_sum_full_n_IBUF),
        .I4(p_0_in),
        .O(ap_NS_fsm[1]));
  (* SOFT_HLUTNM = "soft_lutpair4" *)
  LUT5 #(
    .INIT(32'hA0B08090))
    \ap_CS_fsm[3]_i_4
       (.I0(loop_idx_fu_56[0]),
        .I1(loop_idx_fu_56[1]),
        .I2(ap_CS_fsm_state2),
        .I3(run_critical_path_IBUF),
        .I4(run_post_bucket_delayed_z_not_reg_178),
        .O(\ap_CS_fsm[3]_i_4_n_0 ));
  (* FSM_ENCODING = "none" *)
  FDSE #(
    .INIT(1'b1))
    \ap_CS_fsm_reg[0]
       (.C(ap_clk_IBUF_BUFG),
        .CE(\<const1> ),
        .D(ap_NS_fsm[0]),
        .Q(\ap_CS_fsm_reg_n_0_[0] ),
        .S(ap_rst_n_inv));
  (* FSM_ENCODING = "none" *)
  FDRE #(
    .INIT(1'b0))
    \ap_CS_fsm_reg[1]
       (.C(ap_clk_IBUF_BUFG),
        .CE(\<const1> ),
        .D(ap_NS_fsm[1]),
        .Q(ap_CS_fsm_state2),
        .R(ap_rst_n_inv));
  (* FSM_ENCODING = "none" *)
  FDRE #(
    .INIT(1'b0))
    \ap_CS_fsm_reg[2]
       (.C(ap_clk_IBUF_BUFG),
        .CE(\<const1> ),
        .D(ap_NS_fsm[2]),
        .Q(ap_CS_fsm_state3),
        .R(ap_rst_n_inv));
  (* FSM_ENCODING = "none" *)
  FDRE #(
    .INIT(1'b0))
    \ap_CS_fsm_reg[3]
       (.C(ap_clk_IBUF_BUFG),
        .CE(\<const1> ),
        .D(ap_NS_fsm[3]),
        .Q(ap_CS_fsm_state4),
        .R(ap_rst_n_inv));
  (* XILINX_LEGACY_PRIM = "BUFG" *)
  (* XILINX_TRANSFORM_PINMAP = "VCC:CE" *)
  BUFGCE #(
    .CE_TYPE("ASYNC"),
    .SIM_DEVICE("VERSAL_AI_CORE"),
    .STARTUP_SYNC("FALSE"))
    ap_clk_IBUF_BUFG_inst
       (.CE(VCC_2),
        .I(ap_clk_IBUF),
        .O(ap_clk_IBUF_BUFG));
  IBUF #(
    .CCIO_EN("TRUE"))
    ap_clk_IBUF_inst
       (.I(ap_clk),
        .O(ap_clk_IBUF));
  OBUF ap_done_OBUF_inst
       (.I(ap_ready_OBUF),
        .O(ap_done));
  (* SOFT_HLUTNM = "soft_lutpair2" *)
  LUT3 #(
    .INIT(8'h40))
    ap_done_OBUF_inst_i_1
       (.I0(loop_idx_fu_56[0]),
        .I1(loop_idx_fu_56[1]),
        .I2(ap_CS_fsm_state2),
        .O(ap_ready_OBUF));
  OBUF ap_idle_OBUF_inst
       (.I(ap_idle_OBUF),
        .O(ap_idle));
  (* SOFT_HLUTNM = "soft_lutpair3" *)
  LUT2 #(
    .INIT(4'h2))
    ap_idle_OBUF_inst_i_1
       (.I0(\ap_CS_fsm_reg_n_0_[0] ),
        .I1(ap_start_IBUF),
        .O(ap_idle_OBUF));
  OBUF ap_ready_OBUF_inst
       (.I(ap_ready_OBUF),
        .O(ap_ready));
  IBUF #(
    .CCIO_EN("TRUE"))
    ap_rst_n_IBUF_inst
       (.I(ap_rst_n),
        .O(ap_rst_n_IBUF));
  IBUF #(
    .CCIO_EN("TRUE"))
    ap_start_IBUF_inst
       (.I(ap_start),
        .O(ap_start_IBUF));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[0]_inst
       (.I(data_in_dout[0]),
        .O(data_in_dout_IBUF[0]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[10]_inst
       (.I(data_in_dout[10]),
        .O(data_in_dout_IBUF[10]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[11]_inst
       (.I(data_in_dout[11]),
        .O(data_in_dout_IBUF[11]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[12]_inst
       (.I(data_in_dout[12]),
        .O(data_in_dout_IBUF[12]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[13]_inst
       (.I(data_in_dout[13]),
        .O(data_in_dout_IBUF[13]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[14]_inst
       (.I(data_in_dout[14]),
        .O(data_in_dout_IBUF[14]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[15]_inst
       (.I(data_in_dout[15]),
        .O(data_in_dout_IBUF[15]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[16]_inst
       (.I(data_in_dout[16]),
        .O(data_in_dout_IBUF[16]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[17]_inst
       (.I(data_in_dout[17]),
        .O(data_in_dout_IBUF[17]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[18]_inst
       (.I(data_in_dout[18]),
        .O(data_in_dout_IBUF[18]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[19]_inst
       (.I(data_in_dout[19]),
        .O(data_in_dout_IBUF[19]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[1]_inst
       (.I(data_in_dout[1]),
        .O(data_in_dout_IBUF[1]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[20]_inst
       (.I(data_in_dout[20]),
        .O(data_in_dout_IBUF[20]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[21]_inst
       (.I(data_in_dout[21]),
        .O(data_in_dout_IBUF[21]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[22]_inst
       (.I(data_in_dout[22]),
        .O(data_in_dout_IBUF[22]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[23]_inst
       (.I(data_in_dout[23]),
        .O(data_in_dout_IBUF[23]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[24]_inst
       (.I(data_in_dout[24]),
        .O(data_in_dout_IBUF[24]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[25]_inst
       (.I(data_in_dout[25]),
        .O(data_in_dout_IBUF[25]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[26]_inst
       (.I(data_in_dout[26]),
        .O(data_in_dout_IBUF[26]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[27]_inst
       (.I(data_in_dout[27]),
        .O(data_in_dout_IBUF[27]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[28]_inst
       (.I(data_in_dout[28]),
        .O(data_in_dout_IBUF[28]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[29]_inst
       (.I(data_in_dout[29]),
        .O(data_in_dout_IBUF[29]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[2]_inst
       (.I(data_in_dout[2]),
        .O(data_in_dout_IBUF[2]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[30]_inst
       (.I(data_in_dout[30]),
        .O(data_in_dout_IBUF[30]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[31]_inst
       (.I(data_in_dout[31]),
        .O(data_in_dout_IBUF[31]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[32]_inst
       (.I(data_in_dout[32]),
        .O(data_in_dout_IBUF[32]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[33]_inst
       (.I(data_in_dout[33]),
        .O(data_in_dout_IBUF[33]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[34]_inst
       (.I(data_in_dout[34]),
        .O(data_in_dout_IBUF[34]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[35]_inst
       (.I(data_in_dout[35]),
        .O(data_in_dout_IBUF[35]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[36]_inst
       (.I(data_in_dout[36]),
        .O(data_in_dout_IBUF[36]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[37]_inst
       (.I(data_in_dout[37]),
        .O(data_in_dout_IBUF[37]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[38]_inst
       (.I(data_in_dout[38]),
        .O(data_in_dout_IBUF[38]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[39]_inst
       (.I(data_in_dout[39]),
        .O(data_in_dout_IBUF[39]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[3]_inst
       (.I(data_in_dout[3]),
        .O(data_in_dout_IBUF[3]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[40]_inst
       (.I(data_in_dout[40]),
        .O(data_in_dout_IBUF[40]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[41]_inst
       (.I(data_in_dout[41]),
        .O(data_in_dout_IBUF[41]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[42]_inst
       (.I(data_in_dout[42]),
        .O(data_in_dout_IBUF[42]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[43]_inst
       (.I(data_in_dout[43]),
        .O(data_in_dout_IBUF[43]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[44]_inst
       (.I(data_in_dout[44]),
        .O(data_in_dout_IBUF[44]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[45]_inst
       (.I(data_in_dout[45]),
        .O(data_in_dout_IBUF[45]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[46]_inst
       (.I(data_in_dout[46]),
        .O(data_in_dout_IBUF[46]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[47]_inst
       (.I(data_in_dout[47]),
        .O(data_in_dout_IBUF[47]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[48]_inst
       (.I(data_in_dout[48]),
        .O(data_in_dout_IBUF[48]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[49]_inst
       (.I(data_in_dout[49]),
        .O(data_in_dout_IBUF[49]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[4]_inst
       (.I(data_in_dout[4]),
        .O(data_in_dout_IBUF[4]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[50]_inst
       (.I(data_in_dout[50]),
        .O(data_in_dout_IBUF[50]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[51]_inst
       (.I(data_in_dout[51]),
        .O(data_in_dout_IBUF[51]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[52]_inst
       (.I(data_in_dout[52]),
        .O(data_in_dout_IBUF[52]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[53]_inst
       (.I(data_in_dout[53]),
        .O(data_in_dout_IBUF[53]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[54]_inst
       (.I(data_in_dout[54]),
        .O(data_in_dout_IBUF[54]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[55]_inst
       (.I(data_in_dout[55]),
        .O(data_in_dout_IBUF[55]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[56]_inst
       (.I(data_in_dout[56]),
        .O(data_in_dout_IBUF[56]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[57]_inst
       (.I(data_in_dout[57]),
        .O(data_in_dout_IBUF[57]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[58]_inst
       (.I(data_in_dout[58]),
        .O(data_in_dout_IBUF[58]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[59]_inst
       (.I(data_in_dout[59]),
        .O(data_in_dout_IBUF[59]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[5]_inst
       (.I(data_in_dout[5]),
        .O(data_in_dout_IBUF[5]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[60]_inst
       (.I(data_in_dout[60]),
        .O(data_in_dout_IBUF[60]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[61]_inst
       (.I(data_in_dout[61]),
        .O(data_in_dout_IBUF[61]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[62]_inst
       (.I(data_in_dout[62]),
        .O(data_in_dout_IBUF[62]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[63]_inst
       (.I(data_in_dout[63]),
        .O(data_in_dout_IBUF[63]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[64]_inst
       (.I(data_in_dout[64]),
        .O(data_in_dout_IBUF[64]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[6]_inst
       (.I(data_in_dout[6]),
        .O(data_in_dout_IBUF[6]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[7]_inst
       (.I(data_in_dout[7]),
        .O(data_in_dout_IBUF[7]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[8]_inst
       (.I(data_in_dout[8]),
        .O(data_in_dout_IBUF[8]));
  IBUF #(
    .CCIO_EN("TRUE"))
    \data_in_dout_IBUF[9]_inst
       (.I(data_in_dout[9]),
        .O(data_in_dout_IBUF[9]));
  IBUF #(
    .CCIO_EN("TRUE"))
    data_in_empty_n_IBUF_inst
       (.I(data_in_empty_n),
        .O(data_in_empty_n_IBUF));
  OBUF data_in_read_OBUF_inst
       (.I(data_in_read_OBUF),
        .O(data_in_read));
  (* SOFT_HLUTNM = "soft_lutpair5" *)
  LUT3 #(
    .INIT(8'h80))
    data_in_read_OBUF_inst_i_1
       (.I0(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg),
        .I1(data_in_empty_n_IBUF),
        .I2(ap_CS_fsm_state3),
        .O(data_in_read_OBUF));
  stream_fmacc_stream_fmacc_Pipeline_VITIS_LOOP_26_2 grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79
       (.CLK(ap_clk_IBUF_BUFG),
        .D(add1_fu_42_p4),
        .E(acc0),
        .Q(weighted_sum_din_OBUF),
        .SR(ap_rst_n_inv),
        .\ap_CS_fsm_reg[2] (ap_NS_fsm[3:2]),
        .\ap_CS_fsm_reg[2]_0 (loop_idx_fu_56),
        .\ap_CS_fsm_reg[3] ({ap_CS_fsm_state4,ap_CS_fsm_state3,ap_CS_fsm_state2}),
        .\ap_CS_fsm_reg[3]_0 (\ap_CS_fsm[3]_i_4_n_0 ),
        .ap_rst_n_IBUF(ap_rst_n_IBUF),
        .data_in_dout_IBUF(data_in_dout_IBUF),
        .data_in_empty_n_IBUF(data_in_empty_n_IBUF),
        .grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg),
        .p_0_in(p_0_in),
        .run_critical_path_IBUF(run_critical_path_IBUF),
        .run_post_bucket_delayed_z_not_reg_178(run_post_bucket_delayed_z_not_reg_178),
        .weighted_sum_full_n_IBUF(weighted_sum_full_n_IBUF));
  (* SOFT_HLUTNM = "soft_lutpair5" *)
  LUT4 #(
    .INIT(16'hFF70))
    grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg_i_1
       (.I0(data_in_dout_IBUF[64]),
        .I1(data_in_empty_n_IBUF),
        .I2(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg),
        .I3(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg0),
        .O(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg_i_1_n_0));
  (* SOFT_HLUTNM = "soft_lutpair4" *)
  LUT5 #(
    .INIT(32'h000800A8))
    grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg_i_2
       (.I0(ap_CS_fsm_state2),
        .I1(run_critical_path_IBUF),
        .I2(loop_idx_fu_56[0]),
        .I3(loop_idx_fu_56[1]),
        .I4(run_post_bucket_delayed_z_not_reg_178),
        .O(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg0));
  FDRE #(
    .INIT(1'b0))
    grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg_reg
       (.C(ap_clk_IBUF_BUFG),
        .CE(\<const1> ),
        .D(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg_i_1_n_0),
        .Q(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg),
        .R(ap_rst_n_inv));
  LUT4 #(
    .INIT(16'h7702))
    \icmp_ln25_reg_191[0]_i_1
       (.I0(ap_CS_fsm_state2),
        .I1(loop_idx_fu_56[0]),
        .I2(loop_idx_fu_56[1]),
        .I3(p_0_in),
        .O(\icmp_ln25_reg_191[0]_i_1_n_0 ));
  FDRE #(
    .INIT(1'b0))
    \icmp_ln25_reg_191_reg[0]
       (.C(ap_clk_IBUF_BUFG),
        .CE(\<const1> ),
        .D(\icmp_ln25_reg_191[0]_i_1_n_0 ),
        .Q(p_0_in),
        .R(\<const0> ));
  (* SOFT_HLUTNM = "soft_lutpair6" *)
  LUT1 #(
    .INIT(2'h1))
    \loop_idx_2_reg_183[0]_i_1
       (.I0(loop_idx_fu_56[0]),
        .O(loop_idx_2_fu_101_p2[0]));
  (* SOFT_HLUTNM = "soft_lutpair6" *)
  LUT2 #(
    .INIT(4'h6))
    \loop_idx_2_reg_183[1]_i_1
       (.I0(loop_idx_fu_56[0]),
        .I1(loop_idx_fu_56[1]),
        .O(loop_idx_2_fu_101_p2[1]));
  FDRE #(
    .INIT(1'b0))
    \loop_idx_2_reg_183_reg[0]
       (.C(ap_clk_IBUF_BUFG),
        .CE(ap_CS_fsm_state2),
        .D(loop_idx_2_fu_101_p2[0]),
        .Q(loop_idx_2_reg_183[0]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \loop_idx_2_reg_183_reg[1]
       (.C(ap_clk_IBUF_BUFG),
        .CE(ap_CS_fsm_state2),
        .D(loop_idx_2_fu_101_p2[1]),
        .Q(loop_idx_2_reg_183[1]),
        .R(\<const0> ));
  LUT2 #(
    .INIT(4'h8))
    \loop_idx_fu_56[1]_i_1
       (.I0(ap_start_IBUF),
        .I1(\ap_CS_fsm_reg_n_0_[0] ),
        .O(ap_NS_fsm13_out));
  LUT3 #(
    .INIT(8'h8A))
    \loop_idx_fu_56[1]_i_2
       (.I0(ap_CS_fsm_state4),
        .I1(weighted_sum_full_n_IBUF),
        .I2(p_0_in),
        .O(ap_NS_fsm1));
  FDRE #(
    .INIT(1'b0))
    \loop_idx_fu_56_reg[0]
       (.C(ap_clk_IBUF_BUFG),
        .CE(ap_NS_fsm1),
        .D(loop_idx_2_reg_183[0]),
        .Q(loop_idx_fu_56[0]),
        .R(ap_NS_fsm13_out));
  FDRE #(
    .INIT(1'b0))
    \loop_idx_fu_56_reg[1]
       (.C(ap_clk_IBUF_BUFG),
        .CE(ap_NS_fsm1),
        .D(loop_idx_2_reg_183[1]),
        .Q(loop_idx_fu_56[1]),
        .R(ap_NS_fsm13_out));
  IBUF #(
    .CCIO_EN("TRUE"))
    run_critical_path_IBUF_inst
       (.I(run_critical_path),
        .O(run_critical_path_IBUF));
  IBUF #(
    .CCIO_EN("TRUE"))
    run_post_bucket_delayed_z_IBUF_inst
       (.I(run_post_bucket_delayed_z),
        .O(run_post_bucket_delayed_z_IBUF));
  LUT3 #(
    .INIT(8'h74))
    \run_post_bucket_delayed_z_not_reg_178[0]_i_1
       (.I0(run_post_bucket_delayed_z_IBUF),
        .I1(\ap_CS_fsm_reg_n_0_[0] ),
        .I2(run_post_bucket_delayed_z_not_reg_178),
        .O(\run_post_bucket_delayed_z_not_reg_178[0]_i_1_n_0 ));
  FDRE #(
    .INIT(1'b0))
    \run_post_bucket_delayed_z_not_reg_178_reg[0]
       (.C(ap_clk_IBUF_BUFG),
        .CE(\<const1> ),
        .D(\run_post_bucket_delayed_z_not_reg_178[0]_i_1_n_0 ),
        .Q(run_post_bucket_delayed_z_not_reg_178),
        .R(\<const0> ));
  OBUF \weighted_sum_din_OBUF[0]_inst
       (.I(weighted_sum_din_OBUF[0]),
        .O(weighted_sum_din[0]));
  OBUF \weighted_sum_din_OBUF[10]_inst
       (.I(weighted_sum_din_OBUF[10]),
        .O(weighted_sum_din[10]));
  OBUF \weighted_sum_din_OBUF[11]_inst
       (.I(weighted_sum_din_OBUF[11]),
        .O(weighted_sum_din[11]));
  OBUF \weighted_sum_din_OBUF[12]_inst
       (.I(weighted_sum_din_OBUF[12]),
        .O(weighted_sum_din[12]));
  OBUF \weighted_sum_din_OBUF[13]_inst
       (.I(weighted_sum_din_OBUF[13]),
        .O(weighted_sum_din[13]));
  OBUF \weighted_sum_din_OBUF[14]_inst
       (.I(weighted_sum_din_OBUF[14]),
        .O(weighted_sum_din[14]));
  OBUF \weighted_sum_din_OBUF[15]_inst
       (.I(weighted_sum_din_OBUF[15]),
        .O(weighted_sum_din[15]));
  OBUF \weighted_sum_din_OBUF[16]_inst
       (.I(weighted_sum_din_OBUF[16]),
        .O(weighted_sum_din[16]));
  OBUF \weighted_sum_din_OBUF[17]_inst
       (.I(weighted_sum_din_OBUF[17]),
        .O(weighted_sum_din[17]));
  OBUF \weighted_sum_din_OBUF[18]_inst
       (.I(weighted_sum_din_OBUF[18]),
        .O(weighted_sum_din[18]));
  OBUF \weighted_sum_din_OBUF[19]_inst
       (.I(weighted_sum_din_OBUF[19]),
        .O(weighted_sum_din[19]));
  OBUF \weighted_sum_din_OBUF[1]_inst
       (.I(weighted_sum_din_OBUF[1]),
        .O(weighted_sum_din[1]));
  OBUF \weighted_sum_din_OBUF[20]_inst
       (.I(weighted_sum_din_OBUF[20]),
        .O(weighted_sum_din[20]));
  OBUF \weighted_sum_din_OBUF[21]_inst
       (.I(weighted_sum_din_OBUF[21]),
        .O(weighted_sum_din[21]));
  OBUF \weighted_sum_din_OBUF[22]_inst
       (.I(weighted_sum_din_OBUF[22]),
        .O(weighted_sum_din[22]));
  OBUF \weighted_sum_din_OBUF[23]_inst
       (.I(weighted_sum_din_OBUF[23]),
        .O(weighted_sum_din[23]));
  OBUF \weighted_sum_din_OBUF[24]_inst
       (.I(weighted_sum_din_OBUF[24]),
        .O(weighted_sum_din[24]));
  OBUF \weighted_sum_din_OBUF[25]_inst
       (.I(weighted_sum_din_OBUF[25]),
        .O(weighted_sum_din[25]));
  OBUF \weighted_sum_din_OBUF[26]_inst
       (.I(weighted_sum_din_OBUF[26]),
        .O(weighted_sum_din[26]));
  OBUF \weighted_sum_din_OBUF[27]_inst
       (.I(weighted_sum_din_OBUF[27]),
        .O(weighted_sum_din[27]));
  OBUF \weighted_sum_din_OBUF[28]_inst
       (.I(weighted_sum_din_OBUF[28]),
        .O(weighted_sum_din[28]));
  OBUF \weighted_sum_din_OBUF[29]_inst
       (.I(weighted_sum_din_OBUF[29]),
        .O(weighted_sum_din[29]));
  OBUF \weighted_sum_din_OBUF[2]_inst
       (.I(weighted_sum_din_OBUF[2]),
        .O(weighted_sum_din[2]));
  OBUF \weighted_sum_din_OBUF[30]_inst
       (.I(weighted_sum_din_OBUF[30]),
        .O(weighted_sum_din[30]));
  OBUF \weighted_sum_din_OBUF[31]_inst
       (.I(weighted_sum_din_OBUF[31]),
        .O(weighted_sum_din[31]));
  OBUF \weighted_sum_din_OBUF[3]_inst
       (.I(weighted_sum_din_OBUF[3]),
        .O(weighted_sum_din[3]));
  OBUF \weighted_sum_din_OBUF[4]_inst
       (.I(weighted_sum_din_OBUF[4]),
        .O(weighted_sum_din[4]));
  OBUF \weighted_sum_din_OBUF[5]_inst
       (.I(weighted_sum_din_OBUF[5]),
        .O(weighted_sum_din[5]));
  OBUF \weighted_sum_din_OBUF[6]_inst
       (.I(weighted_sum_din_OBUF[6]),
        .O(weighted_sum_din[6]));
  OBUF \weighted_sum_din_OBUF[7]_inst
       (.I(weighted_sum_din_OBUF[7]),
        .O(weighted_sum_din[7]));
  OBUF \weighted_sum_din_OBUF[8]_inst
       (.I(weighted_sum_din_OBUF[8]),
        .O(weighted_sum_din[8]));
  OBUF \weighted_sum_din_OBUF[9]_inst
       (.I(weighted_sum_din_OBUF[9]),
        .O(weighted_sum_din[9]));
  IBUF #(
    .CCIO_EN("TRUE"))
    weighted_sum_full_n_IBUF_inst
       (.I(weighted_sum_full_n),
        .O(weighted_sum_full_n_IBUF));
  OBUF weighted_sum_write_OBUF_inst
       (.I(weighted_sum_write_OBUF),
        .O(weighted_sum_write));
  LUT3 #(
    .INIT(8'h80))
    weighted_sum_write_OBUF_inst_i_1
       (.I0(weighted_sum_full_n_IBUF),
        .I1(ap_CS_fsm_state4),
        .I2(p_0_in),
        .O(weighted_sum_write_OBUF));
endmodule

module stream_fmacc_flow_control_loop_pipe_sequential_init
   (SR,
    \ap_CS_fsm_reg[2] ,
    CLK,
    run_post_bucket_delayed_z_not_reg_178,
    \ap_CS_fsm_reg[2]_0 ,
    run_critical_path_IBUF,
    \ap_CS_fsm_reg[3] ,
    \ap_CS_fsm_reg[3]_0 ,
    weighted_sum_full_n_IBUF,
    p_0_in,
    grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg,
    data_in_dout_IBUF,
    data_in_empty_n_IBUF,
    ap_rst_n_IBUF);
  output [0:0]SR;
  output [1:0]\ap_CS_fsm_reg[2] ;
  input CLK;
  input run_post_bucket_delayed_z_not_reg_178;
  input [1:0]\ap_CS_fsm_reg[2]_0 ;
  input run_critical_path_IBUF;
  input [2:0]\ap_CS_fsm_reg[3] ;
  input \ap_CS_fsm_reg[3]_0 ;
  input weighted_sum_full_n_IBUF;
  input [0:0]p_0_in;
  input grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg;
  input [0:0]data_in_dout_IBUF;
  input data_in_empty_n_IBUF;
  input ap_rst_n_IBUF;

  wire \<const1> ;
  wire CLK;
  wire [0:0]SR;
  wire \ap_CS_fsm[2]_i_2_n_0 ;
  wire [1:0]\ap_CS_fsm_reg[2] ;
  wire [1:0]\ap_CS_fsm_reg[2]_0 ;
  wire [2:0]\ap_CS_fsm_reg[3] ;
  wire \ap_CS_fsm_reg[3]_0 ;
  wire ap_NS_fsm10_out;
  wire ap_done_cache;
  wire ap_done_cache_i_1_n_0;
  wire ap_rst_n_IBUF;
  wire [0:0]data_in_dout_IBUF;
  wire data_in_empty_n_IBUF;
  wire grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg;
  wire [0:0]p_0_in;
  wire run_critical_path_IBUF;
  wire run_post_bucket_delayed_z_not_reg_178;
  wire weighted_sum_full_n_IBUF;

  VCC VCC
       (.P(\<const1> ));
  LUT6 #(
    .INIT(64'hFFFFFFFF13100000))
    \ap_CS_fsm[2]_i_1
       (.I0(run_post_bucket_delayed_z_not_reg_178),
        .I1(\ap_CS_fsm_reg[2]_0 [1]),
        .I2(\ap_CS_fsm_reg[2]_0 [0]),
        .I3(run_critical_path_IBUF),
        .I4(\ap_CS_fsm_reg[3] [0]),
        .I5(\ap_CS_fsm[2]_i_2_n_0 ),
        .O(\ap_CS_fsm_reg[2] [0]));
  (* SOFT_HLUTNM = "soft_lutpair0" *)
  LUT5 #(
    .INIT(32'h2A002AAA))
    \ap_CS_fsm[2]_i_2
       (.I0(\ap_CS_fsm_reg[3] [1]),
        .I1(data_in_empty_n_IBUF),
        .I2(data_in_dout_IBUF),
        .I3(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg),
        .I4(ap_done_cache),
        .O(\ap_CS_fsm[2]_i_2_n_0 ));
  LUT1 #(
    .INIT(2'h1))
    \ap_CS_fsm[3]_i_1
       (.I0(ap_rst_n_IBUF),
        .O(SR));
  LUT6 #(
    .INIT(64'hF8F8FFF8F8F8F8F8))
    \ap_CS_fsm[3]_i_2
       (.I0(\ap_CS_fsm_reg[3] [1]),
        .I1(ap_NS_fsm10_out),
        .I2(\ap_CS_fsm_reg[3]_0 ),
        .I3(\ap_CS_fsm_reg[3] [2]),
        .I4(weighted_sum_full_n_IBUF),
        .I5(p_0_in),
        .O(\ap_CS_fsm_reg[2] [1]));
  (* SOFT_HLUTNM = "soft_lutpair0" *)
  LUT5 #(
    .INIT(32'hE2220000))
    \ap_CS_fsm[3]_i_3
       (.I0(ap_done_cache),
        .I1(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg),
        .I2(data_in_dout_IBUF),
        .I3(data_in_empty_n_IBUF),
        .I4(\ap_CS_fsm_reg[3] [1]),
        .O(ap_NS_fsm10_out));
  LUT4 #(
    .INIT(16'h8F80))
    ap_done_cache_i_1
       (.I0(data_in_empty_n_IBUF),
        .I1(data_in_dout_IBUF),
        .I2(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg),
        .I3(ap_done_cache),
        .O(ap_done_cache_i_1_n_0));
  FDRE #(
    .INIT(1'b0))
    ap_done_cache_reg
       (.C(CLK),
        .CE(\<const1> ),
        .D(ap_done_cache_i_1_n_0),
        .Q(ap_done_cache),
        .R(SR));
endmodule

module stream_fmacc_fmadd_32ns_32ns_32ns_32ns_32_1_primitive_dsp_1
   (D,
    Q,
    \acc_reg[31] ,
    \acc_reg[31]_0 );
  output [31:0]D;
  input [31:0]Q;
  input [31:0]\acc_reg[31] ;
  input [31:0]\acc_reg[31]_0 ;

  wire \<const1> ;
  wire [31:0]D;
  wire [31:0]Q;
  wire [31:0]\acc_reg[31] ;
  wire [31:0]\acc_reg[31]_0 ;

  VCC VCC
       (.P(\<const1> ));
  stream_fmacc_fmadd_32ns_32ns_32ns_32ns_32_1_primitive_dsp_1_ip stream_fmacc_fmadd_32ns_32ns_32ns_32ns_32_1_primitive_dsp_1_ip_u
       (.m_axis_result_tdata(D),
        .s_axis_a_tdata(Q),
        .s_axis_a_tvalid(\<const1> ),
        .s_axis_b_tdata(\acc_reg[31] ),
        .s_axis_b_tvalid(\<const1> ),
        .s_axis_c_tdata(\acc_reg[31]_0 ),
        .s_axis_c_tvalid(\<const1> ));
endmodule

module stream_fmacc_fmadd_32ns_32ns_32ns_32ns_32_1_primitive_dsp_1_ip
   (s_axis_a_tvalid,
    s_axis_a_tdata,
    s_axis_b_tvalid,
    s_axis_b_tdata,
    s_axis_c_tvalid,
    s_axis_c_tdata,
    m_axis_result_tvalid,
    m_axis_result_tdata);
  input s_axis_a_tvalid;
  input [31:0]s_axis_a_tdata;
  input s_axis_b_tvalid;
  input [31:0]s_axis_b_tdata;
  input s_axis_c_tvalid;
  input [31:0]s_axis_c_tdata;
  output m_axis_result_tvalid;
  output [31:0]m_axis_result_tdata;


endmodule

module stream_fmacc_stream_fmacc_Pipeline_VITIS_LOOP_26_2
   (D,
    SR,
    E,
    \ap_CS_fsm_reg[2] ,
    Q,
    CLK,
    ap_rst_n_IBUF,
    grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg,
    data_in_empty_n_IBUF,
    data_in_dout_IBUF,
    \ap_CS_fsm_reg[3] ,
    run_post_bucket_delayed_z_not_reg_178,
    \ap_CS_fsm_reg[2]_0 ,
    run_critical_path_IBUF,
    \ap_CS_fsm_reg[3]_0 ,
    weighted_sum_full_n_IBUF,
    p_0_in);
  output [31:0]D;
  output [0:0]SR;
  output [0:0]E;
  output [1:0]\ap_CS_fsm_reg[2] ;
  input [31:0]Q;
  input CLK;
  input ap_rst_n_IBUF;
  input grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg;
  input data_in_empty_n_IBUF;
  input [64:0]data_in_dout_IBUF;
  input [2:0]\ap_CS_fsm_reg[3] ;
  input run_post_bucket_delayed_z_not_reg_178;
  input [1:0]\ap_CS_fsm_reg[2]_0 ;
  input run_critical_path_IBUF;
  input \ap_CS_fsm_reg[3]_0 ;
  input weighted_sum_full_n_IBUF;
  input [0:0]p_0_in;

  wire \<const0> ;
  wire \<const1> ;
  wire CLK;
  wire [31:0]D;
  wire [0:0]E;
  wire [31:0]Q;
  wire [0:0]SR;
  wire [1:0]\ap_CS_fsm_reg[2] ;
  wire [1:0]\ap_CS_fsm_reg[2]_0 ;
  wire [2:0]\ap_CS_fsm_reg[3] ;
  wire \ap_CS_fsm_reg[3]_0 ;
  wire ap_enable_reg_pp0_iter1;
  wire ap_enable_reg_pp0_iter1_i_1_n_0;
  wire ap_rst_n_IBUF;
  wire [64:0]data_in_dout_IBUF;
  wire data_in_empty_n_IBUF;
  wire grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg;
  wire [0:0]p_0_in;
  wire run_critical_path_IBUF;
  wire run_post_bucket_delayed_z_not_reg_178;
  wire [31:0]trunc_ln28_1_reg_98;
  wire [31:0]trunc_ln28_reg_93;
  wire \trunc_ln28_reg_93[31]_i_1_n_0 ;
  wire weighted_sum_full_n_IBUF;

  GND GND
       (.G(\<const0> ));
  VCC VCC
       (.P(\<const1> ));
  (* SOFT_HLUTNM = "soft_lutpair1" *)
  LUT4 #(
    .INIT(16'hD000))
    \acc[31]_i_1
       (.I0(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg),
        .I1(data_in_empty_n_IBUF),
        .I2(ap_enable_reg_pp0_iter1),
        .I3(\ap_CS_fsm_reg[3] [1]),
        .O(E));
  (* SOFT_HLUTNM = "soft_lutpair1" *)
  LUT5 #(
    .INIT(32'h0080C080))
    ap_enable_reg_pp0_iter1_i_1
       (.I0(ap_enable_reg_pp0_iter1),
        .I1(ap_rst_n_IBUF),
        .I2(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg),
        .I3(data_in_empty_n_IBUF),
        .I4(data_in_dout_IBUF[64]),
        .O(ap_enable_reg_pp0_iter1_i_1_n_0));
  FDRE #(
    .INIT(1'b0))
    ap_enable_reg_pp0_iter1_reg
       (.C(CLK),
        .CE(\<const1> ),
        .D(ap_enable_reg_pp0_iter1_i_1_n_0),
        .Q(ap_enable_reg_pp0_iter1),
        .R(\<const0> ));
  stream_fmacc_flow_control_loop_pipe_sequential_init flow_control_loop_pipe_sequential_init_U
       (.CLK(CLK),
        .SR(SR),
        .\ap_CS_fsm_reg[2] (\ap_CS_fsm_reg[2] ),
        .\ap_CS_fsm_reg[2]_0 (\ap_CS_fsm_reg[2]_0 ),
        .\ap_CS_fsm_reg[3] (\ap_CS_fsm_reg[3] ),
        .\ap_CS_fsm_reg[3]_0 (\ap_CS_fsm_reg[3]_0 ),
        .ap_rst_n_IBUF(ap_rst_n_IBUF),
        .data_in_dout_IBUF(data_in_dout_IBUF[64]),
        .data_in_empty_n_IBUF(data_in_empty_n_IBUF),
        .grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg),
        .p_0_in(p_0_in),
        .run_critical_path_IBUF(run_critical_path_IBUF),
        .run_post_bucket_delayed_z_not_reg_178(run_post_bucket_delayed_z_not_reg_178),
        .weighted_sum_full_n_IBUF(weighted_sum_full_n_IBUF));
  stream_fmacc_fmadd_32ns_32ns_32ns_32ns_32_1_primitive_dsp_1 fmadd_32ns_32ns_32ns_32ns_32_1_primitive_dsp_1_U1
       (.D(D),
        .Q(trunc_ln28_reg_93),
        .\acc_reg[31] (trunc_ln28_1_reg_98),
        .\acc_reg[31]_0 (Q));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[0]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[32]),
        .Q(trunc_ln28_1_reg_98[0]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[10]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[42]),
        .Q(trunc_ln28_1_reg_98[10]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[11]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[43]),
        .Q(trunc_ln28_1_reg_98[11]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[12]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[44]),
        .Q(trunc_ln28_1_reg_98[12]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[13]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[45]),
        .Q(trunc_ln28_1_reg_98[13]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[14]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[46]),
        .Q(trunc_ln28_1_reg_98[14]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[15]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[47]),
        .Q(trunc_ln28_1_reg_98[15]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[16]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[48]),
        .Q(trunc_ln28_1_reg_98[16]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[17]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[49]),
        .Q(trunc_ln28_1_reg_98[17]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[18]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[50]),
        .Q(trunc_ln28_1_reg_98[18]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[19]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[51]),
        .Q(trunc_ln28_1_reg_98[19]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[1]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[33]),
        .Q(trunc_ln28_1_reg_98[1]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[20]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[52]),
        .Q(trunc_ln28_1_reg_98[20]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[21]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[53]),
        .Q(trunc_ln28_1_reg_98[21]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[22]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[54]),
        .Q(trunc_ln28_1_reg_98[22]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[23]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[55]),
        .Q(trunc_ln28_1_reg_98[23]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[24]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[56]),
        .Q(trunc_ln28_1_reg_98[24]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[25]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[57]),
        .Q(trunc_ln28_1_reg_98[25]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[26]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[58]),
        .Q(trunc_ln28_1_reg_98[26]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[27]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[59]),
        .Q(trunc_ln28_1_reg_98[27]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[28]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[60]),
        .Q(trunc_ln28_1_reg_98[28]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[29]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[61]),
        .Q(trunc_ln28_1_reg_98[29]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[2]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[34]),
        .Q(trunc_ln28_1_reg_98[2]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[30]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[62]),
        .Q(trunc_ln28_1_reg_98[30]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[31]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[63]),
        .Q(trunc_ln28_1_reg_98[31]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[3]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[35]),
        .Q(trunc_ln28_1_reg_98[3]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[4]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[36]),
        .Q(trunc_ln28_1_reg_98[4]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[5]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[37]),
        .Q(trunc_ln28_1_reg_98[5]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[6]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[38]),
        .Q(trunc_ln28_1_reg_98[6]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[7]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[39]),
        .Q(trunc_ln28_1_reg_98[7]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[8]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[40]),
        .Q(trunc_ln28_1_reg_98[8]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_1_reg_98_reg[9]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[41]),
        .Q(trunc_ln28_1_reg_98[9]),
        .R(\<const0> ));
  LUT3 #(
    .INIT(8'h0B))
    \trunc_ln28_reg_93[31]_i_1
       (.I0(data_in_empty_n_IBUF),
        .I1(grp_stream_fmacc_Pipeline_VITIS_LOOP_26_2_fu_79_ap_start_reg),
        .I2(data_in_dout_IBUF[64]),
        .O(\trunc_ln28_reg_93[31]_i_1_n_0 ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[0]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[0]),
        .Q(trunc_ln28_reg_93[0]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[10]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[10]),
        .Q(trunc_ln28_reg_93[10]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[11]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[11]),
        .Q(trunc_ln28_reg_93[11]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[12]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[12]),
        .Q(trunc_ln28_reg_93[12]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[13]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[13]),
        .Q(trunc_ln28_reg_93[13]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[14]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[14]),
        .Q(trunc_ln28_reg_93[14]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[15]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[15]),
        .Q(trunc_ln28_reg_93[15]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[16]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[16]),
        .Q(trunc_ln28_reg_93[16]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[17]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[17]),
        .Q(trunc_ln28_reg_93[17]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[18]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[18]),
        .Q(trunc_ln28_reg_93[18]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[19]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[19]),
        .Q(trunc_ln28_reg_93[19]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[1]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[1]),
        .Q(trunc_ln28_reg_93[1]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[20]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[20]),
        .Q(trunc_ln28_reg_93[20]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[21]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[21]),
        .Q(trunc_ln28_reg_93[21]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[22]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[22]),
        .Q(trunc_ln28_reg_93[22]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[23]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[23]),
        .Q(trunc_ln28_reg_93[23]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[24]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[24]),
        .Q(trunc_ln28_reg_93[24]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[25]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[25]),
        .Q(trunc_ln28_reg_93[25]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[26]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[26]),
        .Q(trunc_ln28_reg_93[26]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[27]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[27]),
        .Q(trunc_ln28_reg_93[27]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[28]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[28]),
        .Q(trunc_ln28_reg_93[28]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[29]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[29]),
        .Q(trunc_ln28_reg_93[29]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[2]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[2]),
        .Q(trunc_ln28_reg_93[2]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[30]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[30]),
        .Q(trunc_ln28_reg_93[30]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[31]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[31]),
        .Q(trunc_ln28_reg_93[31]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[3]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[3]),
        .Q(trunc_ln28_reg_93[3]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[4]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[4]),
        .Q(trunc_ln28_reg_93[4]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[5]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[5]),
        .Q(trunc_ln28_reg_93[5]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[6]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[6]),
        .Q(trunc_ln28_reg_93[6]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[7]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[7]),
        .Q(trunc_ln28_reg_93[7]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[8]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[8]),
        .Q(trunc_ln28_reg_93[8]),
        .R(\<const0> ));
  FDRE #(
    .INIT(1'b0))
    \trunc_ln28_reg_93_reg[9]
       (.C(CLK),
        .CE(\trunc_ln28_reg_93[31]_i_1_n_0 ),
        .D(data_in_dout_IBUF[9]),
        .Q(trunc_ln28_reg_93[9]),
        .R(\<const0> ));
endmodule
