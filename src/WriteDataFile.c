/*
*  This function creates and writes the data file to be used with LAMMPS
*/
#include "msi2lmp.h"
#include "Forcefield.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>
void WriteDataFile(char *nameroot)
{
double center[3];
double pi=3.1415926;
double aa,ba;						
double xshift,zshift,xfen,zfen;				
double hb,kb,lb,ub,vb,wb,ob,pb,qb;	
double xdd,bb,zdd;					
double xinx,xiny,xinz;				
double x1,z1,rr;					
double xita,qq;
double rxin,ream,rdong;						
aa=2.855;
ba=0;
xshift=25;
zshift=25;
xfen=48;
zfen=48;
ub=1;
vb=2;
wb=-1;
hb=-1;
kb=1;
lb=1;
ob=1;
pb=0;
qb=1;
xdd=aa*sqrt(ub*ub+vb*vb+wb*wb);		
bb=aa*sqrt(hb*hb+kb*kb+lb*lb)*ba;	
zdd=aa*sqrt(ob*ob+pb*pb+qb*qb);		
rxin=3*xdd;		
ream=2.5*xdd+rxin;	
rdong=0.5*xdd+ream;	
center[0] = center[1] = center[2] = 0.0;
  for(kk=0; kk < total_no_atoms; kk++) {
	center[0] += atoms[kk].x[0];
        center[1] += atoms[kk].x[1];
        center[2] += atoms[kk].x[2];
  }
  center[0] /= (double) total_no_atoms;
  center[1] /= (double) total_no_atoms;
  center[2] /= (double) total_no_atoms;
  center[0]=pbc[0]/2;
  center[1]=pbc[1]/2;
  center[2]=pbc[2]/2;

xinx=center[0]+xdd*xshift/xfen;		
xiny=0;
xinz=center[2]+zdd*zshift/zfen;		
   for(kk=0; kk < total_no_atoms; kk++) {
		xita=0;qq=0;
		atoms[kk].x[0]-=xinx;
		atoms[kk].x[1]-=xiny;
		atoms[kk].x[2]-=xinz;
		x1=atoms[kk].x[0];
		z1=atoms[kk].x[2];
		rr=sqrt(x1*x1+z1*z1);
		if((rr>0)&&(z1>0)) xita=acos(x1/rr);
		else {if((rr>0)&&(z1<=0)) xita=2*pi-acos(x1/rr);}
		qq=bb/(2*pi)*xita;
		atoms[kk].x[1]+=qq;
	}
	 box[0][0] -= xinx;
	 box[0][1] -= xiny;
	 box[0][2] -= xinz;
	 box[1][0] -= xinx;
	 box[1][1] -= xiny;
	 box[1][2] -= xinz;
 int total_no_atoms1;
  total_no_atoms1=0;
  no_atom_types=4;
  atomtypes[0].mass=26.982000;
  atomtypes[1].mass=58.710000;
  atomtypes[2].mass=26.982000;
  atomtypes[3].mass=58.710000;
   for(kk=0; kk < total_no_atoms; kk++) {
   rr=sqrt(atoms[kk].x[0]*atoms[kk].x[0]+atoms[kk].x[2]*atoms[kk].x[2]);
    if (rr<=rdong ) {
    total_no_atoms1++;	
    if (rr>=ream ) {atoms[kk].type=atoms[kk].type+2;}
    else atoms[kk].type=atoms[kk].type;
  }
 }
  int k;
  char line[MAX_LINE_LENGTH];
  FILE *DatF;
  /* Open data file */
  sprintf(line,"%s.data",rootname);
  if (pflag > 0) {
    printf(" Writing LAMMPS data file %s.data",rootname);
    if (forcefield & FF_TYPE_CLASS1) puts(" for Class I force field");
    if (forcefield & FF_TYPE_CLASS2) puts(" for Class II force field");
    if (forcefield & FF_TYPE_OPLSAA) puts(" for OPLS-AA force field");
  }
  if ((DatF = fopen(line,"w")) == NULL ) {
    printf("Cannot open %s\n",line);
    exit(62);
  }
  if (forcefield & (FF_TYPE_CLASS1|FF_TYPE_OPLSAA)) total_no_angle_angles = 0;
  if (hintflag) fprintf(DatF, "LAMMPS data file. msi2lmp " MSI2LMP_VERSION
                        " / CGCMM for %s\n\n", nameroot);
  else fprintf(DatF, "LAMMPS data file. msi2lmp " MSI2LMP_VERSION
               " for %s\n\n", nameroot);
  fprintf(DatF, " %6d atoms\n", total_no_atoms1);	
  fputs("\n",DatF);
  fprintf(DatF, " %3d atom types\n", no_atom_types);	
  /* Modified by SLTM to print out triclinic box types 10/05/10 - lines 56-68 */
  if (TriclinicFlag == 0) {	
    fputs("\n",DatF);
    fprintf(DatF, " %15.9f %15.9f xlo xhi\n", box[0][0], box[1][0]);
    fprintf(DatF, " %15.9f %15.9f ylo yhi\n", box[0][1], box[1][1]);
    fprintf(DatF, " %15.9f %15.9f zlo zhi\n", box[0][2], box[1][2]);
  } else {	
    fputs("\n",DatF);
    fprintf(DatF, " %15.9f %15.9f xlo xhi\n", box[0][0], box[1][0]);
    fprintf(DatF, " %15.9f %15.9f ylo yhi\n", box[0][1], box[1][1]);
    fprintf(DatF, " %15.9f %15.9f zlo zhi\n", box[0][2], box[1][2]);
    fprintf(DatF, " %15.9f %15.9f %15.9f xy xz yz\n",box[2][0], box[2][1], box[2][2]);
  }
  /* MASSES */
  fprintf(DatF, "\nMasses\n\n");
  for(k=0; k < no_atom_types; k++) {
    if (hintflag) fprintf(DatF, " %3d %10.6f # %s\n",k+1,atomtypes[k].mass,atomtypes[k].potential);
    else fprintf(DatF, " %3d %10.6f\n",k+1,atomtypes[k].mass);
  }
  fputs("\n",DatF);
  /* ATOMS */
  if (hintflag) fputs("Atoms # full\n\n",DatF);
  else fputs("Atoms\n\n",DatF);
for(k=0; k < total_no_atoms; k++) {
     int typ = atoms[k].type;
     rr=sqrt(atoms[k].x[0]*atoms[k].x[0]+atoms[k].x[2]*atoms[k].x[2]);
    if (rr<=rdong) {
    fprintf(DatF," %6i  %3i  %15.9f %15.9f %15.9f ",
            k+1,
            typ+1,
            atoms[k].x[0],
            atoms[k].x[1],
            atoms[k].x[2]);
    if (hintflag) fprintf(DatF," # %s\n",atomtypes[typ].potential);
    else fputs("\n",DatF);
  }
 
}
  fputs("\n",DatF);
  /* Close data file */
  if (fclose(DatF) !=0) {
    printf("Error closing %s.lammps05\n", rootname);
    exit(61);
  }
}

