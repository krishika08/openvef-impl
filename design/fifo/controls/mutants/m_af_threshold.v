// OpenVEF FIFO — original RTL, DRAFT for owner review.
// CONTROL MUTANT m_af_threshold (role M-exposed). AI-written (DEV-005, D-039, D-040): almost-full threshold 2, not 3 (breaks FIFO-029).
// Implements docs/fifo-spec-v0.2.md (DRAFT). Drafted by Claude (Claude Opus 5.5, via
// Claude Code) under owner decision D-005 (Krishika, 24 Nov 2026; Ayush's confirmation
// pending). Not approved, not frozen. Target: Icarus Verilog 12, -g2012; Yosys v0.71.
//
// Single clock, synchronous active-high reset (FIFO-003, FIFO-010). Every output is a
// register updated only at the rising edge of clk (FIFO-003, FIFO-029, FIFO-034).
// Behaviour for the illegal input of FIFO-031 (write while full without a read) is not
// specified; this RTL ignores such a write.
module ovf_fifo (
    input  wire       clk,
    input  wire       rst,
    input  wire       wr_en,
    input  wire [7:0] wr_data,
    input  wire       rd_en,
    output reg        rd_valid,
    output reg  [7:0] rd_data,
    output reg        full,
    output reg        almost_full,
    output reg        empty
);
    localparam integer DEPTH = 4;           // FIFO-001
    localparam integer AF_THRESHOLD = 2;    // FIFO-029

    reg [7:0] mem [0:DEPTH-1];
    reg [1:0] rd_ptr;
    reg [1:0] wr_ptr;
    reg [2:0] count;                         // occupancy c, 0..4 (FIFO-006)

    // FIFO-020: a read occurs when rd_en = 1 and c > 0 before the edge.
    wire       do_read  = rd_en && (count != 3'd0);
    // FIFO-024/-030: a write occurs when wr_en = 1 and (c < 4 or a read occurs).
    wire       do_write = wr_en && ((count != DEPTH) || do_read);
    // FIFO-027: c after = c before + write - read.
    wire [2:0] count_next = count + {2'b00, do_write} - {2'b00, do_read};

    always @(posedge clk) begin
        if (rst) begin                       // FIFO-010
            rd_ptr      <= 2'd0;
            wr_ptr      <= 2'd0;
            count       <= 3'd0;
            rd_valid    <= 1'b0;
            rd_data     <= 8'd0;             // don't-care (FIFO-022); driven to a known value
            full        <= 1'b0;
            almost_full <= 1'b0;
            empty       <= 1'b1;
        end else begin
            // FIFO-026/-030: the read takes mem[rd_ptr] before this edge's write lands
            // (nonblocking), so a word written at this edge cannot be read at it, and at
            // full the oldest word is read while the new word replaces it.
            if (do_read) begin
                rd_data <= mem[rd_ptr];
                rd_ptr  <= rd_ptr + 2'd1;
            end
            if (do_write) begin
                mem[wr_ptr] <= wr_data;
                wr_ptr      <= wr_ptr + 2'd1;
            end
            rd_valid    <= do_read;                        // FIFO-021, FIFO-023
            count       <= count_next;
            full        <= (count_next == DEPTH);          // FIFO-028
            empty       <= (count_next == 3'd0);           // FIFO-028
            almost_full <= (count_next >= AF_THRESHOLD);   // FIFO-029, FIFO-034, FIFO-035
        end
    end
endmodule
