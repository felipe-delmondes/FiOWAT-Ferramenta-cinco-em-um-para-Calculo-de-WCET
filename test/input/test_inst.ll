; ModuleID = '/home/munak98/Documents/TCC-PES/test/input/test_inst.ll'
source_filename = "/home/munak98/Documents/TCC-PES/test/input/test_inst.c"
target datalayout = "e-P1-p:16:8-i8:8-i16:8-i32:8-i64:8-f32:8-f64:8-n8-a:8"
target triple = "avr-atmel-none"

@.str = private unnamed_addr constant [7 x i8] c"Input\0A\00", align 1
@.str.1 = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@Array = dso_local global [10 x i16] zeroinitializer, align 1
@0 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@1 = private unnamed_addr constant [20 x i8] c"#;BubbleSort;block0\00", align 1
@2 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@3 = private unnamed_addr constant [20 x i8] c"#;BubbleSort;block1\00", align 1
@4 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@5 = private unnamed_addr constant [20 x i8] c"#;BubbleSort;block2\00", align 1
@6 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@7 = private unnamed_addr constant [20 x i8] c"#;BubbleSort;block3\00", align 1
@8 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@9 = private unnamed_addr constant [20 x i8] c"#;BubbleSort;block4\00", align 1
@10 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@11 = private unnamed_addr constant [20 x i8] c"#;BubbleSort;block5\00", align 1
@12 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@13 = private unnamed_addr constant [20 x i8] c"#;BubbleSort;block6\00", align 1
@14 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@15 = private unnamed_addr constant [20 x i8] c"#;BubbleSort;block7\00", align 1
@16 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@17 = private unnamed_addr constant [20 x i8] c"#;BubbleSort;block8\00", align 1
@18 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@19 = private unnamed_addr constant [20 x i8] c"#;BubbleSort;block9\00", align 1
@20 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@21 = private unnamed_addr constant [21 x i8] c"#;BubbleSort;block10\00", align 1
@22 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@23 = private unnamed_addr constant [21 x i8] c"#;BubbleSort;block11\00", align 1
@24 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@25 = private unnamed_addr constant [21 x i8] c"#;BubbleSort;block12\00", align 1
@26 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@27 = private unnamed_addr constant [21 x i8] c"#;BubbleSort;block13\00", align 1
@28 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@29 = private unnamed_addr constant [21 x i8] c"#;BubbleSort;block14\00", align 1

; Function Attrs: noinline nounwind optnone
define dso_local void @BubbleSort(ptr noundef %0) addrspace(1) #0 !dbg !7 {
"#;BubbleSort;block0":
  %1 = call addrspace(1) i32 (ptr, ...) @printf(ptr @0, ptr @1)
  %2 = alloca ptr, align 1
  %3 = alloca i16, align 1
  %4 = alloca i16, align 1
  %5 = alloca i16, align 1
  %6 = alloca i16, align 1
  store ptr %0, ptr %2, align 1
  store i16 0, ptr %3, align 1, !dbg !11
  store i16 0, ptr %6, align 1, !dbg !12
  br label %"#;BubbleSort;block1", !dbg !13

"#;BubbleSort;block1":                            ; preds = %"#;BubbleSort;block13", %"#;BubbleSort;block0"
  %7 = call addrspace(1) i32 (ptr, ...) @printf(ptr @2, ptr @3), !dbg !14
  %8 = load i16, ptr %6, align 1, !dbg !14
  %9 = icmp slt i16 %8, 10, !dbg !15
  br i1 %9, label %"#;BubbleSort;block2", label %"#;BubbleSort;block14", !dbg !16

"#;BubbleSort;block2":                            ; preds = %"#;BubbleSort;block1"
  %10 = call addrspace(1) i32 (ptr, ...) @printf(ptr @4, ptr @5), !dbg !17
  store i16 1, ptr %3, align 1, !dbg !17
  store i16 0, ptr %5, align 1, !dbg !18
  br label %"#;BubbleSort;block3", !dbg !19

"#;BubbleSort;block3":                            ; preds = %"#;BubbleSort;block9", %"#;BubbleSort;block2"
  %11 = call addrspace(1) i32 (ptr, ...) @printf(ptr @6, ptr @7), !dbg !20
  %12 = load i16, ptr %5, align 1, !dbg !20
  %13 = icmp slt i16 %12, 10, !dbg !21
  br i1 %13, label %"#;BubbleSort;block4", label %"#;BubbleSort;block10", !dbg !22

"#;BubbleSort;block4":                            ; preds = %"#;BubbleSort;block3"
  %14 = call addrspace(1) i32 (ptr, ...) @printf(ptr @8, ptr @9), !dbg !23
  %15 = load i16, ptr %5, align 1, !dbg !23
  %16 = load i16, ptr %6, align 1, !dbg !24
  %17 = sub nsw i16 10, %16, !dbg !25
  %18 = sub nsw i16 %17, 1, !dbg !26
  %19 = icmp sge i16 %15, %18, !dbg !27
  br i1 %19, label %"#;BubbleSort;block5", label %"#;BubbleSort;block6", !dbg !23

"#;BubbleSort;block5":                            ; preds = %"#;BubbleSort;block4"
  %20 = call addrspace(1) i32 (ptr, ...) @printf(ptr @10, ptr @11), !dbg !28
  br label %"#;BubbleSort;block10", !dbg !28

"#;BubbleSort;block6":                            ; preds = %"#;BubbleSort;block4"
  %21 = call addrspace(1) i32 (ptr, ...) @printf(ptr @12, ptr @13), !dbg !29
  %22 = load ptr, ptr %2, align 1, !dbg !29
  %23 = load i16, ptr %5, align 1, !dbg !30
  %24 = getelementptr inbounds i16, ptr %22, i16 %23, !dbg !29
  %25 = load i16, ptr %24, align 1, !dbg !29
  %26 = load ptr, ptr %2, align 1, !dbg !31
  %27 = load i16, ptr %5, align 1, !dbg !32
  %28 = add nsw i16 %27, 1, !dbg !33
  %29 = getelementptr inbounds i16, ptr %26, i16 %28, !dbg !31
  %30 = load i16, ptr %29, align 1, !dbg !31
  %31 = icmp sgt i16 %25, %30, !dbg !34
  br i1 %31, label %"#;BubbleSort;block7", label %"#;BubbleSort;block8", !dbg !29

"#;BubbleSort;block7":                            ; preds = %"#;BubbleSort;block6"
  %32 = call addrspace(1) i32 (ptr, ...) @printf(ptr @14, ptr @15), !dbg !35
  %33 = load ptr, ptr %2, align 1, !dbg !35
  %34 = load i16, ptr %5, align 1, !dbg !36
  %35 = getelementptr inbounds i16, ptr %33, i16 %34, !dbg !35
  %36 = load i16, ptr %35, align 1, !dbg !35
  store i16 %36, ptr %4, align 1, !dbg !37
  %37 = load ptr, ptr %2, align 1, !dbg !38
  %38 = load i16, ptr %5, align 1, !dbg !39
  %39 = add nsw i16 %38, 1, !dbg !40
  %40 = getelementptr inbounds i16, ptr %37, i16 %39, !dbg !38
  %41 = load i16, ptr %40, align 1, !dbg !38
  %42 = load ptr, ptr %2, align 1, !dbg !41
  %43 = load i16, ptr %5, align 1, !dbg !42
  %44 = getelementptr inbounds i16, ptr %42, i16 %43, !dbg !41
  store i16 %41, ptr %44, align 1, !dbg !43
  %45 = load i16, ptr %4, align 1, !dbg !44
  %46 = load ptr, ptr %2, align 1, !dbg !45
  %47 = load i16, ptr %5, align 1, !dbg !46
  %48 = add nsw i16 %47, 1, !dbg !47
  %49 = getelementptr inbounds i16, ptr %46, i16 %48, !dbg !45
  store i16 %45, ptr %49, align 1, !dbg !48
  store i16 0, ptr %3, align 1, !dbg !49
  br label %"#;BubbleSort;block8", !dbg !50

"#;BubbleSort;block8":                            ; preds = %"#;BubbleSort;block7", %"#;BubbleSort;block6"
  %50 = call addrspace(1) i32 (ptr, ...) @printf(ptr @16, ptr @17), !dbg !51
  br label %"#;BubbleSort;block9", !dbg !51

"#;BubbleSort;block9":                            ; preds = %"#;BubbleSort;block8"
  %51 = call addrspace(1) i32 (ptr, ...) @printf(ptr @18, ptr @19), !dbg !52
  %52 = load i16, ptr %5, align 1, !dbg !52
  %53 = add nsw i16 %52, 1, !dbg !52
  store i16 %53, ptr %5, align 1, !dbg !52
  br label %"#;BubbleSort;block3", !dbg !22, !llvm.loop !53

"#;BubbleSort;block10":                           ; preds = %"#;BubbleSort;block5", %"#;BubbleSort;block3"
  %54 = call addrspace(1) i32 (ptr, ...) @printf(ptr @20, ptr @21), !dbg !55
  %55 = load i16, ptr %3, align 1, !dbg !55
  %56 = icmp ne i16 %55, 0, !dbg !55
  br i1 %56, label %"#;BubbleSort;block11", label %"#;BubbleSort;block12", !dbg !55

"#;BubbleSort;block11":                           ; preds = %"#;BubbleSort;block10"
  %57 = call addrspace(1) i32 (ptr, ...) @printf(ptr @22, ptr @23), !dbg !56
  br label %"#;BubbleSort;block14", !dbg !56

"#;BubbleSort;block12":                           ; preds = %"#;BubbleSort;block10"
  %58 = call addrspace(1) i32 (ptr, ...) @printf(ptr @24, ptr @25), !dbg !57
  br label %"#;BubbleSort;block13", !dbg !57

"#;BubbleSort;block13":                           ; preds = %"#;BubbleSort;block12"
  %59 = call addrspace(1) i32 (ptr, ...) @printf(ptr @26, ptr @27), !dbg !58
  %60 = load i16, ptr %6, align 1, !dbg !58
  %61 = add nsw i16 %60, 1, !dbg !58
  store i16 %61, ptr %6, align 1, !dbg !58
  br label %"#;BubbleSort;block1", !dbg !16, !llvm.loop !59

"#;BubbleSort;block14":                           ; preds = %"#;BubbleSort;block11", %"#;BubbleSort;block1"
  %62 = call addrspace(1) i32 (ptr, ...) @printf(ptr @28, ptr @29), !dbg !60
  ret void, !dbg !60
}

; Function Attrs: noinline nounwind optnone
define dso_local i16 @main() addrspace(1) #0 !dbg !61 {
"#;main;block0":
  %0 = alloca i16, align 1
  %1 = alloca i16, align 1
  store i16 0, ptr %0, align 1
  store i16 0, ptr %1, align 1, !dbg !62
  br label %"#;main;block1", !dbg !63

"#;main;block1":                                  ; preds = %"#;main;block3", %"#;main;block0"
  %2 = load i16, ptr %1, align 1, !dbg !64
  %3 = icmp slt i16 %2, 10, !dbg !65
  br i1 %3, label %"#;main;block2", label %"#;main;block4", !dbg !66

"#;main;block2":                                  ; preds = %"#;main;block1"
  %4 = call addrspace(1) i16 (ptr, ...) @printf(ptr noundef @.str), !dbg !67
  %5 = load i16, ptr %1, align 1, !dbg !68
  %6 = getelementptr inbounds [10 x i16], ptr @Array, i16 0, i16 %5, !dbg !69
  %7 = call addrspace(1) i16 (ptr, ...) @scanf(ptr noundef @.str.1, ptr noundef %6), !dbg !70
  br label %"#;main;block3", !dbg !71

"#;main;block3":                                  ; preds = %"#;main;block2"
  %8 = load i16, ptr %1, align 1, !dbg !72
  %9 = add nsw i16 %8, 1, !dbg !72
  store i16 %9, ptr %1, align 1, !dbg !72
  br label %"#;main;block1", !dbg !66, !llvm.loop !73

"#;main;block4":                                  ; preds = %"#;main;block1"
  call addrspace(1) void @BubbleSort(ptr noundef @Array), !dbg !74
  ret i16 0, !dbg !75
}

declare dso_local i16 @printf(ptr noundef, ...) addrspace(1) #1

declare dso_local i16 @scanf(ptr noundef, ...) addrspace(1) #1

attributes #0 = { noinline nounwind optnone "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="atmega328" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="atmega328" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "Ubuntu clang version 16.0.6 (++20230710042027+7cbf1a259152-1~exp1~20230710162048.105)", isOptimized: false, runtimeVersion: 0, emissionKind: LineTablesOnly, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "/home/munak98/Documents/TCC-PES/test/input/test_inst.c", directory: "/home/munak98/Documents/TCC-PES", checksumkind: CSK_MD5, checksum: "855e9a39d89164001846c4527d1be6a1")
!2 = !{i32 7, !"Dwarf Version", i32 5}
!3 = !{i32 2, !"Debug Info Version", i32 3}
!4 = !{i32 1, !"wchar_size", i32 2}
!5 = !{i32 7, !"frame-pointer", i32 2}
!6 = !{!"Ubuntu clang version 16.0.6 (++20230710042027+7cbf1a259152-1~exp1~20230710162048.105)"}
!7 = distinct !DISubprogram(name: "BubbleSort", scope: !8, file: !8, line: 9, type: !9, scopeLine: 9, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !10)
!8 = !DIFile(filename: "test/input/test_inst.c", directory: "/home/munak98/Documents/TCC-PES", checksumkind: CSK_MD5, checksum: "855e9a39d89164001846c4527d1be6a1")
!9 = !DISubroutineType(types: !10)
!10 = !{}
!11 = !DILocation(line: 10, column: 6, scope: !7)
!12 = !DILocation(line: 13, column: 9, scope: !7)
!13 = !DILocation(line: 13, column: 7, scope: !7)
!14 = !DILocation(line: 13, column: 14, scope: !7)
!15 = !DILocation(line: 13, column: 16, scope: !7)
!16 = !DILocation(line: 13, column: 2, scope: !7)
!17 = !DILocation(line: 14, column: 10, scope: !7)
!18 = !DILocation(line: 15, column: 14, scope: !7)
!19 = !DILocation(line: 15, column: 8, scope: !7)
!20 = !DILocation(line: 15, column: 19, scope: !7)
!21 = !DILocation(line: 15, column: 25, scope: !7)
!22 = !DILocation(line: 15, column: 3, scope: !7)
!23 = !DILocation(line: 16, column: 8, scope: !7)
!24 = !DILocation(line: 16, column: 28, scope: !7)
!25 = !DILocation(line: 16, column: 26, scope: !7)
!26 = !DILocation(line: 16, column: 30, scope: !7)
!27 = !DILocation(line: 16, column: 14, scope: !7)
!28 = !DILocation(line: 17, column: 5, scope: !7)
!29 = !DILocation(line: 18, column: 8, scope: !7)
!30 = !DILocation(line: 18, column: 14, scope: !7)
!31 = !DILocation(line: 18, column: 23, scope: !7)
!32 = !DILocation(line: 18, column: 29, scope: !7)
!33 = !DILocation(line: 18, column: 35, scope: !7)
!34 = !DILocation(line: 18, column: 21, scope: !7)
!35 = !DILocation(line: 19, column: 12, scope: !7)
!36 = !DILocation(line: 19, column: 18, scope: !7)
!37 = !DILocation(line: 19, column: 10, scope: !7)
!38 = !DILocation(line: 20, column: 20, scope: !7)
!39 = !DILocation(line: 20, column: 26, scope: !7)
!40 = !DILocation(line: 20, column: 32, scope: !7)
!41 = !DILocation(line: 20, column: 5, scope: !7)
!42 = !DILocation(line: 20, column: 11, scope: !7)
!43 = !DILocation(line: 20, column: 18, scope: !7)
!44 = !DILocation(line: 21, column: 24, scope: !7)
!45 = !DILocation(line: 21, column: 5, scope: !7)
!46 = !DILocation(line: 21, column: 11, scope: !7)
!47 = !DILocation(line: 21, column: 17, scope: !7)
!48 = !DILocation(line: 21, column: 22, scope: !7)
!49 = !DILocation(line: 22, column: 12, scope: !7)
!50 = !DILocation(line: 23, column: 4, scope: !7)
!51 = !DILocation(line: 24, column: 3, scope: !7)
!52 = !DILocation(line: 15, column: 42, scope: !7)
!53 = distinct !{!53, !22, !51, !54}
!54 = !{!"llvm.loop.mustprogress"}
!55 = !DILocation(line: 25, column: 7, scope: !7)
!56 = !DILocation(line: 26, column: 4, scope: !7)
!57 = !DILocation(line: 27, column: 2, scope: !7)
!58 = !DILocation(line: 13, column: 29, scope: !7)
!59 = distinct !{!59, !16, !57, !54}
!60 = !DILocation(line: 28, column: 1, scope: !7)
!61 = distinct !DISubprogram(name: "main", scope: !8, file: !8, line: 30, type: !9, scopeLine: 30, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !10)
!62 = !DILocation(line: 31, column: 10, scope: !61)
!63 = !DILocation(line: 31, column: 6, scope: !61)
!64 = !DILocation(line: 31, column: 17, scope: !61)
!65 = !DILocation(line: 31, column: 19, scope: !61)
!66 = !DILocation(line: 31, column: 2, scope: !61)
!67 = !DILocation(line: 32, column: 3, scope: !61)
!68 = !DILocation(line: 33, column: 22, scope: !61)
!69 = !DILocation(line: 33, column: 16, scope: !61)
!70 = !DILocation(line: 33, column: 3, scope: !61)
!71 = !DILocation(line: 34, column: 2, scope: !61)
!72 = !DILocation(line: 31, column: 32, scope: !61)
!73 = distinct !{!73, !66, !71, !54}
!74 = !DILocation(line: 35, column: 2, scope: !61)
!75 = !DILocation(line: 36, column: 2, scope: !61)
