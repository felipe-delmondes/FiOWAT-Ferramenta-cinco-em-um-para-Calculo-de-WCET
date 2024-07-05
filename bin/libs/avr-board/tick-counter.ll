; ModuleID = './bin/libs/avr-board/tick-counter.c'
source_filename = "./bin/libs/avr-board/tick-counter.c"
target datalayout = "e-P1-p:16:8-i8:8-i16:8-i32:8-i64:8-f32:8-f64:8-n8-a:8"
target triple = "avr-atmel-none"

@counter_overflow = dso_local global i8 0, align 1
@tempVar = dso_local global i16 0, align 1
@.str = private unnamed_addr constant [4 x i8] c"%u\0A\00", align 1
@startTime = dso_local global i16 0, align 1
@endTime = dso_local global i16 0, align 1
@execution_time = dso_local global i32 0, align 1
@llvm.compiler.used = appending global [1 x ptr] [ptr addrspacecast (ptr addrspace(1) @__vector_13 to ptr)], section "llvm.metadata"

; Function Attrs: noinline nounwind optnone
define dso_local void @InitTickCounter() addrspace(1) #0 !dbg !7 {
  store volatile i8 0, ptr inttoptr (i16 128 to ptr), align 1, !dbg !11
  store volatile i8 1, ptr inttoptr (i16 129 to ptr), align 1, !dbg !12
  ret void, !dbg !13
}

; Function Attrs: noinline nounwind optnone
define dso_local void @InitTickCounter_Overflow() addrspace(1) #0 !dbg !14 {
  store volatile i8 0, ptr inttoptr (i16 128 to ptr), align 1, !dbg !15
  store volatile i8 1, ptr inttoptr (i16 129 to ptr), align 1, !dbg !16
  %1 = load volatile i8, ptr inttoptr (i16 111 to ptr), align 1, !dbg !17
  %2 = zext i8 %1 to i16, !dbg !17
  %3 = or i16 %2, 1, !dbg !17
  %4 = trunc i16 %3 to i8, !dbg !17
  store volatile i8 %4, ptr inttoptr (i16 111 to ptr), align 1, !dbg !17
  call addrspace(0) void asm sideeffect "sei", "~{memory}"() #3, !dbg !18, !srcloc !19
  ret void, !dbg !20
}

; Function Attrs: noinline nounwind optnone
define dso_local void @CaptureTickCounter() addrspace(1) #0 !dbg !21 {
  %1 = load volatile i16, ptr inttoptr (i16 132 to ptr), align 1, !dbg !22
  store i16 %1, ptr @tempVar, align 1, !dbg !23
  ret void, !dbg !24
}

; Function Attrs: noinline nounwind optnone
define dso_local void @ResetTickCounter() addrspace(1) #0 !dbg !25 {
  store volatile i16 0, ptr inttoptr (i16 132 to ptr), align 1, !dbg !26
  ret void, !dbg !27
}

; Function Attrs: noinline nounwind optnone
define dso_local void @PrintTickCounter() addrspace(1) #0 !dbg !28 {
  %1 = load i16, ptr @tempVar, align 1, !dbg !29
  %2 = call addrspace(1) i16 (ptr, ...) @printf(ptr noundef @.str, i16 noundef %1), !dbg !30
  ret void, !dbg !31
}

declare dso_local i16 @printf(ptr noundef, ...) addrspace(1) #1

; Function Attrs: noinline nounwind optnone
define dso_local void @StartTickCounter() addrspace(1) #0 !dbg !32 {
  %1 = load volatile i16, ptr inttoptr (i16 132 to ptr), align 1, !dbg !33
  store i16 %1, ptr @startTime, align 1, !dbg !34
  ret void, !dbg !35
}

; Function Attrs: noinline nounwind optnone
define dso_local void @StopTickCounter() addrspace(1) #0 !dbg !36 {
  %1 = load volatile i16, ptr inttoptr (i16 132 to ptr), align 1, !dbg !37
  store i16 %1, ptr @endTime, align 1, !dbg !38
  ret void, !dbg !39
}

; Function Attrs: noinline nounwind optnone
define dso_local i32 @GetTick_Overflow() addrspace(1) #0 !dbg !40 {
  %1 = load i8, ptr @counter_overflow, align 1, !dbg !41
  %2 = sext i8 %1 to i32, !dbg !41
  %3 = mul nsw i32 %2, 65535, !dbg !42
  %4 = load i16, ptr @endTime, align 1, !dbg !43
  %5 = sext i16 %4 to i32, !dbg !43
  %6 = add nsw i32 %3, %5, !dbg !44
  %7 = load i16, ptr @startTime, align 1, !dbg !45
  %8 = sext i16 %7 to i32, !dbg !45
  %9 = sub nsw i32 %6, %8, !dbg !46
  ret i32 %9, !dbg !47
}

; Function Attrs: noinline nounwind optnone
define dso_local void @__vector_13() addrspace(1) #2 !dbg !48 {
  %1 = load i8, ptr @counter_overflow, align 1, !dbg !49
  %2 = add i8 %1, 1, !dbg !49
  store i8 %2, ptr @counter_overflow, align 1, !dbg !49
  call addrspace(1) void @ResetTickCounter(), !dbg !50
  ret void, !dbg !51
}

attributes #0 = { noinline nounwind optnone "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="atmega328" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="atmega328" }
attributes #2 = { noinline nounwind optnone "frame-pointer"="all" "no-trapping-math"="true" "signal" "stack-protector-buffer-size"="8" "target-cpu"="atmega328" }
attributes #3 = { nounwind }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "Ubuntu clang version 16.0.6 (++20230710042027+7cbf1a259152-1~exp1~20230710162048.105)", isOptimized: false, runtimeVersion: 0, emissionKind: LineTablesOnly, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "bin/libs/avr-board/tick-counter.c", directory: "/home/munak98/Documents/TCC-PES", checksumkind: CSK_MD5, checksum: "30e019955cace7c5cc66909da446ecd5")
!2 = !{i32 7, !"Dwarf Version", i32 5}
!3 = !{i32 2, !"Debug Info Version", i32 3}
!4 = !{i32 1, !"wchar_size", i32 2}
!5 = !{i32 7, !"frame-pointer", i32 2}
!6 = !{!"Ubuntu clang version 16.0.6 (++20230710042027+7cbf1a259152-1~exp1~20230710162048.105)"}
!7 = distinct !DISubprogram(name: "InitTickCounter", scope: !8, file: !8, line: 8, type: !9, scopeLine: 8, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !10)
!8 = !DIFile(filename: "./bin/libs/avr-board/tick-counter.c", directory: "/home/munak98/Documents/TCC-PES", checksumkind: CSK_MD5, checksum: "30e019955cace7c5cc66909da446ecd5")
!9 = !DISubroutineType(types: !10)
!10 = !{}
!11 = !DILocation(line: 9, column: 12, scope: !7)
!12 = !DILocation(line: 10, column: 12, scope: !7)
!13 = !DILocation(line: 12, column: 1, scope: !7)
!14 = distinct !DISubprogram(name: "InitTickCounter_Overflow", scope: !8, file: !8, line: 14, type: !9, scopeLine: 14, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !10)
!15 = !DILocation(line: 15, column: 12, scope: !14)
!16 = !DILocation(line: 16, column: 12, scope: !14)
!17 = !DILocation(line: 17, column: 12, scope: !14)
!18 = !DILocation(line: 18, column: 5, scope: !14)
!19 = !{i64 2147680910}
!20 = !DILocation(line: 19, column: 1, scope: !14)
!21 = distinct !DISubprogram(name: "CaptureTickCounter", scope: !8, file: !8, line: 21, type: !9, scopeLine: 21, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !10)
!22 = !DILocation(line: 22, column: 15, scope: !21)
!23 = !DILocation(line: 22, column: 13, scope: !21)
!24 = !DILocation(line: 23, column: 1, scope: !21)
!25 = distinct !DISubprogram(name: "ResetTickCounter", scope: !8, file: !8, line: 25, type: !9, scopeLine: 25, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !10)
!26 = !DILocation(line: 26, column: 11, scope: !25)
!27 = !DILocation(line: 27, column: 1, scope: !25)
!28 = distinct !DISubprogram(name: "PrintTickCounter", scope: !8, file: !8, line: 29, type: !9, scopeLine: 29, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !10)
!29 = !DILocation(line: 30, column: 20, scope: !28)
!30 = !DILocation(line: 30, column: 5, scope: !28)
!31 = !DILocation(line: 31, column: 1, scope: !28)
!32 = distinct !DISubprogram(name: "StartTickCounter", scope: !8, file: !8, line: 33, type: !9, scopeLine: 33, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !10)
!33 = !DILocation(line: 34, column: 17, scope: !32)
!34 = !DILocation(line: 34, column: 15, scope: !32)
!35 = !DILocation(line: 35, column: 1, scope: !32)
!36 = distinct !DISubprogram(name: "StopTickCounter", scope: !8, file: !8, line: 36, type: !9, scopeLine: 36, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !10)
!37 = !DILocation(line: 37, column: 15, scope: !36)
!38 = !DILocation(line: 37, column: 13, scope: !36)
!39 = !DILocation(line: 38, column: 1, scope: !36)
!40 = distinct !DISubprogram(name: "GetTick_Overflow", scope: !8, file: !8, line: 40, type: !9, scopeLine: 40, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !10)
!41 = !DILocation(line: 41, column: 12, scope: !40)
!42 = !DILocation(line: 41, column: 28, scope: !40)
!43 = !DILocation(line: 41, column: 39, scope: !40)
!44 = !DILocation(line: 41, column: 37, scope: !40)
!45 = !DILocation(line: 41, column: 49, scope: !40)
!46 = !DILocation(line: 41, column: 47, scope: !40)
!47 = !DILocation(line: 41, column: 5, scope: !40)
!48 = distinct !DISubprogram(name: "__vector_13", scope: !8, file: !8, line: 44, type: !9, scopeLine: 44, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !10)
!49 = !DILocation(line: 45, column: 21, scope: !48)
!50 = !DILocation(line: 46, column: 5, scope: !48)
!51 = !DILocation(line: 47, column: 1, scope: !48)
