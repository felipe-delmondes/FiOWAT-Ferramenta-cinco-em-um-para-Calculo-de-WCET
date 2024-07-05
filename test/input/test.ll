; ModuleID = 'llvm-link'
source_filename = "llvm-link"
target datalayout = "e-P1-p:16:8-i8:8-i16:8-i32:8-i64:8-f32:8-f64:8-n8-a:8"
target triple = "avr-atmel-none"

%struct.__file = type { ptr, i8, i8, i16, i16, ptr addrspace(1), ptr addrspace(1), ptr }

@.str = private unnamed_addr constant [7 x i8] c"Input\0A\00", align 1
@.str.1 = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@Array = dso_local global [10 x i16] zeroinitializer, align 1
@uart_getchar.b = internal global [64 x i8] zeroinitializer, align 1
@uart_getchar.rxp = internal global ptr null, align 1
@mystdout = dso_local global %struct.__file zeroinitializer, align 1
@__iob = external dso_local global [0 x ptr], align 1
@mystdin = dso_local global %struct.__file zeroinitializer, align 1
@llvm.compiler.used = appending global [1 x ptr] [ptr addrspacecast (ptr addrspace(1) @__vector_13 to ptr)], section "llvm.metadata"
@counter_overflow = dso_local global i8 0, align 1
@tempVar = dso_local global i16 0, align 1
@.str.2 = private unnamed_addr constant [4 x i8] c"%u\0A\00", align 1
@startTime = dso_local global i16 0, align 1
@endTime = dso_local global i16 0, align 1
@execution_time = dso_local global i32 0, align 1

; Function Attrs: noinline nounwind optnone
define dso_local void @BubbleSort(ptr noundef %0) addrspace(1) #0 !dbg !9 {
  %2 = alloca ptr, align 1
  %3 = alloca i16, align 1
  %4 = alloca i16, align 1
  %5 = alloca i16, align 1
  %6 = alloca i16, align 1
  store ptr %0, ptr %2, align 1
  store i16 0, ptr %3, align 1, !dbg !13
  store i16 0, ptr %6, align 1, !dbg !14
  br label %7, !dbg !15

7:                                                ; preds = %59, %1
  %8 = load i16, ptr %6, align 1, !dbg !16
  %9 = icmp slt i16 %8, 10, !dbg !17
  br i1 %9, label %10, label %62, !dbg !18

10:                                               ; preds = %7
  store i16 1, ptr %3, align 1, !dbg !19
  store i16 0, ptr %5, align 1, !dbg !20
  br label %11, !dbg !21

11:                                               ; preds = %51, %10
  %12 = load i16, ptr %5, align 1, !dbg !22
  %13 = icmp slt i16 %12, 10, !dbg !23
  br i1 %13, label %14, label %54, !dbg !24

14:                                               ; preds = %11
  %15 = load i16, ptr %5, align 1, !dbg !25
  %16 = load i16, ptr %6, align 1, !dbg !26
  %17 = sub nsw i16 10, %16, !dbg !27
  %18 = sub nsw i16 %17, 1, !dbg !28
  %19 = icmp sge i16 %15, %18, !dbg !29
  br i1 %19, label %20, label %21, !dbg !25

20:                                               ; preds = %14
  br label %54, !dbg !30

21:                                               ; preds = %14
  %22 = load ptr, ptr %2, align 1, !dbg !31
  %23 = load i16, ptr %5, align 1, !dbg !32
  %24 = getelementptr inbounds i16, ptr %22, i16 %23, !dbg !31
  %25 = load i16, ptr %24, align 1, !dbg !31
  %26 = load ptr, ptr %2, align 1, !dbg !33
  %27 = load i16, ptr %5, align 1, !dbg !34
  %28 = add nsw i16 %27, 1, !dbg !35
  %29 = getelementptr inbounds i16, ptr %26, i16 %28, !dbg !33
  %30 = load i16, ptr %29, align 1, !dbg !33
  %31 = icmp sgt i16 %25, %30, !dbg !36
  br i1 %31, label %32, label %50, !dbg !31

32:                                               ; preds = %21
  %33 = load ptr, ptr %2, align 1, !dbg !37
  %34 = load i16, ptr %5, align 1, !dbg !38
  %35 = getelementptr inbounds i16, ptr %33, i16 %34, !dbg !37
  %36 = load i16, ptr %35, align 1, !dbg !37
  store i16 %36, ptr %4, align 1, !dbg !39
  %37 = load ptr, ptr %2, align 1, !dbg !40
  %38 = load i16, ptr %5, align 1, !dbg !41
  %39 = add nsw i16 %38, 1, !dbg !42
  %40 = getelementptr inbounds i16, ptr %37, i16 %39, !dbg !40
  %41 = load i16, ptr %40, align 1, !dbg !40
  %42 = load ptr, ptr %2, align 1, !dbg !43
  %43 = load i16, ptr %5, align 1, !dbg !44
  %44 = getelementptr inbounds i16, ptr %42, i16 %43, !dbg !43
  store i16 %41, ptr %44, align 1, !dbg !45
  %45 = load i16, ptr %4, align 1, !dbg !46
  %46 = load ptr, ptr %2, align 1, !dbg !47
  %47 = load i16, ptr %5, align 1, !dbg !48
  %48 = add nsw i16 %47, 1, !dbg !49
  %49 = getelementptr inbounds i16, ptr %46, i16 %48, !dbg !47
  store i16 %45, ptr %49, align 1, !dbg !50
  store i16 0, ptr %3, align 1, !dbg !51
  br label %50, !dbg !52

50:                                               ; preds = %32, %21
  br label %51, !dbg !53

51:                                               ; preds = %50
  %52 = load i16, ptr %5, align 1, !dbg !54
  %53 = add nsw i16 %52, 1, !dbg !54
  store i16 %53, ptr %5, align 1, !dbg !54
  br label %11, !dbg !24, !llvm.loop !55

54:                                               ; preds = %20, %11
  %55 = load i16, ptr %3, align 1, !dbg !57
  %56 = icmp ne i16 %55, 0, !dbg !57
  br i1 %56, label %57, label %58, !dbg !57

57:                                               ; preds = %54
  br label %62, !dbg !58

58:                                               ; preds = %54
  br label %59, !dbg !59

59:                                               ; preds = %58
  %60 = load i16, ptr %6, align 1, !dbg !60
  %61 = add nsw i16 %60, 1, !dbg !60
  store i16 %61, ptr %6, align 1, !dbg !60
  br label %7, !dbg !18, !llvm.loop !61

62:                                               ; preds = %57, %7
  ret void, !dbg !62
}

; Function Attrs: noinline nounwind optnone
define dso_local i16 @main() addrspace(1) #0 !dbg !63 {
  %1 = alloca i16, align 1
  %2 = alloca i16, align 1
  store i16 0, ptr %1, align 1
  store i16 0, ptr %2, align 1, !dbg !64
  br label %3, !dbg !65

3:                                                ; preds = %11, %0
  %4 = load i16, ptr %2, align 1, !dbg !66
  %5 = icmp slt i16 %4, 10, !dbg !67
  br i1 %5, label %6, label %14, !dbg !68

6:                                                ; preds = %3
  %7 = call addrspace(1) i16 (ptr, ...) @printf(ptr noundef @.str), !dbg !69
  %8 = load i16, ptr %2, align 1, !dbg !70
  %9 = getelementptr inbounds [10 x i16], ptr @Array, i16 0, i16 %8, !dbg !71
  %10 = call addrspace(1) i16 (ptr, ...) @scanf(ptr noundef @.str.1, ptr noundef %9), !dbg !72
  br label %11, !dbg !73

11:                                               ; preds = %6
  %12 = load i16, ptr %2, align 1, !dbg !74
  %13 = add nsw i16 %12, 1, !dbg !74
  store i16 %13, ptr %2, align 1, !dbg !74
  br label %3, !dbg !68, !llvm.loop !75

14:                                               ; preds = %3
  call addrspace(1) void @BubbleSort(ptr noundef @Array), !dbg !76
  ret i16 0, !dbg !77
}

declare dso_local i16 @printf(ptr noundef, ...) addrspace(1) #1

declare dso_local i16 @scanf(ptr noundef, ...) addrspace(1) #1

; Function Attrs: noinline nounwind optnone
define dso_local i16 @uart_getchar(ptr noundef %0) addrspace(1) #0 {
  %2 = alloca i16, align 1
  %3 = alloca ptr, align 1
  %4 = alloca i8, align 1
  %5 = alloca ptr, align 1
  %6 = alloca ptr, align 1
  store ptr %0, ptr %3, align 1
  %7 = load ptr, ptr @uart_getchar.rxp, align 1
  %8 = icmp eq ptr %7, null
  br i1 %8, label %9, label %74

9:                                                ; preds = %1
  store ptr @uart_getchar.b, ptr %5, align 1
  br label %10

10:                                               ; preds = %72, %71, %9
  br label %11

11:                                               ; preds = %12, %10
  br label %12

12:                                               ; preds = %11
  %13 = load volatile i8, ptr inttoptr (i16 192 to ptr), align 1
  %14 = zext i8 %13 to i16
  %15 = and i16 %14, 128
  %16 = icmp ne i16 %15, 0
  %17 = xor i1 %16, true
  br i1 %17, label %11, label %18, !llvm.loop !78

18:                                               ; preds = %12
  %19 = load volatile i8, ptr inttoptr (i16 192 to ptr), align 1
  %20 = zext i8 %19 to i16
  %21 = and i16 %20, 16
  %22 = icmp ne i16 %21, 0
  br i1 %22, label %23, label %24

23:                                               ; preds = %18
  store i16 -2, ptr %2, align 1
  br label %85

24:                                               ; preds = %18
  %25 = load volatile i8, ptr inttoptr (i16 192 to ptr), align 1
  %26 = zext i8 %25 to i16
  %27 = and i16 %26, 8
  %28 = icmp ne i16 %27, 0
  br i1 %28, label %29, label %30

29:                                               ; preds = %24
  store i16 -1, ptr %2, align 1
  br label %85

30:                                               ; preds = %24
  %31 = load volatile i8, ptr inttoptr (i16 198 to ptr), align 1
  store i8 %31, ptr %4, align 1
  %32 = load i8, ptr %4, align 1
  %33 = zext i8 %32 to i16
  %34 = icmp eq i16 %33, 13
  br i1 %34, label %35, label %36

35:                                               ; preds = %30
  store i8 10, ptr %4, align 1
  br label %36

36:                                               ; preds = %35, %30
  %37 = load i8, ptr %4, align 1
  %38 = zext i8 %37 to i16
  %39 = icmp eq i16 %38, 10
  br i1 %39, label %40, label %43

40:                                               ; preds = %36
  %41 = load i8, ptr %4, align 1
  %42 = load ptr, ptr %5, align 1
  store i8 %41, ptr %42, align 1
  store ptr @uart_getchar.b, ptr @uart_getchar.rxp, align 1
  br label %73

43:                                               ; preds = %36
  %44 = load i8, ptr %4, align 1
  %45 = zext i8 %44 to i16
  %46 = icmp eq i16 %45, 9
  br i1 %46, label %47, label %48

47:                                               ; preds = %43
  store i8 32, ptr %4, align 1
  br label %48

48:                                               ; preds = %47, %43
  br label %49

49:                                               ; preds = %48
  %50 = load i8, ptr %4, align 1
  %51 = zext i8 %50 to i16
  %52 = icmp sge i16 %51, 32
  br i1 %52, label %53, label %57

53:                                               ; preds = %49
  %54 = load i8, ptr %4, align 1
  %55 = zext i8 %54 to i16
  %56 = icmp sle i16 %55, 126
  br i1 %56, label %61, label %57

57:                                               ; preds = %53, %49
  %58 = load i8, ptr %4, align 1
  %59 = zext i8 %58 to i16
  %60 = icmp sge i16 %59, -96
  br i1 %60, label %61, label %72

61:                                               ; preds = %57, %53
  %62 = load ptr, ptr %5, align 1
  %63 = icmp eq ptr %62, getelementptr inbounds (i8, ptr @uart_getchar.b, i16 63)
  br i1 %63, label %64, label %67

64:                                               ; preds = %61
  %65 = load ptr, ptr %3, align 1
  %66 = call addrspace(1) i16 @uart_putchar(i8 noundef signext 7, ptr noundef %65)
  br label %71

67:                                               ; preds = %61
  %68 = load i8, ptr %4, align 1
  %69 = load ptr, ptr %5, align 1
  %70 = getelementptr inbounds i8, ptr %69, i32 1
  store ptr %70, ptr %5, align 1
  store i8 %68, ptr %69, align 1
  br label %71

71:                                               ; preds = %67, %64
  br label %10

72:                                               ; preds = %57
  br label %10

73:                                               ; preds = %40
  br label %74

74:                                               ; preds = %73, %1
  %75 = load ptr, ptr @uart_getchar.rxp, align 1
  %76 = getelementptr inbounds i8, ptr %75, i32 1
  store ptr %76, ptr @uart_getchar.rxp, align 1
  %77 = load i8, ptr %75, align 1
  store i8 %77, ptr %4, align 1
  %78 = load i8, ptr %4, align 1
  %79 = zext i8 %78 to i16
  %80 = icmp eq i16 %79, 10
  br i1 %80, label %81, label %82

81:                                               ; preds = %74
  store ptr null, ptr @uart_getchar.rxp, align 1
  br label %82

82:                                               ; preds = %81, %74
  %83 = load i8, ptr %4, align 1
  %84 = zext i8 %83 to i16
  store i16 %84, ptr %2, align 1
  br label %85

85:                                               ; preds = %82, %29, %23
  %86 = load i16, ptr %2, align 1
  ret i16 %86
}

; Function Attrs: noinline nounwind optnone
define dso_local i16 @uart_putchar(i8 noundef signext %0, ptr noundef %1) addrspace(1) #0 {
  %3 = alloca i8, align 1
  %4 = alloca ptr, align 1
  store i8 %0, ptr %3, align 1
  store ptr %1, ptr %4, align 1
  %5 = load i8, ptr %3, align 1
  %6 = sext i8 %5 to i16
  %7 = icmp eq i16 %6, 10
  br i1 %7, label %8, label %11

8:                                                ; preds = %2
  %9 = load ptr, ptr %4, align 1
  %10 = call addrspace(1) i16 @uart_putchar(i8 noundef signext 13, ptr noundef %9)
  br label %11

11:                                               ; preds = %8, %2
  br label %12

12:                                               ; preds = %17, %11
  %13 = load volatile i8, ptr inttoptr (i16 192 to ptr), align 1
  %14 = zext i8 %13 to i16
  %15 = and i16 %14, 32
  %16 = icmp eq i16 %15, 0
  br i1 %16, label %17, label %18

17:                                               ; preds = %12
  br label %12, !llvm.loop !79

18:                                               ; preds = %12
  %19 = load i8, ptr %3, align 1
  store volatile i8 %19, ptr inttoptr (i16 198 to ptr), align 1
  ret i16 0
}

; Function Attrs: noinline nounwind optnone
define dso_local void @InitIO() addrspace(1) #0 {
  store volatile i8 0, ptr inttoptr (i16 197 to ptr), align 1
  store volatile i8 104, ptr inttoptr (i16 196 to ptr), align 1
  store volatile i8 24, ptr inttoptr (i16 193 to ptr), align 1
  br label %1

1:                                                ; preds = %0
  store ptr addrspace(1) @uart_putchar, ptr getelementptr inbounds (%struct.__file, ptr @mystdout, i32 0, i32 5), align 1
  store ptr addrspace(1) null, ptr getelementptr inbounds (%struct.__file, ptr @mystdout, i32 0, i32 6), align 1
  store i8 2, ptr getelementptr inbounds (%struct.__file, ptr @mystdout, i32 0, i32 2), align 1
  store ptr null, ptr getelementptr inbounds (%struct.__file, ptr @mystdout, i32 0, i32 7), align 1
  br label %2

2:                                                ; preds = %1
  store ptr @mystdout, ptr getelementptr inbounds ([0 x ptr], ptr @__iob, i16 0, i16 1), align 1
  br label %3

3:                                                ; preds = %2
  store ptr addrspace(1) null, ptr getelementptr inbounds (%struct.__file, ptr @mystdin, i32 0, i32 5), align 1
  store ptr addrspace(1) @uart_getchar, ptr getelementptr inbounds (%struct.__file, ptr @mystdin, i32 0, i32 6), align 1
  store i8 1, ptr getelementptr inbounds (%struct.__file, ptr @mystdin, i32 0, i32 2), align 1
  store ptr null, ptr getelementptr inbounds (%struct.__file, ptr @mystdin, i32 0, i32 7), align 1
  br label %4

4:                                                ; preds = %3
  store ptr @mystdin, ptr @__iob, align 1
  ret void
}

; Function Attrs: noinline nounwind optnone
define dso_local void @__vector_13() addrspace(1) #2 !dbg !80 {
  %1 = load i8, ptr @counter_overflow, align 1, !dbg !82
  %2 = add i8 %1, 1, !dbg !82
  store i8 %2, ptr @counter_overflow, align 1, !dbg !82
  call addrspace(1) void @ResetTickCounter(), !dbg !83
  ret void, !dbg !84
}

; Function Attrs: noinline nounwind optnone
define dso_local void @ResetTickCounter() addrspace(1) #0 !dbg !85 {
  store volatile i16 0, ptr inttoptr (i16 132 to ptr), align 1, !dbg !86
  ret void, !dbg !87
}

; Function Attrs: noinline nounwind optnone
define dso_local void @InitTickCounter() addrspace(1) #0 !dbg !88 {
  store volatile i8 0, ptr inttoptr (i16 128 to ptr), align 1, !dbg !89
  store volatile i8 1, ptr inttoptr (i16 129 to ptr), align 1, !dbg !90
  ret void, !dbg !91
}

; Function Attrs: noinline nounwind optnone
define dso_local void @InitTickCounter_Overflow() addrspace(1) #0 !dbg !92 {
  store volatile i8 0, ptr inttoptr (i16 128 to ptr), align 1, !dbg !93
  store volatile i8 1, ptr inttoptr (i16 129 to ptr), align 1, !dbg !94
  %1 = load volatile i8, ptr inttoptr (i16 111 to ptr), align 1, !dbg !95
  %2 = zext i8 %1 to i16, !dbg !95
  %3 = or i16 %2, 1, !dbg !95
  %4 = trunc i16 %3 to i8, !dbg !95
  store volatile i8 %4, ptr inttoptr (i16 111 to ptr), align 1, !dbg !95
  call addrspace(0) void asm sideeffect "sei", "~{memory}"() #3, !dbg !96, !srcloc !97
  ret void, !dbg !98
}

; Function Attrs: noinline nounwind optnone
define dso_local void @CaptureTickCounter() addrspace(1) #0 !dbg !99 {
  %1 = load volatile i16, ptr inttoptr (i16 132 to ptr), align 1, !dbg !100
  store i16 %1, ptr @tempVar, align 1, !dbg !101
  ret void, !dbg !102
}

; Function Attrs: noinline nounwind optnone
define dso_local void @PrintTickCounter() addrspace(1) #0 !dbg !103 {
  %1 = load i16, ptr @tempVar, align 1, !dbg !104
  %2 = call addrspace(1) i16 (ptr, ...) @printf(ptr noundef @.str.2, i16 noundef %1), !dbg !105
  ret void, !dbg !106
}

; Function Attrs: noinline nounwind optnone
define dso_local void @StartTickCounter() addrspace(1) #0 !dbg !107 {
  %1 = load volatile i16, ptr inttoptr (i16 132 to ptr), align 1, !dbg !108
  store i16 %1, ptr @startTime, align 1, !dbg !109
  ret void, !dbg !110
}

; Function Attrs: noinline nounwind optnone
define dso_local void @StopTickCounter() addrspace(1) #0 !dbg !111 {
  %1 = load volatile i16, ptr inttoptr (i16 132 to ptr), align 1, !dbg !112
  store i16 %1, ptr @endTime, align 1, !dbg !113
  ret void, !dbg !114
}

; Function Attrs: noinline nounwind optnone
define dso_local i32 @GetTick_Overflow() addrspace(1) #0 !dbg !115 {
  %1 = load i8, ptr @counter_overflow, align 1, !dbg !116
  %2 = sext i8 %1 to i32, !dbg !116
  %3 = mul nsw i32 %2, 65535, !dbg !117
  %4 = load i16, ptr @endTime, align 1, !dbg !118
  %5 = sext i16 %4 to i32, !dbg !118
  %6 = add nsw i32 %3, %5, !dbg !119
  %7 = load i16, ptr @startTime, align 1, !dbg !120
  %8 = sext i16 %7 to i32, !dbg !120
  %9 = sub nsw i32 %6, %8, !dbg !121
  ret i32 %9, !dbg !122
}

attributes #0 = { noinline nounwind optnone "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="atmega328" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="atmega328" }
attributes #2 = { noinline nounwind optnone "frame-pointer"="all" "no-trapping-math"="true" "signal" "stack-protector-buffer-size"="8" "target-cpu"="atmega328" }
attributes #3 = { nounwind }

!llvm.dbg.cu = !{!0, !2}
!llvm.ident = !{!4, !4, !4}
!llvm.module.flags = !{!5, !6, !7, !8}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "Ubuntu clang version 16.0.6 (++20230710042027+7cbf1a259152-1~exp1~20230710162048.105)", isOptimized: false, runtimeVersion: 0, emissionKind: LineTablesOnly, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "/home/munak98/Documents/TCC-PES/test/input/test.c", directory: "/home/munak98/Documents/TCC-PES", checksumkind: CSK_MD5, checksum: "855e9a39d89164001846c4527d1be6a1")
!2 = distinct !DICompileUnit(language: DW_LANG_C11, file: !3, producer: "Ubuntu clang version 16.0.6 (++20230710042027+7cbf1a259152-1~exp1~20230710162048.105)", isOptimized: false, runtimeVersion: 0, emissionKind: LineTablesOnly, splitDebugInlining: false, nameTableKind: None)
!3 = !DIFile(filename: "bin/libs/avr-board/tick-counter.c", directory: "/home/munak98/Documents/TCC-PES", checksumkind: CSK_MD5, checksum: "30e019955cace7c5cc66909da446ecd5")
!4 = !{!"Ubuntu clang version 16.0.6 (++20230710042027+7cbf1a259152-1~exp1~20230710162048.105)"}
!5 = !{i32 7, !"Dwarf Version", i32 5}
!6 = !{i32 2, !"Debug Info Version", i32 3}
!7 = !{i32 1, !"wchar_size", i32 2}
!8 = !{i32 7, !"frame-pointer", i32 2}
!9 = distinct !DISubprogram(name: "BubbleSort", scope: !10, file: !10, line: 9, type: !11, scopeLine: 9, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !12)
!10 = !DIFile(filename: "test/input/test.c", directory: "/home/munak98/Documents/TCC-PES", checksumkind: CSK_MD5, checksum: "855e9a39d89164001846c4527d1be6a1")
!11 = !DISubroutineType(types: !12)
!12 = !{}
!13 = !DILocation(line: 10, column: 6, scope: !9)
!14 = !DILocation(line: 13, column: 9, scope: !9)
!15 = !DILocation(line: 13, column: 7, scope: !9)
!16 = !DILocation(line: 13, column: 14, scope: !9)
!17 = !DILocation(line: 13, column: 16, scope: !9)
!18 = !DILocation(line: 13, column: 2, scope: !9)
!19 = !DILocation(line: 14, column: 10, scope: !9)
!20 = !DILocation(line: 15, column: 14, scope: !9)
!21 = !DILocation(line: 15, column: 8, scope: !9)
!22 = !DILocation(line: 15, column: 19, scope: !9)
!23 = !DILocation(line: 15, column: 25, scope: !9)
!24 = !DILocation(line: 15, column: 3, scope: !9)
!25 = !DILocation(line: 16, column: 8, scope: !9)
!26 = !DILocation(line: 16, column: 28, scope: !9)
!27 = !DILocation(line: 16, column: 26, scope: !9)
!28 = !DILocation(line: 16, column: 30, scope: !9)
!29 = !DILocation(line: 16, column: 14, scope: !9)
!30 = !DILocation(line: 17, column: 5, scope: !9)
!31 = !DILocation(line: 18, column: 8, scope: !9)
!32 = !DILocation(line: 18, column: 14, scope: !9)
!33 = !DILocation(line: 18, column: 23, scope: !9)
!34 = !DILocation(line: 18, column: 29, scope: !9)
!35 = !DILocation(line: 18, column: 35, scope: !9)
!36 = !DILocation(line: 18, column: 21, scope: !9)
!37 = !DILocation(line: 19, column: 12, scope: !9)
!38 = !DILocation(line: 19, column: 18, scope: !9)
!39 = !DILocation(line: 19, column: 10, scope: !9)
!40 = !DILocation(line: 20, column: 20, scope: !9)
!41 = !DILocation(line: 20, column: 26, scope: !9)
!42 = !DILocation(line: 20, column: 32, scope: !9)
!43 = !DILocation(line: 20, column: 5, scope: !9)
!44 = !DILocation(line: 20, column: 11, scope: !9)
!45 = !DILocation(line: 20, column: 18, scope: !9)
!46 = !DILocation(line: 21, column: 24, scope: !9)
!47 = !DILocation(line: 21, column: 5, scope: !9)
!48 = !DILocation(line: 21, column: 11, scope: !9)
!49 = !DILocation(line: 21, column: 17, scope: !9)
!50 = !DILocation(line: 21, column: 22, scope: !9)
!51 = !DILocation(line: 22, column: 12, scope: !9)
!52 = !DILocation(line: 23, column: 4, scope: !9)
!53 = !DILocation(line: 24, column: 3, scope: !9)
!54 = !DILocation(line: 15, column: 42, scope: !9)
!55 = distinct !{!55, !24, !53, !56}
!56 = !{!"llvm.loop.mustprogress"}
!57 = !DILocation(line: 25, column: 7, scope: !9)
!58 = !DILocation(line: 26, column: 4, scope: !9)
!59 = !DILocation(line: 27, column: 2, scope: !9)
!60 = !DILocation(line: 13, column: 29, scope: !9)
!61 = distinct !{!61, !18, !59, !56}
!62 = !DILocation(line: 28, column: 1, scope: !9)
!63 = distinct !DISubprogram(name: "main", scope: !10, file: !10, line: 30, type: !11, scopeLine: 30, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !12)
!64 = !DILocation(line: 31, column: 10, scope: !63)
!65 = !DILocation(line: 31, column: 6, scope: !63)
!66 = !DILocation(line: 31, column: 17, scope: !63)
!67 = !DILocation(line: 31, column: 19, scope: !63)
!68 = !DILocation(line: 31, column: 2, scope: !63)
!69 = !DILocation(line: 32, column: 3, scope: !63)
!70 = !DILocation(line: 33, column: 22, scope: !63)
!71 = !DILocation(line: 33, column: 16, scope: !63)
!72 = !DILocation(line: 33, column: 3, scope: !63)
!73 = !DILocation(line: 34, column: 2, scope: !63)
!74 = !DILocation(line: 31, column: 32, scope: !63)
!75 = distinct !{!75, !68, !73, !56}
!76 = !DILocation(line: 35, column: 2, scope: !63)
!77 = !DILocation(line: 36, column: 2, scope: !63)
!78 = distinct !{!78, !56}
!79 = distinct !{!79, !56}
!80 = distinct !DISubprogram(name: "__vector_13", scope: !81, file: !81, line: 44, type: !11, scopeLine: 44, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !12)
!81 = !DIFile(filename: "./bin/libs/avr-board/tick-counter.c", directory: "/home/munak98/Documents/TCC-PES", checksumkind: CSK_MD5, checksum: "30e019955cace7c5cc66909da446ecd5")
!82 = !DILocation(line: 45, column: 21, scope: !80)
!83 = !DILocation(line: 46, column: 5, scope: !80)
!84 = !DILocation(line: 47, column: 1, scope: !80)
!85 = distinct !DISubprogram(name: "ResetTickCounter", scope: !81, file: !81, line: 25, type: !11, scopeLine: 25, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !12)
!86 = !DILocation(line: 26, column: 11, scope: !85)
!87 = !DILocation(line: 27, column: 1, scope: !85)
!88 = distinct !DISubprogram(name: "InitTickCounter", scope: !81, file: !81, line: 8, type: !11, scopeLine: 8, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !12)
!89 = !DILocation(line: 9, column: 12, scope: !88)
!90 = !DILocation(line: 10, column: 12, scope: !88)
!91 = !DILocation(line: 12, column: 1, scope: !88)
!92 = distinct !DISubprogram(name: "InitTickCounter_Overflow", scope: !81, file: !81, line: 14, type: !11, scopeLine: 14, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !12)
!93 = !DILocation(line: 15, column: 12, scope: !92)
!94 = !DILocation(line: 16, column: 12, scope: !92)
!95 = !DILocation(line: 17, column: 12, scope: !92)
!96 = !DILocation(line: 18, column: 5, scope: !92)
!97 = !{i64 2147680910}
!98 = !DILocation(line: 19, column: 1, scope: !92)
!99 = distinct !DISubprogram(name: "CaptureTickCounter", scope: !81, file: !81, line: 21, type: !11, scopeLine: 21, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !12)
!100 = !DILocation(line: 22, column: 15, scope: !99)
!101 = !DILocation(line: 22, column: 13, scope: !99)
!102 = !DILocation(line: 23, column: 1, scope: !99)
!103 = distinct !DISubprogram(name: "PrintTickCounter", scope: !81, file: !81, line: 29, type: !11, scopeLine: 29, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !12)
!104 = !DILocation(line: 30, column: 20, scope: !103)
!105 = !DILocation(line: 30, column: 5, scope: !103)
!106 = !DILocation(line: 31, column: 1, scope: !103)
!107 = distinct !DISubprogram(name: "StartTickCounter", scope: !81, file: !81, line: 33, type: !11, scopeLine: 33, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !12)
!108 = !DILocation(line: 34, column: 17, scope: !107)
!109 = !DILocation(line: 34, column: 15, scope: !107)
!110 = !DILocation(line: 35, column: 1, scope: !107)
!111 = distinct !DISubprogram(name: "StopTickCounter", scope: !81, file: !81, line: 36, type: !11, scopeLine: 36, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !12)
!112 = !DILocation(line: 37, column: 15, scope: !111)
!113 = !DILocation(line: 37, column: 13, scope: !111)
!114 = !DILocation(line: 38, column: 1, scope: !111)
!115 = distinct !DISubprogram(name: "GetTick_Overflow", scope: !81, file: !81, line: 40, type: !11, scopeLine: 40, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !2, retainedNodes: !12)
!116 = !DILocation(line: 41, column: 12, scope: !115)
!117 = !DILocation(line: 41, column: 28, scope: !115)
!118 = !DILocation(line: 41, column: 39, scope: !115)
!119 = !DILocation(line: 41, column: 37, scope: !115)
!120 = !DILocation(line: 41, column: 49, scope: !115)
!121 = !DILocation(line: 41, column: 47, scope: !115)
!122 = !DILocation(line: 41, column: 5, scope: !115)
