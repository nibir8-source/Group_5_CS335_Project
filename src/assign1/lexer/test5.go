package main
import ("fmt")

func main() {
	//Different type of integer assignment
	a:=42
	b:=4_2
	c:=0600
	d:=0_600
	e:=0o600
	f:=0O600       
	g:=0xBadFace
	h:=0xBad_Face
	i:=0x_67_7a_2f_cc_40_c6
	j:=170141183460469
	k:=170_141183_46046

	//floating point assignment
	a:= 0.
	b:=72.40
	c:=072.40      
	d:=2.71828
	e:=1.e+0
	f:=6.67428e-11
	g:=1E6
	h:=.25
	i:=.12345E+5
	j:=1_5.         
	k:=0.15e+0_2    

	l:=0x1p-2       
	m:=0x2.p10      
	n:=0x1.Fp+0     
	o:=0X.8p-0      
	p:=0X_1FFFP-16  
	q:=0x15e-2      
	
	//Imaginary number assignment
	a:=0i
	b:=0123i         
	c:=0o123i        
	d:=0xabci        
	e:=0.i
	f:=2.71828i
	g:=1.e+0i
	h:=6.67428e-11i
	i:=1E6i
	j:=.25i
	k:=.12345E+5i
	l:=0x1p-2i       
	//string representation

	s1:=`abc`                
	s2:=`\n
	\n`        //giving error         
	s4:="\n"
	s5:="\""                
	s6:="Hello, world!\n"
	s7:="日本語"
	s8:="\u65e5本\U00008a9e"
	s9:="\xff\u00FF"
	s10:="\uD800"           
	s11:="\U00110000"        




}