; ModuleID = '/home/munak98/Documents/TCC-PES/bin/libs/avr-board/io-ports.c'
source_filename = "/home/munak98/Documents/TCC-PES/bin/libs/avr-board/io-ports.c"
target datalayout = "e-P1-p:16:8-i8:8-i16:8-i32:8-i64:8-f32:8-f64:8-n8-a:8"
target triple = "avr-atmel-none"

%struct.__file = type { ptr, i8, i8, i16, i16, ptr addrspace(1), ptr addrspace(1), ptr }

@uart_getchar.b = internal global [64 x i8] zeroinitializer, align 1
@uart_getchar.rxp = internal global ptr null, align 1
@mystdout = dso_local global %struct.__file zeroinitializer, align 1
@__iob = external dso_local global [0 x ptr], align 1
@mystdin = dso_local global %struct.__file zeroinitializer, align 1

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
  br i1 %17, label %11, label %18, !llvm.loop !3

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
  br label %12, !llvm.loop !5

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

attributes #0 = { noinline nounwind optnone "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="atmega328" }

!llvm.module.flags = !{!0, !1}
!llvm.ident = !{!2}

!0 = !{i32 1, !"wchar_size", i32 2}
!1 = !{i32 7, !"frame-pointer", i32 2}
!2 = !{!"Ubuntu clang version 16.0.6 (++20230710042027+7cbf1a259152-1~exp1~20230710162048.105)"}
!3 = distinct !{!3, !4}
!4 = !{!"llvm.loop.mustprogress"}
!5 = distinct !{!5, !4}
