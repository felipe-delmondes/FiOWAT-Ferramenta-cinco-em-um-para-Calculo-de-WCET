; ModuleID = 'C:\Users\Lucas\source\repos\VS Code\TCC-PES\test\input\first.c'
source_filename = "C:\\Users\\Lucas\\source\\repos\\VS Code\\TCC-PES\\test\\input\\first.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.29.30151"

$sprintf = comdat any

$vsprintf = comdat any

$_snprintf = comdat any

$_vsnprintf = comdat any

$printf = comdat any

$scanf = comdat any

$_vsprintf_l = comdat any

$_vsnprintf_l = comdat any

$__local_stdio_printf_options = comdat any

$_vfprintf_l = comdat any

$_vfscanf_l = comdat any

$__local_stdio_scanf_options = comdat any

$"??_C@_0BI@IKGCHOED@Digite?5um?5frase?5curta?3?5?$AA@" = comdat any

$"??_C@_02DKCKIIND@?$CFs?$AA@" = comdat any

$"??_C@_0BA@EAECEJBF@Programa?3?5?$CFs?6?6?6?$AA@" = comdat any

$"??_C@_0N@HLBFEOC@Fatorial?3?5?$CFd?$AA@" = comdat any

@"??_C@_0BI@IKGCHOED@Digite?5um?5frase?5curta?3?5?$AA@" = linkonce_odr dso_local unnamed_addr constant [24 x i8] c"Digite um frase curta: \00", comdat, align 1
@"??_C@_02DKCKIIND@?$CFs?$AA@" = linkonce_odr dso_local unnamed_addr constant [3 x i8] c"%s\00", comdat, align 1
@"??_C@_0BA@EAECEJBF@Programa?3?5?$CFs?6?6?6?$AA@" = linkonce_odr dso_local unnamed_addr constant [16 x i8] c"Programa: %s\0A\0A\0A\00", comdat, align 1
@"??_C@_0N@HLBFEOC@Fatorial?3?5?$CFd?$AA@" = linkonce_odr dso_local unnamed_addr constant [13 x i8] c"Fatorial: %d\00", comdat, align 1
@__local_stdio_printf_options._OptionsStorage = internal global i64 0, align 8
@__local_stdio_scanf_options._OptionsStorage = internal global i64 0, align 8

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @sprintf(ptr noundef %0, ptr noundef %1, ...) #0 comdat !dbg !8 {
  %3 = alloca ptr, align 8
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca ptr, align 8
  store ptr %1, ptr %3, align 8
  store ptr %0, ptr %4, align 8
  call void @llvm.va_start(ptr %6), !dbg !20
  %7 = load ptr, ptr %6, align 8, !dbg !21
  %8 = load ptr, ptr %3, align 8, !dbg !21
  %9 = load ptr, ptr %4, align 8, !dbg !21
  %10 = call i32 @_vsprintf_l(ptr noundef %9, ptr noundef %8, ptr noundef null, ptr noundef %7), !dbg !21
  store i32 %10, ptr %5, align 4, !dbg !21
  call void @llvm.va_end(ptr %6), !dbg !22
  %11 = load i32, ptr %5, align 4, !dbg !23
  ret i32 %11, !dbg !23
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @vsprintf(ptr noundef %0, ptr noundef %1, ptr noundef %2) #0 comdat !dbg !24 {
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  store ptr %2, ptr %4, align 8
  store ptr %1, ptr %5, align 8
  store ptr %0, ptr %6, align 8
  %7 = load ptr, ptr %4, align 8, !dbg !29
  %8 = load ptr, ptr %5, align 8, !dbg !29
  %9 = load ptr, ptr %6, align 8, !dbg !29
  %10 = call i32 @_vsnprintf_l(ptr noundef %9, i64 noundef -1, ptr noundef %8, ptr noundef null, ptr noundef %7), !dbg !29
  ret i32 %10, !dbg !29
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_snprintf(ptr noundef %0, i64 noundef %1, ptr noundef %2, ...) #0 comdat !dbg !30 {
  %4 = alloca ptr, align 8
  %5 = alloca i64, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  %8 = alloca ptr, align 8
  store ptr %2, ptr %4, align 8
  store i64 %1, ptr %5, align 8
  store ptr %0, ptr %6, align 8
  call void @llvm.va_start(ptr %8), !dbg !37
  %9 = load ptr, ptr %8, align 8, !dbg !38
  %10 = load ptr, ptr %4, align 8, !dbg !38
  %11 = load i64, ptr %5, align 8, !dbg !38
  %12 = load ptr, ptr %6, align 8, !dbg !38
  %13 = call i32 @_vsnprintf(ptr noundef %12, i64 noundef %11, ptr noundef %10, ptr noundef %9), !dbg !38
  store i32 %13, ptr %7, align 4, !dbg !38
  call void @llvm.va_end(ptr %8), !dbg !39
  %14 = load i32, ptr %7, align 4, !dbg !40
  ret i32 %14, !dbg !40
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_vsnprintf(ptr noundef %0, i64 noundef %1, ptr noundef %2, ptr noundef %3) #0 comdat !dbg !41 {
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i64, align 8
  %8 = alloca ptr, align 8
  store ptr %3, ptr %5, align 8
  store ptr %2, ptr %6, align 8
  store i64 %1, ptr %7, align 8
  store ptr %0, ptr %8, align 8
  %9 = load ptr, ptr %5, align 8, !dbg !44
  %10 = load ptr, ptr %6, align 8, !dbg !44
  %11 = load i64, ptr %7, align 8, !dbg !44
  %12 = load ptr, ptr %8, align 8, !dbg !44
  %13 = call i32 @_vsnprintf_l(ptr noundef %12, i64 noundef %11, ptr noundef %10, ptr noundef null, ptr noundef %9), !dbg !44
  ret i32 %13, !dbg !44
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @calculadora() #0 !dbg !45 {
  %1 = alloca [10 x i8], align 1
  %2 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0BI@IKGCHOED@Digite?5um?5frase?5curta?3?5?$AA@"), !dbg !49
  %3 = getelementptr inbounds [10 x i8], ptr %1, i64 0, i64 0, !dbg !50
  %4 = call i32 (ptr, ...) @scanf(ptr noundef @"??_C@_02DKCKIIND@?$CFs?$AA@", ptr noundef %3), !dbg !50
  %5 = getelementptr inbounds [10 x i8], ptr %1, i64 0, i64 0, !dbg !51
  %6 = load i8, ptr %5, align 1, !dbg !51
  %7 = sext i8 %6 to i32, !dbg !51
  %8 = sdiv i32 %7, 20, !dbg !51
  ret i32 %8, !dbg !51
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @printf(ptr noundef %0, ...) #0 comdat !dbg !52 {
  %2 = alloca ptr, align 8
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  call void @llvm.va_start(ptr %4), !dbg !55
  %5 = load ptr, ptr %4, align 8, !dbg !56
  %6 = load ptr, ptr %2, align 8, !dbg !56
  %7 = call ptr @__acrt_iob_func(i32 noundef 1), !dbg !56
  %8 = call i32 @_vfprintf_l(ptr noundef %7, ptr noundef %6, ptr noundef null, ptr noundef %5), !dbg !56
  store i32 %8, ptr %3, align 4, !dbg !56
  call void @llvm.va_end(ptr %4), !dbg !57
  %9 = load i32, ptr %3, align 4, !dbg !58
  ret i32 %9, !dbg !58
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @scanf(ptr noundef %0, ...) #0 comdat !dbg !59 {
  %2 = alloca ptr, align 8
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  call void @llvm.va_start(ptr %4), !dbg !60
  %5 = load ptr, ptr %4, align 8, !dbg !61
  %6 = load ptr, ptr %2, align 8, !dbg !61
  %7 = call ptr @__acrt_iob_func(i32 noundef 0), !dbg !61
  %8 = call i32 @_vfscanf_l(ptr noundef %7, ptr noundef %6, ptr noundef null, ptr noundef %5), !dbg !61
  store i32 %8, ptr %3, align 4, !dbg !61
  call void @llvm.va_end(ptr %4), !dbg !62
  %9 = load i32, ptr %3, align 4, !dbg !63
  ret i32 %9, !dbg !63
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @fatorial(i32 noundef %0) #0 !dbg !64 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, ptr %3, align 4
  %4 = load i32, ptr %3, align 4, !dbg !67
  %5 = icmp sle i32 %4, 1, !dbg !67
  br i1 %5, label %6, label %7, !dbg !67

6:                                                ; preds = %1
  store i32 1, ptr %2, align 4, !dbg !68
  br label %13, !dbg !68

7:                                                ; preds = %1
  %8 = load i32, ptr %3, align 4, !dbg !69
  %9 = load i32, ptr %3, align 4, !dbg !69
  %10 = sub nsw i32 %9, 1, !dbg !69
  %11 = call i32 @fatorial(i32 noundef %10), !dbg !69
  %12 = mul nsw i32 %8, %11, !dbg !69
  store i32 %12, ptr %2, align 4, !dbg !69
  br label %13, !dbg !69

13:                                               ; preds = %7, %6
  %14 = load i32, ptr %2, align 4, !dbg !70
  ret i32 %14, !dbg !70
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @soma_prefixa(ptr noundef %0, ptr noundef %1, i32 noundef %2) #0 !dbg !71 {
  %4 = alloca i32, align 4
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  store i32 %2, ptr %4, align 4
  store ptr %1, ptr %5, align 8
  store ptr %0, ptr %6, align 8
  %10 = load i32, ptr %4, align 4, !dbg !76
  %11 = icmp sgt i32 %10, 0, !dbg !76
  br i1 %11, label %12, label %46, !dbg !76

12:                                               ; preds = %3
  store i32 0, ptr %7, align 4, !dbg !77
  br label %13, !dbg !78

13:                                               ; preds = %41, %12
  store i32 0, ptr %8, align 4, !dbg !79
  store i32 0, ptr %9, align 4, !dbg !80
  %14 = load i32, ptr %9, align 4, !dbg !81
  %15 = load i32, ptr %7, align 4, !dbg !81
  %16 = icmp slt i32 %14, %15, !dbg !81
  br i1 %16, label %17, label %38, !dbg !81

17:                                               ; preds = %13
  br label %18, !dbg !82

18:                                               ; preds = %28, %17
  %19 = load ptr, ptr %6, align 8, !dbg !83
  %20 = load i32, ptr %9, align 4, !dbg !83
  %21 = sext i32 %20 to i64, !dbg !83
  %22 = getelementptr inbounds i32, ptr %19, i64 %21, !dbg !83
  %23 = load i32, ptr %22, align 4, !dbg !83
  %24 = load i32, ptr %8, align 4, !dbg !83
  %25 = add nsw i32 %24, %23, !dbg !83
  store i32 %25, ptr %8, align 4, !dbg !83
  %26 = load i32, ptr %9, align 4, !dbg !84
  %27 = add nsw i32 %26, 1, !dbg !84
  store i32 %27, ptr %9, align 4, !dbg !84
  br label %28, !dbg !85

28:                                               ; preds = %18
  %29 = load i32, ptr %9, align 4, !dbg !85
  %30 = load i32, ptr %7, align 4, !dbg !85
  %31 = icmp slt i32 %29, %30, !dbg !85
  br i1 %31, label %18, label %32, !dbg !85, !llvm.loop !86

32:                                               ; preds = %28
  %33 = load i32, ptr %8, align 4, !dbg !88
  %34 = load ptr, ptr %5, align 8, !dbg !88
  %35 = load i32, ptr %7, align 4, !dbg !88
  %36 = sext i32 %35 to i64, !dbg !88
  %37 = getelementptr inbounds i32, ptr %34, i64 %36, !dbg !88
  store i32 %33, ptr %37, align 4, !dbg !88
  br label %38, !dbg !89

38:                                               ; preds = %32, %13
  %39 = load i32, ptr %7, align 4, !dbg !90
  %40 = add nsw i32 %39, 1, !dbg !90
  store i32 %40, ptr %7, align 4, !dbg !90
  br label %41, !dbg !91

41:                                               ; preds = %38
  %42 = load i32, ptr %7, align 4, !dbg !91
  %43 = load i32, ptr %4, align 4, !dbg !91
  %44 = icmp slt i32 %42, %43, !dbg !91
  br i1 %44, label %13, label %45, !dbg !91, !llvm.loop !92

45:                                               ; preds = %41
  br label %46, !dbg !93

46:                                               ; preds = %45, %3
  ret void, !dbg !94
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main(i32 noundef %0, ptr noundef %1) #0 !dbg !95 {
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca [5 x i32], align 16
  %8 = alloca [5 x i32], align 16
  %9 = alloca i32, align 4
  store i32 0, ptr %3, align 4
  store ptr %1, ptr %4, align 8
  store i32 %0, ptr %5, align 4
  %10 = load ptr, ptr %4, align 8, !dbg !99
  %11 = getelementptr inbounds ptr, ptr %10, i64 0, !dbg !99
  %12 = load ptr, ptr %11, align 8, !dbg !99
  %13 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0BA@EAECEJBF@Programa?3?5?$CFs?6?6?6?$AA@", ptr noundef %12), !dbg !99
  %14 = call i64 @time(ptr noundef null), !dbg !100
  %15 = trunc i64 %14 to i32, !dbg !100
  call void @srand(i32 noundef %15), !dbg !100
  store i32 0, ptr %6, align 4, !dbg !101
  br label %16, !dbg !101

16:                                               ; preds = %30, %2
  %17 = load i32, ptr %6, align 4, !dbg !101
  %18 = icmp slt i32 %17, 5, !dbg !101
  br i1 %18, label %19, label %33, !dbg !101

19:                                               ; preds = %16
  %20 = call i32 @rand(), !dbg !102
  %21 = srem i32 %20, 10, !dbg !102
  %22 = load i32, ptr %6, align 4, !dbg !102
  %23 = sext i32 %22 to i64, !dbg !102
  %24 = getelementptr inbounds [5 x i32], ptr %7, i64 0, i64 %23, !dbg !102
  store i32 %21, ptr %24, align 4, !dbg !102
  %25 = call i32 @rand(), !dbg !103
  %26 = srem i32 %25, 7, !dbg !103
  %27 = load i32, ptr %6, align 4, !dbg !103
  %28 = sext i32 %27 to i64, !dbg !103
  %29 = getelementptr inbounds [5 x i32], ptr %8, i64 0, i64 %28, !dbg !103
  store i32 %26, ptr %29, align 4, !dbg !103
  br label %30, !dbg !104

30:                                               ; preds = %19
  %31 = load i32, ptr %6, align 4, !dbg !101
  %32 = add nsw i32 %31, 1, !dbg !101
  store i32 %32, ptr %6, align 4, !dbg !101
  br label %16, !dbg !101, !llvm.loop !105

33:                                               ; preds = %16
  store i32 2, ptr %9, align 4, !dbg !106
  %34 = load i32, ptr %9, align 4, !dbg !107
  %35 = getelementptr inbounds [5 x i32], ptr %8, i64 0, i64 0, !dbg !107
  %36 = getelementptr inbounds [5 x i32], ptr %7, i64 0, i64 0, !dbg !107
  call void @soma_prefixa(ptr noundef %36, ptr noundef %35, i32 noundef %34), !dbg !107
  %37 = call i32 @calculadora(), !dbg !108
  store i32 %37, ptr %9, align 4, !dbg !108
  %38 = load i32, ptr %9, align 4, !dbg !109
  %39 = icmp sgt i32 %38, 0, !dbg !109
  br i1 %39, label %40, label %43, !dbg !109

40:                                               ; preds = %33
  %41 = load i32, ptr %9, align 4, !dbg !110
  %42 = call i32 @fatorial(i32 noundef %41), !dbg !110
  store i32 %42, ptr %9, align 4, !dbg !110
  br label %43, !dbg !111

43:                                               ; preds = %40, %33
  %44 = load i32, ptr %9, align 4, !dbg !112
  %45 = call i32 (ptr, ...) @printf(ptr noundef @"??_C@_0N@HLBFEOC@Fatorial?3?5?$CFd?$AA@", i32 noundef %44), !dbg !112
  ret i32 0, !dbg !113
}

declare dso_local void @srand(i32 noundef) #1

; Function Attrs: noinline nounwind optnone uwtable
define internal i64 @time(ptr noundef %0) #0 !dbg !114 {
  %2 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %3 = load ptr, ptr %2, align 8, !dbg !124
  %4 = call i64 @_time64(ptr noundef %3), !dbg !124
  ret i64 %4, !dbg !124
}

declare dso_local i32 @rand() #1

; Function Attrs: nocallback nofree nosync nounwind willreturn
declare void @llvm.va_start(ptr) #2

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_vsprintf_l(ptr noundef %0, ptr noundef %1, ptr noundef %2, ptr noundef %3) #0 comdat !dbg !125 {
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  %8 = alloca ptr, align 8
  store ptr %3, ptr %5, align 8
  store ptr %2, ptr %6, align 8
  store ptr %1, ptr %7, align 8
  store ptr %0, ptr %8, align 8
  %9 = load ptr, ptr %5, align 8, !dbg !133
  %10 = load ptr, ptr %6, align 8, !dbg !133
  %11 = load ptr, ptr %7, align 8, !dbg !133
  %12 = load ptr, ptr %8, align 8, !dbg !133
  %13 = call i32 @_vsnprintf_l(ptr noundef %12, i64 noundef -1, ptr noundef %11, ptr noundef %10, ptr noundef %9), !dbg !133
  ret i32 %13, !dbg !133
}

; Function Attrs: nocallback nofree nosync nounwind willreturn
declare void @llvm.va_end(ptr) #2

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_vsnprintf_l(ptr noundef %0, i64 noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4) #0 comdat !dbg !134 {
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  %8 = alloca ptr, align 8
  %9 = alloca i64, align 8
  %10 = alloca ptr, align 8
  %11 = alloca i32, align 4
  store ptr %4, ptr %6, align 8
  store ptr %3, ptr %7, align 8
  store ptr %2, ptr %8, align 8
  store i64 %1, ptr %9, align 8
  store ptr %0, ptr %10, align 8
  %12 = load ptr, ptr %6, align 8, !dbg !137
  %13 = load ptr, ptr %7, align 8, !dbg !137
  %14 = load ptr, ptr %8, align 8, !dbg !137
  %15 = load i64, ptr %9, align 8, !dbg !137
  %16 = load ptr, ptr %10, align 8, !dbg !137
  %17 = call ptr @__local_stdio_printf_options(), !dbg !137
  %18 = load i64, ptr %17, align 8, !dbg !137
  %19 = or i64 %18, 1, !dbg !137
  %20 = call i32 @__stdio_common_vsprintf(i64 noundef %19, ptr noundef %16, i64 noundef %15, ptr noundef %14, ptr noundef %13, ptr noundef %12), !dbg !137
  store i32 %20, ptr %11, align 4, !dbg !137
  %21 = load i32, ptr %11, align 4, !dbg !138
  %22 = icmp slt i32 %21, 0, !dbg !138
  br i1 %22, label %23, label %24, !dbg !138

23:                                               ; preds = %5
  br label %26, !dbg !138

24:                                               ; preds = %5
  %25 = load i32, ptr %11, align 4, !dbg !138
  br label %26, !dbg !138

26:                                               ; preds = %24, %23
  %27 = phi i32 [ -1, %23 ], [ %25, %24 ], !dbg !138
  ret i32 %27, !dbg !138
}

declare dso_local i32 @__stdio_common_vsprintf(i64 noundef, ptr noundef, i64 noundef, ptr noundef, ptr noundef, ptr noundef) #1

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local ptr @__local_stdio_printf_options() #0 comdat !dbg !139 {
  ret ptr @__local_stdio_printf_options._OptionsStorage, !dbg !144
}

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_vfprintf_l(ptr noundef %0, ptr noundef %1, ptr noundef %2, ptr noundef %3) #0 comdat !dbg !145 {
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  %8 = alloca ptr, align 8
  store ptr %3, ptr %5, align 8
  store ptr %2, ptr %6, align 8
  store ptr %1, ptr %7, align 8
  store ptr %0, ptr %8, align 8
  %9 = load ptr, ptr %5, align 8, !dbg !153
  %10 = load ptr, ptr %6, align 8, !dbg !153
  %11 = load ptr, ptr %7, align 8, !dbg !153
  %12 = load ptr, ptr %8, align 8, !dbg !153
  %13 = call ptr @__local_stdio_printf_options(), !dbg !153
  %14 = load i64, ptr %13, align 8, !dbg !153
  %15 = call i32 @__stdio_common_vfprintf(i64 noundef %14, ptr noundef %12, ptr noundef %11, ptr noundef %10, ptr noundef %9), !dbg !153
  ret i32 %15, !dbg !153
}

declare dso_local ptr @__acrt_iob_func(i32 noundef) #1

declare dso_local i32 @__stdio_common_vfprintf(i64 noundef, ptr noundef, ptr noundef, ptr noundef, ptr noundef) #1

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_vfscanf_l(ptr noundef %0, ptr noundef %1, ptr noundef %2, ptr noundef %3) #0 comdat !dbg !154 {
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  %8 = alloca ptr, align 8
  store ptr %3, ptr %5, align 8
  store ptr %2, ptr %6, align 8
  store ptr %1, ptr %7, align 8
  store ptr %0, ptr %8, align 8
  %9 = load ptr, ptr %5, align 8, !dbg !155
  %10 = load ptr, ptr %6, align 8, !dbg !155
  %11 = load ptr, ptr %7, align 8, !dbg !155
  %12 = load ptr, ptr %8, align 8, !dbg !155
  %13 = call ptr @__local_stdio_scanf_options(), !dbg !155
  %14 = load i64, ptr %13, align 8, !dbg !155
  %15 = call i32 @__stdio_common_vfscanf(i64 noundef %14, ptr noundef %12, ptr noundef %11, ptr noundef %10, ptr noundef %9), !dbg !155
  ret i32 %15, !dbg !155
}

declare dso_local i32 @__stdio_common_vfscanf(i64 noundef, ptr noundef, ptr noundef, ptr noundef, ptr noundef) #1

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local ptr @__local_stdio_scanf_options() #0 comdat !dbg !156 {
  ret ptr @__local_stdio_scanf_options._OptionsStorage, !dbg !157
}

declare dso_local i64 @_time64(ptr noundef) #1

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nocallback nofree nosync nounwind willreturn }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 16.0.0", isOptimized: false, runtimeVersion: 0, emissionKind: LineTablesOnly, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "C:\\Users\\Lucas\\source\\repos\\VS Code\\TCC-PES\\test\\input\\first.c", directory: "c:\\Users\\Lucas\\source\\repos\\VS Code\\TCC-PES", checksumkind: CSK_MD5, checksum: "0f5da55deaae4144daea65e434214000")
!2 = !{i32 2, !"CodeView", i32 1}
!3 = !{i32 2, !"Debug Info Version", i32 3}
!4 = !{i32 1, !"wchar_size", i32 2}
!5 = !{i32 8, !"PIC Level", i32 2}
!6 = !{i32 7, !"uwtable", i32 2}
!7 = !{!"clang version 16.0.0"}
!8 = distinct !DISubprogram(name: "sprintf", scope: !9, file: !9, line: 1764, type: !10, scopeLine: 1771, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!9 = !DIFile(filename: "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt\\stdio.h", directory: "", checksumkind: CSK_MD5, checksum: "c1a1fbc43e7d45f0ea4ae539ddcffb19")
!10 = !DISubroutineType(types: !11)
!11 = !{!12, !13, !16, null}
!12 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!13 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !14)
!14 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !15, size: 64)
!15 = !DIBasicType(name: "char", size: 8, encoding: DW_ATE_signed_char)
!16 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !17)
!17 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !18, size: 64)
!18 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !15)
!19 = !{}
!20 = !DILocation(line: 1774, scope: !8)
!21 = !DILocation(line: 1776, scope: !8)
!22 = !DILocation(line: 1778, scope: !8)
!23 = !DILocation(line: 1779, scope: !8)
!24 = distinct !DISubprogram(name: "vsprintf", scope: !9, file: !9, line: 1465, type: !25, scopeLine: 1473, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!25 = !DISubroutineType(types: !26)
!26 = !{!12, !13, !16, !27}
!27 = !DIDerivedType(tag: DW_TAG_typedef, name: "va_list", file: !28, line: 72, baseType: !14)
!28 = !DIFile(filename: "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.29.30133\\include\\vadefs.h", directory: "", checksumkind: CSK_MD5, checksum: "a4b8f96637d0704c82f39ecb6bde2ab4")
!29 = !DILocation(line: 1474, scope: !24)
!30 = distinct !DISubprogram(name: "_snprintf", scope: !9, file: !9, line: 1939, type: !31, scopeLine: 1947, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!31 = !DISubroutineType(types: !32)
!32 = !{!12, !13, !33, !16, null}
!33 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !34)
!34 = !DIDerivedType(tag: DW_TAG_typedef, name: "size_t", file: !35, line: 193, baseType: !36)
!35 = !DIFile(filename: "C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\Tools\\MSVC\\14.29.30133\\include\\vcruntime.h", directory: "", checksumkind: CSK_MD5, checksum: "1147c94afb6f25c377433eef20bc3e8f")
!36 = !DIBasicType(name: "unsigned long long", size: 64, encoding: DW_ATE_unsigned)
!37 = !DILocation(line: 1950, scope: !30)
!38 = !DILocation(line: 1951, scope: !30)
!39 = !DILocation(line: 1952, scope: !30)
!40 = !DILocation(line: 1953, scope: !30)
!41 = distinct !DISubprogram(name: "_vsnprintf", scope: !9, file: !9, line: 1402, type: !42, scopeLine: 1411, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!42 = !DISubroutineType(types: !43)
!43 = !{!12, !13, !33, !16, !27}
!44 = !DILocation(line: 1412, scope: !41)
!45 = distinct !DISubprogram(name: "calculadora", scope: !46, file: !46, line: 6, type: !47, scopeLine: 6, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!46 = !DIFile(filename: "C:\\Users\\Lucas\\source\\repos\\VS Code\\TCC-PES\\test\\input/first.h", directory: "", checksumkind: CSK_MD5, checksum: "e09c7be67896cac626147fed89ef2cb0")
!47 = !DISubroutineType(types: !48)
!48 = !{!12}
!49 = !DILocation(line: 8, scope: !45)
!50 = !DILocation(line: 9, scope: !45)
!51 = !DILocation(line: 10, scope: !45)
!52 = distinct !DISubprogram(name: "printf", scope: !9, file: !9, line: 950, type: !53, scopeLine: 956, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!53 = !DISubroutineType(types: !54)
!54 = !{!12, !16, null}
!55 = !DILocation(line: 959, scope: !52)
!56 = !DILocation(line: 960, scope: !52)
!57 = !DILocation(line: 961, scope: !52)
!58 = !DILocation(line: 962, scope: !52)
!59 = distinct !DISubprogram(name: "scanf", scope: !9, file: !9, line: 1276, type: !53, scopeLine: 1282, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!60 = !DILocation(line: 1285, scope: !59)
!61 = !DILocation(line: 1286, scope: !59)
!62 = !DILocation(line: 1287, scope: !59)
!63 = !DILocation(line: 1288, scope: !59)
!64 = distinct !DISubprogram(name: "fatorial", scope: !46, file: !46, line: 14, type: !65, scopeLine: 14, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!65 = !DISubroutineType(types: !66)
!66 = !{!12, !12}
!67 = !DILocation(line: 15, scope: !64)
!68 = !DILocation(line: 16, scope: !64)
!69 = !DILocation(line: 19, scope: !64)
!70 = !DILocation(line: 21, scope: !64)
!71 = distinct !DISubprogram(name: "soma_prefixa", scope: !72, file: !72, line: 7, type: !73, scopeLine: 7, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!72 = !DIFile(filename: "C:\\Users\\Lucas\\source\\repos\\VS Code\\TCC-PES\\test\\input\\first.c", directory: "", checksumkind: CSK_MD5, checksum: "0f5da55deaae4144daea65e434214000")
!73 = !DISubroutineType(types: !74)
!74 = !{null, !75, !75, !12}
!75 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !12, size: 64)
!76 = !DILocation(line: 8, scope: !71)
!77 = !DILocation(line: 9, scope: !71)
!78 = !DILocation(line: 10, scope: !71)
!79 = !DILocation(line: 11, scope: !71)
!80 = !DILocation(line: 12, scope: !71)
!81 = !DILocation(line: 13, scope: !71)
!82 = !DILocation(line: 14, scope: !71)
!83 = !DILocation(line: 15, scope: !71)
!84 = !DILocation(line: 16, scope: !71)
!85 = !DILocation(line: 17, scope: !71)
!86 = distinct !{!86, !82, !85, !87}
!87 = !{!"llvm.loop.mustprogress"}
!88 = !DILocation(line: 18, scope: !71)
!89 = !DILocation(line: 19, scope: !71)
!90 = !DILocation(line: 20, scope: !71)
!91 = !DILocation(line: 21, scope: !71)
!92 = distinct !{!92, !78, !91, !87}
!93 = !DILocation(line: 22, scope: !71)
!94 = !DILocation(line: 23, scope: !71)
!95 = distinct !DISubprogram(name: "main", scope: !72, file: !72, line: 28, type: !96, scopeLine: 28, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!96 = !DISubroutineType(types: !97)
!97 = !{!12, !12, !98}
!98 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !14, size: 64)
!99 = !DILocation(line: 31, scope: !95)
!100 = !DILocation(line: 32, scope: !95)
!101 = !DILocation(line: 33, scope: !95)
!102 = !DILocation(line: 34, scope: !95)
!103 = !DILocation(line: 35, scope: !95)
!104 = !DILocation(line: 36, scope: !95)
!105 = distinct !{!105, !101, !104, !87}
!106 = !DILocation(line: 39, scope: !95)
!107 = !DILocation(line: 40, scope: !95)
!108 = !DILocation(line: 41, scope: !95)
!109 = !DILocation(line: 42, scope: !95)
!110 = !DILocation(line: 43, scope: !95)
!111 = !DILocation(line: 44, scope: !95)
!112 = !DILocation(line: 46, scope: !95)
!113 = !DILocation(line: 47, scope: !95)
!114 = distinct !DISubprogram(name: "time", scope: !115, file: !115, line: 518, type: !116, scopeLine: 521, flags: DIFlagPrototyped, spFlags: DISPFlagLocalToUnit | DISPFlagDefinition, unit: !0, retainedNodes: !19)
!115 = !DIFile(filename: "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt\\time.h", directory: "", checksumkind: CSK_MD5, checksum: "452c47c1a6e57bc48e99148b619c7eab")
!116 = !DISubroutineType(types: !117)
!117 = !{!118, !122}
!118 = !DIDerivedType(tag: DW_TAG_typedef, name: "time_t", file: !119, line: 631, baseType: !120)
!119 = !DIFile(filename: "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt\\corecrt.h", directory: "", checksumkind: CSK_MD5, checksum: "db0cd8b4d76ec84d3625032eaca2a3ca")
!120 = !DIDerivedType(tag: DW_TAG_typedef, name: "__time64_t", file: !119, line: 594, baseType: !121)
!121 = !DIBasicType(name: "long long", size: 64, encoding: DW_ATE_signed)
!122 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !123)
!123 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !118, size: 64)
!124 = !DILocation(line: 522, scope: !114)
!125 = distinct !DISubprogram(name: "_vsprintf_l", scope: !9, file: !9, line: 1449, type: !126, scopeLine: 1458, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!126 = !DISubroutineType(types: !127)
!127 = !{!12, !13, !16, !128, !27}
!128 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !129)
!129 = !DIDerivedType(tag: DW_TAG_typedef, name: "_locale_t", file: !119, line: 609, baseType: !130)
!130 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !131, size: 64)
!131 = !DIDerivedType(tag: DW_TAG_typedef, name: "__crt_locale_pointers", file: !119, line: 607, baseType: !132)
!132 = !DICompositeType(tag: DW_TAG_structure_type, name: "__crt_locale_pointers", file: !119, line: 603, size: 128, flags: DIFlagFwdDecl)
!133 = !DILocation(line: 1459, scope: !125)
!134 = distinct !DISubprogram(name: "_vsnprintf_l", scope: !9, file: !9, line: 1381, type: !135, scopeLine: 1391, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!135 = !DISubroutineType(types: !136)
!136 = !{!12, !13, !33, !16, !128, !27}
!137 = !DILocation(line: 1392, scope: !134)
!138 = !DILocation(line: 1396, scope: !134)
!139 = distinct !DISubprogram(name: "__local_stdio_printf_options", scope: !140, file: !140, line: 89, type: !141, scopeLine: 90, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!140 = !DIFile(filename: "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt\\corecrt_stdio_config.h", directory: "", checksumkind: CSK_MD5, checksum: "dacf907bda504afb0b64f53a242bdae6")
!141 = !DISubroutineType(types: !142)
!142 = !{!143}
!143 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !36, size: 64)
!144 = !DILocation(line: 92, scope: !139)
!145 = distinct !DISubprogram(name: "_vfprintf_l", scope: !9, file: !9, line: 635, type: !146, scopeLine: 644, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!146 = !DISubroutineType(types: !147)
!147 = !{!12, !148, !16, !128, !27}
!148 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !149)
!149 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !150, size: 64)
!150 = !DIDerivedType(tag: DW_TAG_typedef, name: "FILE", file: !151, line: 31, baseType: !152)
!151 = !DIFile(filename: "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt\\corecrt_wstdio.h", directory: "", checksumkind: CSK_MD5, checksum: "bf50373b435d0afd0235dd3e05c4a277")
!152 = !DICompositeType(tag: DW_TAG_structure_type, name: "_iobuf", file: !151, line: 28, size: 64, flags: DIFlagFwdDecl)
!153 = !DILocation(line: 645, scope: !145)
!154 = distinct !DISubprogram(name: "_vfscanf_l", scope: !9, file: !9, line: 1055, type: !146, scopeLine: 1064, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!155 = !DILocation(line: 1065, scope: !154)
!156 = distinct !DISubprogram(name: "__local_stdio_scanf_options", scope: !140, file: !140, line: 99, type: !141, scopeLine: 100, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!157 = !DILocation(line: 102, scope: !156)
