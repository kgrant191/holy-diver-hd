; Fixed bank $FD2A. Preserve X/Y and all RAM. Return negative to skip
; only sound $26 pulse-1 while active backing-track $1E occupies priority 3.

LDA $0130,Y
BMI done
PHA
TXA
PHA
LDA $E5
BNE normal
LDA $0133
BMI normal
TAX
LDA $0140,X
BEQ normal
LDA $01B8,X
CMP #$1E
BNE normal
LDA $0130,Y
TAX
LDA $01B8,X
CMP #$26
BNE normal
PLA
TAX
PLA
LDA #$FF
RTS
normal:
PLA
TAX
PLA
done:
RTS
