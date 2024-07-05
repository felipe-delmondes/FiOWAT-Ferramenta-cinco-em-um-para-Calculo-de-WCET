; ModuleID = '/home/munak98/Documents/TCC-PES/bin/libs/avr-simul/tick-counter.c'
source_filename = "/home/munak98/Documents/TCC-PES/bin/libs/avr-simul/tick-counter.c"
target datalayout = "e-P1-p:16:8-i8:8-i16:8-i32:8-i64:8-f32:8-f64:8-n8-a:8"
target triple = "avr-atmel-none"

@counter_overflow = dso_local global i16 0, align 1
@tempVar = dso_local global i16 0, align 1
@.str = private unnamed_addr constant [4 x i8] c"%u\0A\00", align 1
@endTime = dso_local global i16 0, align 1
@executionTime = dso_local global i32 0, align 1
@llvm.compiler.used = appending global [1 x ptr] [ptr addrspacecast (ptr addrspace(1) @__vector_13 to ptr)], section "llvm.metadata"

; Function Attrs: noinline nounwind optnone
define dso_local void @InitTickCounter() addrspace(1) #0 {
  store volatile i8 0, ptr inttoptr (i16 128 to ptr), align 1
  store volatile i8 1, ptr inttoptr (i16 129 to ptr), align 1
  ret void
}

; Function Attrs: noinline nounwind optnone
define dso_local void @InitTickCounter_Overflow() addrspace(1) #0 {
  store volatile i8 0, ptr inttoptr (i16 128 to ptr), align 1
  store volatile i8 1, ptr inttoptr (i16 129 to ptr), align 1
  %1 = load volatile i8, ptr inttoptr (i16 111 to ptr), align 1
  %2 = zext i8 %1 to i16
  %3 = or i16 %2, 1
  %4 = trunc i16 %3 to i8
  store volatile i8 %4, ptr inttoptr (i16 111 to ptr), align 1
  store i16 0, ptr @counter_overflow, align 1
  call addrspace(0) void asm sideeffect "sei", "~{memory}"() #3, !srcloc !3
  ret void
}

; Function Attrs: noinline nounwind optnone
define dso_local void @CaptureTickCounter() addrspace(1) #0 {
  %1 = load volatile i16, ptr inttoptr (i16 132 to ptr), align 1
  store i16 %1, ptr @tempVar, align 1
  ret void
}

; Function Attrs: noinline nounwind optnone
define dso_local void @ResetTickCounter() addrspace(1) #0 {
  store volatile i16 0, ptr inttoptr (i16 132 to ptr), align 1
  ret void
}

; Function Attrs: noinline nounwind optnone
define dso_local void @PrintTickCounter() addrspace(1) #0 {
  %1 = load i16, ptr @tempVar, align 1
  %2 = call addrspace(1) i16 (ptr, ...) @printf(ptr noundef @.str, i16 noundef %1)
  ret void
}

declare dso_local i16 @printf(ptr noundef, ...) addrspace(1) #1

; Function Attrs: noinline nounwind optnone
define dso_local void @StopTickCounter() addrspace(1) #0 {
  call addrspace(0) void asm sideeffect "cli", "~{memory}"() #3, !srcloc !4
  %1 = load volatile i16, ptr inttoptr (i16 132 to ptr), align 1
  store i16 %1, ptr @endTime, align 1
  ret void
}

; Function Attrs: noinline nounwind optnone
define dso_local i32 @GetTick_Overflow() addrspace(1) #0 {
  %1 = load i16, ptr @counter_overflow, align 1
  %2 = zext i16 %1 to i32
  %3 = mul nsw i32 %2, 65535
  %4 = load i16, ptr @endTime, align 1
  %5 = zext i16 %4 to i32
  %6 = add nsw i32 %3, %5
  store i32 %6, ptr @executionTime, align 1
  call addrspace(0) void asm sideeffect "sei", "~{memory}"() #3, !srcloc !5
  %7 = load i32, ptr @executionTime, align 1
  ret i32 %7
}

; Function Attrs: noinline nounwind optnone
define dso_local void @__vector_13() addrspace(1) #2 {
  %1 = load i16, ptr @counter_overflow, align 1
  %2 = add i16 %1, 1
  store i16 %2, ptr @counter_overflow, align 1
  call addrspace(1) void @ResetTickCounter()
  ret void
}

attributes #0 = { noinline nounwind optnone "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="atmega328" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="atmega328" }
attributes #2 = { noinline nounwind optnone "frame-pointer"="all" "no-trapping-math"="true" "signal" "stack-protector-buffer-size"="8" "target-cpu"="atmega328" }
attributes #3 = { nounwind }

!llvm.module.flags = !{!0, !1}
!llvm.ident = !{!2}

!0 = !{i32 1, !"wchar_size", i32 2}
!1 = !{i32 7, !"frame-pointer", i32 2}
!2 = !{!"Ubuntu clang version 16.0.6 (++20230710042027+7cbf1a259152-1~exp1~20230710162048.105)"}
!3 = !{i64 2147680861}
!4 = !{i64 2147681069}
!5 = !{i64 2147681194}
