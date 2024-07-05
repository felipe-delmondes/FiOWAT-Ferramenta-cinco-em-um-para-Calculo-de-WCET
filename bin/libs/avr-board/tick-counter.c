#include "tick-counter.h"

uint16_t tempVar;
int8_t counter_overflow=0;
int16_t startTime, endTime;
int32_t execution_time;

extern void InitTickCounter(void){
    TCCR1A = 0;            // Configuração dos modos de operação do Timer/Counter1 (nenhuma configuração necessária)
    TCCR1B = (1 << CS10);  // Configuração do prescaler (divisão de clock = 1)
    // TIMSK1 |= (1 << TOIE1); // Libera interrupções por overflow
}

extern void InitTickCounter_Overflow(void){
    TCCR1A = 0;            // Configuração dos modos de operação do Timer/Counter1 (nenhuma configuração necessária)
    TCCR1B = (1 << CS10);  // Configuração do prescaler (divisão de clock = 1)
    TIMSK1 |= (1 << TOIE1); // Libera interrupções por overflow
    sei();
}

extern void CaptureTickCounter(void){
    tempVar = TCNT1;
}

extern void ResetTickCounter(void){
    TCNT1 = 0;
}

extern void PrintTickCounter(void){
    printf("%u\n", tempVar);
}

extern void StartTickCounter(void){
    startTime = TCNT1;
}
extern void StopTickCounter(void){
    endTime = TCNT1;
}

extern uint32_t GetTick_Overflow(void){
    return counter_overflow*(65535) + endTime - startTime;;
}

ISR (TIMER1_OVF_vect){
    counter_overflow++;
    ResetTickCounter();
}