Cin=1e-9;
CF=1e-12;
CL=1e-12;
Vdd=0.8;
fs=1e6;
a=16;
CRES=1e-10;

beta=CF/(Cin+CF);
CLtot=CL+CF*Cin/(CF+Cin);

Gavg=a*CRES*fs*log(1+Gm0/(a*CRES*fs));
Ec=exp(-beta*Gavg/2/fs/CLtot);

Gain=CF/Cin+Ec*(1+CF/Cin);
