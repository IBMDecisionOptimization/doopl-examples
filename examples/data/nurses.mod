// --------------------------------------------------------------------------
// Licensed Materials - Property of IBM
//
// 5725-A06 5725-A29 5724-Y48 5724-Y49 5724-Y54 5724-Y55
// Copyright IBM Corporation 1998, 2013. All Rights Reserved.
//
// Note to U.S. Government Users Restricted Rights:
// Use, duplication or disclosure restricted by GSA ADP Schedule
// Contract with IBM Corp.
// --------------------------------------------------------------------------

{string} Weekdays = ...;  
tuple nurse {
  key string name;
  int seniority;
  int qualification;
  int payRate;
}

tuple shift {
   key string departmentName;
   key string day;
   key int startTime;
   key int endTime;
   int minRequirement;
   int maxRequirement;   
}

tuple nurseCouple {
  nurse Nurse1;
  nurse Nurse2;
}

tuple departmentIncompat {
  nurse Nurse;
  string department;
}

//tuple workTimeByNurse {
//   string Nurse;
//   int minTime;
//   int maxTime;
//}

tuple skillRequirement {
  key string department;
  key string skill;
  int number;
}

int MaxWorkTime = ...;
{nurse} Nurses = ...;
{shift} Shifts = ...;
{string} Departments = ...;

{skillRequirement} SkillRequirements = ...;

{nurseCouple} NurseAssoc 
  with Nurse1 in Nurses,Nurse2 in Nurses = ...;
{nurseCouple} NurseIncompat 
  with Nurse1 in Nurses, Nurse2 in Nurses = ...;
{departmentIncompat} DepartmentIncompat
  with Nurse in Nurses, department in Departments  = ...;
  
int Vacations[Nurses][Weekdays] = ...;
//{WorkTimeByNurse} WorkTimeByNurses = ...;

{string} Skills = ...;
int NurseSkill[Nurses][Skills] = ...;

int RequiredAssignments[Nurses][Shifts] = ...;

int AbsStartTime[s in Shifts]= s.startTime + ord(Weekdays,s.day)*24;
int AbsEndTime[s in Shifts] = 
  s.endTime + ord(Weekdays,s.day)*24
  +(( s.startTime > s.endTime )?24:0);
  
int Duration[s in Shifts] = AbsEndTime[s] - AbsStartTime[s];

int incompatShifts[Shifts][Shifts] = [ s1 : [ s2 : 1 ] | s1,s2 in Shifts: AbsStartTime[s2]>=AbsStartTime[s1] && AbsStartTime[s2]<AbsEndTime[s1] ];

dvar int NurseAssignments[Nurses][Shifts] in 0..1;
dvar float+ NurseWorkTime[Nurses];
dvar float+ NurseAvgHours;
dvar float+ NurseMoreThanAvgHours[Nurses];
dvar float+ NurseLessThanAvgHours[Nurses];
dvar float+ Fairness;
dvar int CostByDepartments[Departments];
dvar int AllocationByDepartments[Departments];


minimize 
  sum(d in Departments) 
    CostByDepartments[d];

subject to {
   // cost by department
   forall( d in Departments )
     CostByDepartments[d] == 
     sum( s in Shifts , n in Nurses : s.departmentName == d ) 
       NurseAssignments[n][s] * Duration[s] * n.payRate;
   
   // allocation by department
   forall(d in Departments)
      AllocationByDepartments[d] == sum(s in Shifts, n in Nurses : s.departmentName == d) NurseAssignments[n][s];
   
   // a shift require between min and max Nurses 
   forall(s in Shifts) 
     s.minRequirement <= sum(n in Nurses) NurseAssignments[n][s] <= s.maxRequirement;
   
   forall(n in Nurses) {      
       // time worked by a Nurse
      NurseWorkTime[n] == sum( s in Shifts ) 
        NurseAssignments[n][s]*Duration[s];

      // two shifts at the same time are incompatible
      forall( s in Shifts )
         sum( s2 in Shifts : incompatShifts[s,s2]==1 )
           NurseAssignments[n][s2] <=1;         
   }
   // respect required assignments
     forall( n in Nurses, s in Shifts : RequiredAssignments[n][s] == 1 )
       ctRequiredAssignmentConstraints:
         NurseAssignments[n][s] == 1;
   //global max worked time
     forall(n in Nurses)
       ctNurseMaxTimeConstraints: 
         NurseWorkTime[n] <= MaxWorkTime;

   // Nurse-Nurse incompatibility
     forall( < n1 , n2 > in NurseIncompat , s in Shifts )
       ctNurseIncompatConstraints:
         NurseAssignments[n1][s] + NurseAssignments[n2][s] <= 1; 

   // Nurse association
     forall( < n1 , n2 > in NurseAssoc, s in Shifts)
       ctNurseAssocConstraints:
         NurseAssignments[n1][s] == NurseAssignments[n2][s]; 
  
   // Nurse-shift incompatibility
   forall(s in Shifts, <n, s.departmentName > in DepartmentIncompat)
      NurseAssignments[n][s] == 0;
   
   // max worked time
   // forall( t in workTimeByNurses , n in Nurses : n.name == t.Nurse )
   //   WorkTimeByNurseConstraints[n]=t.minTime <= NurseWorkTime[n] <= t.maxTime;

   // Nurse vacations
   forall( n in Nurses , d in Weekdays : Vacations[n][d] == 1 )
     ctNurseVacationConstraints:
       sum(s in Shifts : s.day == d) NurseAssignments[n][s] == 0;

   // skills
   forall(r in SkillRequirements, s in Shifts : r.department == s.departmentName)
     ctSkillRequirementConstraints:
       sum(n in Nurses : NurseSkill[n][r.skill] == 1) NurseAssignments[n][s] >= r.number;   
  
   forall( n in Nurses )
      NurseWorkTime[n] == NurseAvgHours + NurseMoreThanAvgHours[n] - NurseLessThanAvgHours[n];

   Fairness == sum(n in Nurses) (NurseMoreThanAvgHours[n] + NurseLessThanAvgHours[n]);
      NurseAvgHours == ((card(Nurses) == 0) ? 0  : sum(n in Nurses) NurseWorkTime[n] / card(Nurses));
}


tuple CostByDepartmentsSolutionT{ 
	string Departments; 
	int value; 
};
{CostByDepartmentsSolutionT} CostByDepartmentsSolution = {<i0,CostByDepartments[i0]> | i0 in Departments};
tuple NurseAssignmentsSolutionT{ 
	nurse Nurses; 
	shift Shifts; 	
	int value; 
};
{NurseAssignmentsSolutionT} NurseAssignmentsSolution = {<i0,i1,NurseAssignments[i0][i1]> | i0 in Nurses,i1 in Shifts};
tuple AllocationByDepartmentsSolutionT{ 
	string Departments; 
	int value; 
};
{AllocationByDepartmentsSolutionT} AllocationByDepartmentsSolution = {<i0,AllocationByDepartments[i0]> | i0 in Departments};
tuple NurseWorkTimeSolutionT{ 
	nurse Nurses; 	
	float value; 
};
{NurseWorkTimeSolutionT} NurseWorkTimeSolution = {<i0,NurseWorkTime[i0]> | i0 in Nurses};
tuple NurseMoreThanAvgHoursSolutionT{ 
	nurse Nurses; 	
	float value; 
};
{NurseMoreThanAvgHoursSolutionT} NurseMoreThanAvgHoursSolution = {<i0,NurseMoreThanAvgHours[i0]> | i0 in Nurses};
tuple NurseLessThanAvgHoursSolutionT{ 
	nurse Nurses; 	
	float value; 
};
{NurseLessThanAvgHoursSolutionT} NurseLessThanAvgHoursSolution = {<i0,NurseLessThanAvgHours[i0]> | i0 in Nurses};

