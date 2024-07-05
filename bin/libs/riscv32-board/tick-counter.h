#pragma once

#include <inttypes.h>
#include <stdio.h>


extern void PrintTickCounter(void);
extern void CaptureTickCounter(void);
extern void ResetTickCounter(void);
extern void InitTickCounter(void);
extern void InitTickCounter_Overflow(void);
extern void StopTickCounter(void);
extern void StartTickCounter(void);
extern uint32_t GetTick_Overflow(void);
