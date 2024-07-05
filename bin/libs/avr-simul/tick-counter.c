#include "tick-counter.h"
#include <inttypes.h>

uint16_t tempVar;
uint16_t counter_overflow;
uint16_t endTime;
uint32_t executionTime;


extern void InitTickCounter(void){
    TCCR1A = 0;            // Configuração dos modos de operação do Timer/Counter1 (nenhuma configuração necessária)
    TCCR1B = (1 << CS10);  // Configuração do prescaler (divisão de clock = 1)
    // TIMSK1 |= (1 << TOIE1); // Libera interrupções por overflow
}

extern void InitTickCounter_Overflow(void){
    TCCR1A = 0;            // Configuração dos modos de operação do Timer/Counter1 (nenhuma configuração necessária)
    TCCR1B = (1 << CS10);  // Configuração do prescaler (divisão de clock = 1)
    TIMSK1 |= (1 << TOIE1); // Libera interrupções por overflow
    counter_overflow = 0;
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


extern void StopTickCounter(void){
    cli();
    endTime = TCNT1;
}

extern uint32_t GetTick_Overflow(void){
    executionTime = counter_overflow*(65535) + endTime;
    sei();
    return executionTime;
}

ISR (TIMER1_OVF_vect){
    counter_overflow++;
    ResetTickCounter();
}