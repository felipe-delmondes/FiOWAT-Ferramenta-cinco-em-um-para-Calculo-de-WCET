; ModuleID = 'semloop.c'
source_filename = "semloop.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-windows-msvc19.29.30151"

$sprintf = comdat any

$vsprintf = comdat any

$_snprintf = comdat any

$_vsnprintf = comdat any

$_vsprintf_l = comdat any

$_vsnprintf_l = comdat any

$__local_stdio_printf_options = comdat any

@__local_stdio_printf_options._OptionsStorage = internal global i64 0, align 8

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
define dso_local i32 @main(i32 noundef %0, ptr noundef %1) #0 !dbg !45 {
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  store i32 0, ptr %3, align 4
  store ptr %1, ptr %4, align 8
  store i32 %0, ptr %5, align 4
  store i32 5, ptr %6, align 4, !dbg !49
  %7 = load i32, ptr %6, align 4, !dbg !50
  %8 = mul nsw i32 %7, 3, !dbg !50
  store i32 %8, ptr %6, align 4, !dbg !50
  ret i32 0, !dbg !51
}

; Function Attrs: nocallback nofree nosync nounwind willreturn
declare void @llvm.va_start(ptr) #1

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_vsprintf_l(ptr noundef %0, ptr noundef %1, ptr noundef %2, ptr noundef %3) #0 comdat !dbg !52 {
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  %8 = alloca ptr, align 8
  store ptr %3, ptr %5, align 8
  store ptr %2, ptr %6, align 8
  store ptr %1, ptr %7, align 8
  store ptr %0, ptr %8, align 8
  %9 = load ptr, ptr %5, align 8, !dbg !61
  %10 = load ptr, ptr %6, align 8, !dbg !61
  %11 = load ptr, ptr %7, align 8, !dbg !61
  %12 = load ptr, ptr %8, align 8, !dbg !61
  %13 = call i32 @_vsnprintf_l(ptr noundef %12, i64 noundef -1, ptr noundef %11, ptr noundef %10, ptr noundef %9), !dbg !61
  ret i32 %13, !dbg !61
}

; Function Attrs: nocallback nofree nosync nounwind willreturn
declare void @llvm.va_end(ptr) #1

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local i32 @_vsnprintf_l(ptr noundef %0, i64 noundef %1, ptr noundef %2, ptr noundef %3, ptr noundef %4) #0 comdat !dbg !62 {
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
  %12 = load ptr, ptr %6, align 8, !dbg !65
  %13 = load ptr, ptr %7, align 8, !dbg !65
  %14 = load ptr, ptr %8, align 8, !dbg !65
  %15 = load i64, ptr %9, align 8, !dbg !65
  %16 = load ptr, ptr %10, align 8, !dbg !65
  %17 = call ptr @__local_stdio_printf_options(), !dbg !65
  %18 = load i64, ptr %17, align 8, !dbg !65
  %19 = or i64 %18, 1, !dbg !65
  %20 = call i32 @__stdio_common_vsprintf(i64 noundef %19, ptr noundef %16, i64 noundef %15, ptr noundef %14, ptr noundef %13, ptr noundef %12), !dbg !65
  store i32 %20, ptr %11, align 4, !dbg !65
  %21 = load i32, ptr %11, align 4, !dbg !66
  %22 = icmp slt i32 %21, 0, !dbg !66
  br i1 %22, label %23, label %24, !dbg !66

23:                                               ; preds = %5
  br label %26, !dbg !66

24:                                               ; preds = %5
  %25 = load i32, ptr %11, align 4, !dbg !66
  br label %26, !dbg !66

26:                                               ; preds = %24, %23
  %27 = phi i32 [ -1, %23 ], [ %25, %24 ], !dbg !66
  ret i32 %27, !dbg !66
}

declare dso_local i32 @__stdio_common_vsprintf(i64 noundef, ptr noundef, i64 noundef, ptr noundef, ptr noundef, ptr noundef) #2

; Function Attrs: noinline nounwind optnone uwtable
define linkonce_odr dso_local ptr @__local_stdio_printf_options() #0 comdat !dbg !67 {
  ret ptr @__local_stdio_printf_options._OptionsStorage, !dbg !72
}

attributes #0 = { noinline nounwind optnone uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind willreturn }
attributes #2 = { "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6}
!llvm.ident = !{!7}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 16.0.0", isOptimized: false, runtimeVersion: 0, emissionKind: LineTablesOnly, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "semloop.c", directory: "C:\\Users\\Peter", checksumkind: CSK_MD5, checksum: "a9b8798997832a9f7b5dcb836ae3c366")
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
!45 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 5, type: !46, scopeLine: 5, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!46 = !DISubroutineType(types: !47)
!47 = !{!12, !12, !48}
!48 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !14, size: 64)
!49 = !DILocation(line: 6, scope: !45)
!50 = !DILocation(line: 7, scope: !45)
!51 = !DILocation(line: 8, scope: !45)
!52 = distinct !DISubprogram(name: "_vsprintf_l", scope: !9, file: !9, line: 1449, type: !53, scopeLine: 1458, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!53 = !DISubroutineType(types: !54)
!54 = !{!12, !13, !16, !55, !27}
!55 = !DIDerivedType(tag: DW_TAG_const_type, baseType: !56)
!56 = !DIDerivedType(tag: DW_TAG_typedef, name: "_locale_t", file: !57, line: 609, baseType: !58)
!57 = !DIFile(filename: "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt\\corecrt.h", directory: "", checksumkind: CSK_MD5, checksum: "db0cd8b4d76ec84d3625032eaca2a3ca")
!58 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !59, size: 64)
!59 = !DIDerivedType(tag: DW_TAG_typedef, name: "__crt_locale_pointers", file: !57, line: 607, baseType: !60)
!60 = !DICompositeType(tag: DW_TAG_structure_type, name: "__crt_locale_pointers", file: !57, line: 603, size: 128, flags: DIFlagFwdDecl)
!61 = !DILocation(line: 1459, scope: !52)
!62 = distinct !DISubprogram(name: "_vsnprintf_l", scope: !9, file: !9, line: 1381, type: !63, scopeLine: 1391, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!63 = !DISubroutineType(types: !64)
!64 = !{!12, !13, !33, !16, !55, !27}
!65 = !DILocation(line: 1392, scope: !62)
!66 = !DILocation(line: 1396, scope: !62)
!67 = distinct !DISubprogram(name: "__local_stdio_printf_options", scope: !68, file: !68, line: 89, type: !69, scopeLine: 90, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !19)
!68 = !DIFile(filename: "C:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.19041.0\\ucrt\\corecrt_stdio_config.h", directory: "", checksumkind: CSK_MD5, checksum: "dacf907bda504afb0b64f53a242bdae6")
!69 = !DISubroutineType(types: !70)
!70 = !{!71}
!71 = !DIDerivedType(tag: DW_TAG_pointer_type, baseType: !36, size: 64)
!72 = !DILocation(line: 92, scope: !67)
