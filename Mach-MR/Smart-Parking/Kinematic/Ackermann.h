/*
 * Ackermann model : calculations based on Webots driver.h & car.h
 */
#include<stdio.h>
#include<string.h>
#define _USE_MATH_DEFINES
#include<math.h>

// speed limited(according to related rules)
#define MS1 5.0
// steering angle limited(maximum the vehicle can achieve in radian form)
// according to the common standard, take 40(0.698 in radian form);it can be adapted to actual world
#define MA1 0.6981317
// according to a sample, take 0.5 in radian form for the vehicle in Webots
#define MA2 0.5
// a parameter for safe guarantee;it can be adapted;sometimes it is even non-positive
// it stands for the maximum proportion that the vehicle can enter until it is parallel with the parking space
#define alpha 0.1
// a parameter to control the steering angle; take 0.35 in radian;it can be adapted according to width of roads in parking lot
#define mA1 0.35

// initial parameters from other modules
// (xc,yc),(xp,yp),lx,ly,thelta as docu describes(set them positive for simplification); l1,l2 width & len of vehicle
// note that thelta is represented in radian form
// specially, lx is 'trackFront' in 'webots/car.h' ly is 'wheelbase' in 'webots/car.h'
struct parameter{
	double xc;
	double yc;
	double xp;
	double yp;
	double l1;
	double l2;
	double lx;
	double ly;
	double thelta;
};

// choose a pos to start steering with given parameter
void choose_bestpos(parameter &para, double &ang,parameter initpara, double myc, double rbi, double myc2, double rbi2, bool vdirec){
	para.xp = initpara.xp;
	para.yp = initpara.yp;
	para.l1 = initpara.l1;
	para.l2 = initpara.l2;
	para.lx = initpara.lx;
	para.ly = initpara.ly;
	para.thelta = 0.0;
	if(initpara.yc <= myc){
		para.yc = myc;
		if(vdirec == true){
			para.xc = rbi + (para.lx / 2.0) - (para.ly / 2.0) - (para.xp / 2.0);
		}
		else{
			para.xc = rbi + (para.lx / 2.0) + (para.ly / 2.0) - (para.xp / 2.0);
		}
		ang = MA2;
	}
	else if(initpara.yc <= myc2){
		para.yc = initpara.yc;
		if(vdirec == true){
			para.xc = para.yc - (para.ly / 2.0) - (para.xp / 2.0);
		}
		else{
			para.xc = para.yc + (para.ly / 2.0) - (para.xp / 2.0);
		}
		ang = atan(tan(para.ly / (para.yc - (para.lx / 2.0))) - para.lx / (2.0 * para.ly));
	}
	else{
		para.yc = myc2;
		if(vdirec == true){
			para.xc = rbi2 + (para.lx / 2.0) - (para.ly / 2.0) - (para.xp / 2.0);
		}
		else{
			para.xc = rbi2 + (para.lx / 2.0) + (para.ly / 2.0) - (para.xp / 2.0);
		}
		ang = atan(tan(para.ly / rbi2) - para.lx / (2.0 * para.ly));
	}
}


// calculate max angles & min radius
void cal_max_min(parameter para, double &MR_bi){
	// calculate the max angle of the front-inside wheel according to Ackerann geometry
	double MAi = atan(tan(MA2) + para.lx / (2.0 * para.ly));
	// calculate the min radius of the back-inside wheel
	MR_bi = para.ly / tan(MAi);
}

// judge whether the vehicle can succeed in parking
// it only depends on the yc when the direction of the vehicle is parallel to x-axis
// return the minimum yc, minimum r_back_inside; vdirec:true--forward parking false--backward parking
void cal_yc_rbi(parameter para, bool vdirec, double &Myc, double &R_bi){
	cal_max_min(para, R_bi);
	if(vdirec == true){
		Myc = R_bi + (para.lx / 2.0) + (para.l2 *(1 - alpha));
	}
	else{
		Myc = R_bi + (para.lx / 2.0) - (para.l2 * alpha);
	}
}

// return the max yc, max rbi
void cal_yc_rbi2(parameter para, bool vdirec, double &Myc, double &R_bi){
	R_bi = para.ly / tan(mA1);
	if(vdirec == true){
		Myc = R_bi + (para.lx / 2.0) ;
	}
	else{
		Myc = R_bi + (para.lx / 2.0) + para.l2;
	}
}
