#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a large HARD / rare-formalism task set (~86) with PYTHON-COMPUTED
ground truths. Emits tasks_hard.json = [[term,math,q,ans,tol],...]."""
import json, math, os

def totient(n):
    r=n;p=2;m=n
    while p*p<=m:
        if m%p==0:
            while m%p==0:m//=p
            r-=r//p
        p+=1
    if m>1:r-=r//m
    return r
def catalan(n): return math.comb(2*n,n)//(n+1)
def lev(a,b):
    d=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        prev=d[0];d[0]=i
        for j,cb in enumerate(b,1):
            prev,d[j]=d[j],min(d[j]+1,d[j-1]+1,prev+(ca!=cb))
    return d[-1]
def bent(p): return -(p*math.log2(p)+(1-p)*math.log2(1-p))
F,I=0.02,0.005

TASKS=[
 ("reduced_mass","mu = m1*m2/(m1+m2)","Reduced mass for m1=3, m2=6?",3*6/9,I),
 ("lorentz_factor","gamma = 1/sqrt(1-(v/c)^2)","Lorentz factor at v=0.6c?",1/math.sqrt(1-0.36),F),
 ("parallel_resistance","R = R1*R2/(R1+R2)","6 ohm and 3 ohm in parallel?",6*3/9,I),
 ("moment_inertia_sphere","I = (2/5) m r^2","Solid sphere inertia, m=5, r=2?",2/5*5*4,I),
 ("moment_inertia_rod","I = (1/12) m L^2","Thin rod inertia about center, m=12, L=1?",1.0,I),
 ("half_life_decay","N = N0 (1/2)^(t/T)","Remaining: N0=80, t=3, half-life 1?",80*0.5**3,I),
 ("heron_area","s=(a+b+c)/2; A=sqrt(s(s-a)(s-b)(s-c))","Heron area of sides 3,4,5?",6.0,I),
 ("law_of_cosines","c=sqrt(a^2+b^2-2ab cosC)","Third side a=3,b=4,C=60deg?",math.sqrt(9+16-12),F),
 ("eulers_totient","phi(n)","Euler totient phi(12)?",totient(12),I),
 ("catalan_number","C_n=(2n)!/((n+1)!n!)","3rd Catalan number?",catalan(3),I),
 ("harmonic_mean","HM=n/sum(1/x)","Harmonic mean of [1,2,4]?",3/(1+0.5+0.25),F),
 ("geometric_mean","GM=(prod)^(1/n)","Geometric mean of [1,3,9]?",(27)**(1/3),F),
 ("determinant_2x2","det=ad-bc","det [[2,3],[1,4]]?",5,I),
 ("point_line_distance","d=|ax0+by0+c|/sqrt(a^2+b^2)","Dist (0,0) to 3x+4y-10=0?",2.0,I),
 ("cagr","(end/begin)^(1/n)-1","CAGR 1000->1331 over 3y?",(1331/1000)**(1/3)-1,F),
 ("poisson_pmf","lambda^k e^-lambda/k!","Poisson lambda=2,k=1?",2*math.exp(-2),F),
 ("binomial_pmf","C(n,k)p^k(1-p)^(n-k)","Binomial k=2,n=4,p=0.5?",math.comb(4,2)*0.25*0.25,F),
 ("normal_pdf_peak","1/(sigma sqrt(2pi))","Normal pdf peak, sigma=1?",1/math.sqrt(2*math.pi),F),
 ("cosine_similarity","(a.b)/(|a||b|)","Cosine sim [1,0],[1,1]?",1/math.sqrt(2),F),
 ("sigmoid_derivative","s(1-s)","Sigmoid deriv at s=0.5?",0.25,I),
 ("sharpe_ratio","(Rp-Rf)/sigma","Sharpe Rp=.1,Rf=.02,sig=.16?",0.5,F),
 ("levenshtein_distance","min edits","Levenshtein kitten->sitting?",lev("kitten","sitting"),I),
 ("jaccard_index","|A&B|/|A|B||","Jaccard {1,2,3},{2,3,4}?",0.5,I),
 ("f1_score","2PR/(P+R)","F1 P=0.5,R=1?",2*0.5*1/1.5,F),
 ("binary_entropy","-(p log2 p+(1-p)log2(1-p))","Binary entropy p=0.25?",bent(0.25),F),
 ("present_value","FV/(1+r)^n","PV of 1331 at 10% in 3y?",1331/1.1**3,F),
 ("kelly_criterion","(bp-q)/b","Kelly b=2,p=0.6,q=0.4?",(2*0.6-0.4)/2,F),
 ("body_surface_area","sqrt(h*w/3600)","Mosteller BSA h=180,w=80?",math.sqrt(180*80/3600),F),
 ("ph","-log10[H+]","pH of [H+]=1e-3?",3.0,I),
 ("henderson_hasselbalch","pKa+log10([A-]/[HA])","pH pKa=4 ratio 10?",5.0,I),
 ("snell_angle","asin(n1 sinθ1/n2)","Refraction n1=1,θ1=30,n2=2 (deg)?",math.degrees(math.asin(0.25)),F),
 ("centripetal_force","F=m v^2/r","Centripetal m=2,v=3,r=3?",2*9/3,I),
 ("spring_energy","E=0.5 k x^2","Elastic PE k=200,x=0.1?",0.5*200*0.01,I),
 ("hookes_law","F=k x","Spring force k=100,x=0.05?",5,I),
 ("buoyant_force","Fb=rho V g","Buoyancy rho=1000,V=0.002,g=9.8?",1000*0.002*9.8,F),
 ("pressure","P=F/A","Pressure F=100,A=4?",25,I),
 ("work_done","W=F d cosθ","Work F=10,d=5,θ=60deg?",10*5*0.5,F),
 ("efficiency","out/in*100","Efficiency 30/50?",60,I),
 ("capacitor_energy","E=0.5 C V^2","Cap energy C=2,V=3?",0.5*2*9,I),
 ("thermal_energy","Q=m c dT","Heat m=2,c=4,dT=5?",40,I),
 ("torque","tau=r F sinθ","Torque r=2,F=5,θ=90deg?",10,I),
 ("angular_velocity_lin","v=omega r","Linear speed omega=2,r=3?",6,I),
 ("frequency_period","f=1/T","Frequency T=0.25s?",4,I),
 ("arithmetic_series","S=n/2(a+l)","Arith sum n=10,a=1,l=19?",100,I),
 ("geometric_series","a(1-r^n)/(1-r)","Geo sum a=1,r=2,n=4?",15,I),
 ("nth_term_arith","a+(n-1)d","5th term a=2,d=3?",14,I),
 ("log_change_base","ln x/ln b","log base 3 of 81?",math.log(81)/math.log(3),F),
 ("gcd","greatest common divisor","gcd(48,36)?",math.gcd(48,36),I),
 ("lcm","a*b/gcd","lcm(4,6)?",12,I),
 ("discriminant","b^2-4ac","Discriminant x^2+5x+6?",1,I),
 ("dot_product","sum a_i b_i","Dot [1,2,3].[4,5,6]?",32,I),
 ("matrix_trace","sum diagonal","Trace [[1,2],[3,4]]?",5,I),
 ("trapezoid_area","0.5(b1+b2)h","Trapezoid b1=3,b2=5,h=4?",16,I),
 ("cylinder_volume","pi r^2 h","Cylinder r=2,h=5?",math.pi*4*5,F),
 ("cone_volume","1/3 pi r^2 h","Cone r=3,h=4?",1/3*math.pi*9*4,F),
 ("sphere_surface","4 pi r^2","Sphere surface r=2?",4*math.pi*4,F),
 ("golden_ratio","(1+sqrt5)/2","Golden ratio value?",(1+math.sqrt(5))/2,F),
 ("fibonacci_10","Binet F_n","10th Fibonacci number?",55,I),
 ("harmonic_number","sum 1/k","Harmonic number H_4?",1+1/2+1/3+1/4,F),
 ("median","middle sorted","Median of [3,1,4,1,5]?",3,I),
 ("mode","most frequent","Mode of [1,2,2,3]?",2,I),
 ("range_stat","max-min","Range of [4,8,2,10]?",8,I),
 ("standard_error","sigma/sqrt(n)","SE sigma=10,n=100?",1,I),
 ("confidence_margin","1.96*SE","95% margin SE=1?",1.96,F),
 ("precision","TP/(TP+FP)","Precision TP=8,FP=2?",0.8,I),
 ("recall","TP/(TP+FN)","Recall TP=8,FN=2?",0.8,I),
 ("specificity","TN/(TN+FP)","Specificity TN=90,FP=10?",0.9,I),
 ("gini_impurity","1-sum p^2","Gini [0.5,0.5]?",0.5,I),
 ("entropy_3class","-sum p log2 p","Entropy of 3 equal classes (bits)?",math.log2(3),F),
 ("perplexity","2^H","Perplexity for H=1 bit?",2,I),
 ("manhattan_distance","sum|a-b|","Manhattan [1,2]->[4,6]?",7,I),
 ("odds_from_prob","p/(1-p)","Odds for p=0.8?",4,I),
 ("future_value","PV(1+r)^n","FV PV=1000,r=0.1,n=2?",1210,F),
 ("roi","(gain-cost)/cost*100","ROI gain=150,cost=100?",50,I),
 ("break_even","fixed/(price-varcost)","Break-even fixed=1000,p=10,vc=5?",200,I),
 ("rule_of_72","72/rate","Doubling years at 8%?",9,I),
 ("gross_margin","(rev-cogs)/rev","Gross margin rev=100,cogs=60?",0.4,F),
 ("molarity","moles/liters","Molarity 2 mol in 4 L?",0.5,I),
 ("dilution_v2","C1 V1/C2","Dilution V2: C1=2,V1=1,C2=0.5?",4,I),
 ("percent_yield","actual/theoretical*100","Yield 8/10?",80,I),
 ("poh","14-pH","pOH for pH=3?",11,I),
 ("left_shift","x*2^n","5 << 2?",20,I),
 ("hex_to_dec","hex->decimal","0x1F in decimal?",31,I),
 ("binary_to_dec","binary->decimal","1011 binary in decimal?",11,I),
]

out=[[t,m,q,round(a,6),tol] for (t,m,q,a,tol) in TASKS]
path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"tasks_hard.json")
json.dump(out,open(path,"w"),indent=1)
print("wrote",len(out),"hard tasks; unique terms:",len(set(t[0] for t in TASKS))==len(TASKS))
