	.text
.set __tmp_reg__, 0
.set __zero_reg__, 1
.set __SREG__, 63
.set __SP_H__, 62
.set __SP_L__, 61
	.file	"test.c"
	.globl	BubbleSort                      ; -- Begin function BubbleSort
	.p2align	1
	.type	BubbleSort,@function
BubbleSort:                             ; @BubbleSort
.Lfunc_begin0:
	.file	0 "/home/munak98/Documents/TCC-PES" "/home/munak98/Documents/TCC-PES/test/input/test.c" md5 0x855e9a39d89164001846c4527d1be6a1
	.file	1 "test/input" "test.c" md5 0x855e9a39d89164001846c4527d1be6a1
	.loc	1 9 0                           ; test/input/test.c:9:0
; %bb.0:
	push	r28
	push	r29
	in	r28, 61
	in	r29, 62
	sbiw	r28, 14
	in	r0, 63
	cli
	out	62, r29
	out	63, r0
	out	61, r28
	std	Y+13, r24
	std	Y+14, r25
	ldi	r24, 0
	ldi	r25, 0
.Ltmp0:
	.loc	1 10 6 prologue_end             ; test/input/test.c:10:6
	std	Y+11, r24
	std	Y+12, r25
	.loc	1 13 9                          ; test/input/test.c:13:9
	std	Y+5, r24
	std	Y+6, r25
	.loc	1 13 7 is_stmt 0                ; test/input/test.c:13:7
	rjmp	.LBB0_1
.LBB0_1:                                ; =>This Loop Header: Depth=1
                                        ;     Child Loop BB0_3 Depth 2
	.loc	1 13 14                         ; test/input/test.c:13:14
	ldd	r24, Y+5
	ldd	r25, Y+6
	.loc	1 13 2                          ; test/input/test.c:13:2
	mov	r18, r24
	mov	r24, r25
	mov	r25, r1
	cpi	r18, 10
	cpc	r24, r25
	brlt	.LBB0_2
	rjmp	.LBB0_14
.LBB0_2:                                ;   in Loop: Header=BB0_1 Depth=1
	.loc	1 0 2                           ; test/input/test.c:0:2
	ldi	r24, 1
	ldi	r25, 0
	.loc	1 14 10 is_stmt 1               ; test/input/test.c:14:10
	std	Y+11, r24
	std	Y+12, r25
	ldi	r24, 0
	ldi	r25, 0
	.loc	1 15 14                         ; test/input/test.c:15:14
	std	Y+7, r24
	std	Y+8, r25
	.loc	1 15 8 is_stmt 0                ; test/input/test.c:15:8
	rjmp	.LBB0_3
.LBB0_3:                                ;   Parent Loop BB0_1 Depth=1
                                        ; =>  This Inner Loop Header: Depth=2
	.loc	1 15 19                         ; test/input/test.c:15:19
	ldd	r24, Y+7
	ldd	r25, Y+8
	.loc	1 15 3                          ; test/input/test.c:15:3
	mov	r18, r24
	mov	r24, r25
	mov	r25, r1
	cpi	r18, 10
	cpc	r24, r25
	brlt	.LBB0_4
	rjmp	.LBB0_10
.LBB0_4:                                ;   in Loop: Header=BB0_3 Depth=2
	.loc	1 16 8 is_stmt 1                ; test/input/test.c:16:8
	ldd	r24, Y+7
	ldd	r25, Y+8
	.loc	1 16 28 is_stmt 0               ; test/input/test.c:16:28
	ldd	r20, Y+5
	ldd	r21, Y+6
	ldi	r18, 9
	ldi	r19, 0
	.loc	1 16 30                         ; test/input/test.c:16:30
	sub	r18, r20
	sbc	r19, r21
	.loc	1 16 8                          ; test/input/test.c:16:8
	cp	r24, r18
	cpc	r25, r19
	brlt	.LBB0_6
	rjmp	.LBB0_5
.LBB0_5:                                ;   in Loop: Header=BB0_1 Depth=1
	.loc	1 17 5 is_stmt 1                ; test/input/test.c:17:5
	rjmp	.LBB0_10
.LBB0_6:                                ;   in Loop: Header=BB0_3 Depth=2
	.loc	1 18 8                          ; test/input/test.c:18:8
	ldd	r30, Y+13
	ldd	r31, Y+14
	.loc	1 18 14 is_stmt 0               ; test/input/test.c:18:14
	ldd	r24, Y+7
	ldd	r25, Y+8
	.loc	1 18 8                          ; test/input/test.c:18:8
	lsl	r24
	rol	r25
	add	r30, r24
	adc	r31, r25
	std	Y+3, r30                        ; 2-byte Folded Spill
	std	Y+4, r31                        ; 2-byte Folded Spill
	ld	r18, Z
	ldd	r19, Z+1
	ldd	r30, Y+3                        ; 2-byte Folded Reload
	ldd	r31, Y+4                        ; 2-byte Folded Reload
	.loc	1 18 23                         ; test/input/test.c:18:23
	ldd	r24, Z+2
	ldd	r25, Z+3
	.loc	1 18 8                          ; test/input/test.c:18:8
	cp	r24, r18
	cpc	r25, r19
	brlt	.LBB0_7
	rjmp	.LBB0_8
.LBB0_7:                                ;   in Loop: Header=BB0_3 Depth=2
	.loc	1 19 12 is_stmt 1               ; test/input/test.c:19:12
	ldd	r30, Y+13
	ldd	r31, Y+14
	.loc	1 19 18 is_stmt 0               ; test/input/test.c:19:18
	ldd	r24, Y+7
	ldd	r25, Y+8
	.loc	1 19 12                         ; test/input/test.c:19:12
	lsl	r24
	rol	r25
	add	r30, r24
	adc	r31, r25
	ld	r24, Z
	ldd	r25, Z+1
	.loc	1 19 10                         ; test/input/test.c:19:10
	std	Y+9, r24
	std	Y+10, r25
	.loc	1 20 20 is_stmt 1               ; test/input/test.c:20:20
	ldd	r30, Y+13
	ldd	r31, Y+14
	.loc	1 20 26 is_stmt 0               ; test/input/test.c:20:26
	ldd	r24, Y+7
	ldd	r25, Y+8
	.loc	1 20 32                         ; test/input/test.c:20:32
	lsl	r24
	rol	r25
	.loc	1 20 5                          ; test/input/test.c:20:5
	add	r30, r24
	adc	r31, r25
	std	Y+1, r30                        ; 2-byte Folded Spill
	std	Y+2, r31                        ; 2-byte Folded Spill
	.loc	1 20 20                         ; test/input/test.c:20:20
	ldd	r24, Z+2
	ldd	r25, Z+3
	ldd	r30, Y+1                        ; 2-byte Folded Reload
	ldd	r31, Y+2                        ; 2-byte Folded Reload
	.loc	1 20 18                         ; test/input/test.c:20:18
	st	Z, r24
	std	Z+1, r25
	.loc	1 21 24 is_stmt 1               ; test/input/test.c:21:24
	ldd	r24, Y+9
	ldd	r25, Y+10
	.loc	1 21 5 is_stmt 0                ; test/input/test.c:21:5
	ldd	r18, Y+13
	ldd	r19, Y+14
	.loc	1 21 11                         ; test/input/test.c:21:11
	ldd	r30, Y+7
	ldd	r31, Y+8
	.loc	1 21 17                         ; test/input/test.c:21:17
	lsl	r30
	rol	r31
	.loc	1 21 5                          ; test/input/test.c:21:5
	add	r30, r18
	adc	r31, r19
	.loc	1 21 22                         ; test/input/test.c:21:22
	std	Z+2, r24
	std	Z+3, r25
	ldi	r24, 0
	ldi	r25, 0
	.loc	1 22 12 is_stmt 1               ; test/input/test.c:22:12
	std	Y+11, r24
	std	Y+12, r25
	.loc	1 23 4                          ; test/input/test.c:23:4
	rjmp	.LBB0_8
.LBB0_8:                                ;   in Loop: Header=BB0_3 Depth=2
	.loc	1 24 3                          ; test/input/test.c:24:3
	rjmp	.LBB0_9
.LBB0_9:                                ;   in Loop: Header=BB0_3 Depth=2
	.loc	1 15 42                         ; test/input/test.c:15:42
	ldd	r24, Y+7
	ldd	r25, Y+8
	adiw	r24, 1
	std	Y+7, r24
	std	Y+8, r25
	.loc	1 15 3 is_stmt 0                ; test/input/test.c:15:3
	rjmp	.LBB0_3
.LBB0_10:                               ;   in Loop: Header=BB0_1 Depth=1
	.loc	1 25 7 is_stmt 1                ; test/input/test.c:25:7
	ldd	r24, Y+11
	ldd	r25, Y+12
	mov	r18, r24
	mov	r24, r25
	mov	r25, r1
	cpi	r18, 0
	cpc	r24, r25
	breq	.LBB0_12
	rjmp	.LBB0_11
.LBB0_11:
	.loc	1 26 4                          ; test/input/test.c:26:4
	rjmp	.LBB0_14
.LBB0_12:                               ;   in Loop: Header=BB0_1 Depth=1
	.loc	1 27 2                          ; test/input/test.c:27:2
	rjmp	.LBB0_13
.LBB0_13:                               ;   in Loop: Header=BB0_1 Depth=1
	.loc	1 13 29                         ; test/input/test.c:13:29
	ldd	r24, Y+5
	ldd	r25, Y+6
	adiw	r24, 1
	std	Y+5, r24
	std	Y+6, r25
	.loc	1 13 2 is_stmt 0                ; test/input/test.c:13:2
	rjmp	.LBB0_1
.LBB0_14:
	.loc	1 28 1 is_stmt 1                ; test/input/test.c:28:1
	adiw	r28, 14
	in	r0, 63
	cli
	out	62, r29
	out	63, r0
	out	61, r28
	pop	r29
	pop	r28
	ret
.Ltmp1:
.Lfunc_end0:
	.size	BubbleSort, .Lfunc_end0-BubbleSort
                                        ; -- End function
	.globl	main                            ; -- Begin function main
	.p2align	1
	.type	main,@function
main:                                   ; @main
.Lfunc_begin1:
	.loc	1 30 0                          ; test/input/test.c:30:0
; %bb.0:
	push	r28
	push	r29
	in	r28, 61
	in	r29, 62
	sbiw	r28, 8
	in	r0, 63
	cli
	out	62, r29
	out	63, r0
	out	61, r28
	ldi	r24, 0
	ldi	r25, 0
	std	Y+7, r24
	std	Y+8, r25
.Ltmp2:
	.loc	1 31 10 prologue_end            ; test/input/test.c:31:10
	std	Y+5, r24
	std	Y+6, r25
	.loc	1 31 6 is_stmt 0                ; test/input/test.c:31:6
	rjmp	.LBB1_1
.LBB1_1:                                ; =>This Inner Loop Header: Depth=1
	.loc	1 31 17                         ; test/input/test.c:31:17
	ldd	r24, Y+5
	ldd	r25, Y+6
	.loc	1 31 2                          ; test/input/test.c:31:2
	mov	r18, r24
	mov	r24, r25
	mov	r25, r1
	cpi	r18, 10
	cpc	r24, r25
	brge	.LBB1_4
	rjmp	.LBB1_2
.LBB1_2:                                ;   in Loop: Header=BB1_1 Depth=1
	.loc	1 32 3 is_stmt 1                ; test/input/test.c:32:3
	ldi	r24, lo8(.str)
	ldi	r25, hi8(.str)
	std	Y+1, r24
	std	Y+2, r25
	call	printf
	.loc	1 33 22                         ; test/input/test.c:33:22
	ldd	r24, Y+5
	ldd	r25, Y+6
	.loc	1 33 16 is_stmt 0               ; test/input/test.c:33:16
	lsl	r24
	rol	r25
	subi	r24, lo8(-(Array))
	sbci	r25, hi8(-(Array))
	.loc	1 33 3                          ; test/input/test.c:33:3
	ldi	r18, lo8(.str.1)
	ldi	r19, hi8(.str.1)
	std	Y+1, r18
	std	Y+2, r19
	std	Y+3, r24
	std	Y+4, r25
	call	scanf
	.loc	1 34 2 is_stmt 1                ; test/input/test.c:34:2
	rjmp	.LBB1_3
.LBB1_3:                                ;   in Loop: Header=BB1_1 Depth=1
	.loc	1 31 32                         ; test/input/test.c:31:32
	ldd	r24, Y+5
	ldd	r25, Y+6
	adiw	r24, 1
	std	Y+5, r24
	std	Y+6, r25
	.loc	1 31 2 is_stmt 0                ; test/input/test.c:31:2
	rjmp	.LBB1_1
.LBB1_4:
	.loc	1 35 2 is_stmt 1                ; test/input/test.c:35:2
	ldi	r24, lo8(Array)
	ldi	r25, hi8(Array)
	call	BubbleSort
	ldi	r24, 0
	ldi	r25, 0
	.loc	1 36 2                          ; test/input/test.c:36:2
	adiw	r28, 8
	in	r0, 63
	cli
	out	62, r29
	out	63, r0
	out	61, r28
	pop	r29
	pop	r28
	ret
.Ltmp3:
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
                                        ; -- End function
	; Declaring this symbol tells the CRT that it should
	;copy all variables from program memory to RAM on startup
	.globl	__do_copy_data
	; Declaring this symbol tells the CRT that it should
	;clear the zeroed data section on startup
	.globl	__do_clear_bss
	.type	.str,@object                    ; @.str
	.section	.rodata.str1.1,"aMS",@progbits,1
.str:
	.asciz	"Input\n"
	.size	.str, 7

	.type	.str.1,@object                  ; @.str.1
.str.1:
	.asciz	"%d"
	.size	.str.1, 3

	.type	Array,@object                   ; @Array
	.section	.bss,"aw",@nobits
	.globl	Array
Array:
	.zero	20
	.size	Array, 20

	.section	.debug_abbrev,"",@progbits
	.byte	1                               ; Abbreviation Code
	.byte	17                              ; DW_TAG_compile_unit
	.byte	0                               ; DW_CHILDREN_no
	.byte	37                              ; DW_AT_producer
	.byte	37                              ; DW_FORM_strx1
	.byte	19                              ; DW_AT_language
	.byte	5                               ; DW_FORM_data2
	.byte	3                               ; DW_AT_name
	.byte	37                              ; DW_FORM_strx1
	.byte	114                             ; DW_AT_str_offsets_base
	.byte	23                              ; DW_FORM_sec_offset
	.byte	16                              ; DW_AT_stmt_list
	.byte	23                              ; DW_FORM_sec_offset
	.byte	27                              ; DW_AT_comp_dir
	.byte	37                              ; DW_FORM_strx1
	.byte	17                              ; DW_AT_low_pc
	.byte	27                              ; DW_FORM_addrx
	.byte	18                              ; DW_AT_high_pc
	.byte	6                               ; DW_FORM_data4
	.byte	115                             ; DW_AT_addr_base
	.byte	23                              ; DW_FORM_sec_offset
	.byte	0                               ; EOM(1)
	.byte	0                               ; EOM(2)
	.byte	0                               ; EOM(3)
	.section	.debug_info,"",@progbits
.Lcu_begin0:
	.long	.Ldebug_info_end0-.Ldebug_info_start0 ; Length of Unit
.Ldebug_info_start0:
	.short	5                               ; DWARF version number
	.byte	1                               ; DWARF Unit Type
	.byte	2                               ; Address Size (in bytes)
	.long	.debug_abbrev                   ; Offset Into Abbrev. Section
	.byte	1                               ; Abbrev [1] 0xc:0x17 DW_TAG_compile_unit
	.byte	0                               ; DW_AT_producer
	.short	29                              ; DW_AT_language
	.byte	1                               ; DW_AT_name
	.long	.Lstr_offsets_base0             ; DW_AT_str_offsets_base
	.long	.Lline_table_start0             ; DW_AT_stmt_list
	.byte	2                               ; DW_AT_comp_dir
	.byte	0                               ; DW_AT_low_pc
	.long	.Lfunc_end1-.Lfunc_begin0       ; DW_AT_high_pc
	.long	.Laddr_table_base0              ; DW_AT_addr_base
.Ldebug_info_end0:
	.section	.debug_str_offsets,"",@progbits
	.long	16                              ; Length of String Offsets Set
	.short	5
	.short	0
.Lstr_offsets_base0:
	.section	.debug_str,"MS",@progbits,1
.Linfo_string0:
	.asciz	"Ubuntu clang version 16.0.6 (++20230710042027+7cbf1a259152-1~exp1~20230710162048.105)" ; string offset=0
.Linfo_string1:
	.asciz	"/home/munak98/Documents/TCC-PES/test/input/test.c" ; string offset=86
.Linfo_string2:
	.asciz	"/home/munak98/Documents/TCC-PES" ; string offset=136
	.section	.debug_str_offsets,"",@progbits
	.long	.Linfo_string0
	.long	.Linfo_string1
	.long	.Linfo_string2
	.section	.debug_addr,"",@progbits
	.long	.Ldebug_addr_end0-.Ldebug_addr_start0 ; Length of contribution
.Ldebug_addr_start0:
	.short	5                               ; DWARF version number
	.byte	2                               ; Address size
	.byte	0                               ; Segment selector size
.Laddr_table_base0:
	.short	.Lfunc_begin0
.Ldebug_addr_end0:
	.section	.debug_line,"",@progbits
.Lline_table_start0:
