pragma circom 2.0.0;

/*This circuit template checks that c is the multiplication of a and b.*/  

template checker () {  

   // Declaration of signals.  
   signal input a;  
   signal input b;  
   signal input c;
   signal input d;  

   // Constraints.  
   c === a * b;  
   d === a + b;
}


component main = checker();