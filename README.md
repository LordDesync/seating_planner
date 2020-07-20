# Seating Planner
Program to assist in creating seating plans for various events.

Written as part of an A-Level qualification.<br>
I have never been formally taught Python; if you look at my source code, I am taking no responsibility for any damage done to brain.<br>
Also have never used github before, so I've probably messed it up somehow.

## Program Usage

Enter:<br>
- Maximum number of guests per table at the top.<br>
- Name of guests in "names" column.<br>
- Each guest's preferences (who they would like to sit with, 3 maximum) in the "preferences" columns.<br>

- "Execute" to generate seating plan. May take some time to complete computation.<br>
- "Clear All" deletes *ALL* user input data. Excercise suitable caution.

Please distinguish between guests with identical first names where applicable; i.e.  use "Joe A" and "Joe B".<br>
Additionally, all entries in any column or row are case sensitive. Take care when entering data.<br>
Using special characters (#,",```,...) may possible cause undocumented behaviour.<br>

## TROUBLESHOOTING

| ERROR MESSAGE     	| METHOD                                                                                                                                                                                     	|
|-------------------	|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| INPUT ERROR       	| MAX SEATING PER TABLE MUST BE ENTERED IN ARABIC NUMERALS; 1,2,3...<br>DO NOT USE COMMAS OR PERIODS.                                                                                        	|
| TABLES MUST BE >2 	| PROGRAM ONLY SUPPORTS TABLES OF SIZE 3 OR GREATER<br>WORKAROUND: IF SMALLER TABLES ARE ABSOLUTELY REQUIRED, INPUT TWICE THE SIZE OF EACH TABLE, THEN SPLIT EACH TABLE.                     	|
| NOT ENOUGH DATA   	| THE NUMBER ENTERED AT THE TOP IS GREATER THAN THE NUMBER OF GUESTS.<br>PLEASE NOTE THAT THE NUMBER AT THE TOP IS THE MAXIMUM NUMBER OF GUESTS *PER TABLE*, AND NOT TOTAL NUMBER OF GUESTS. 	| 
| INVALID PREFERENCE  | THERE IS A PREFERENCE WHICH IS NOT ADDED AS A GUEST; e.g;<br>GUEST A WANTS TO SIT WITH GUEST B, BUT GUEST B IS NOT ENTERED IN THE NAMES COLUMN                                              | 

## KNOWN ̶I̶S̶S̶U̶E̶S *INTENDED FEATURES*

  DUE TO THE INHERENT UNPREDICTABLE VARIATION OF INPUT, THE PROGRAM MAY OCCASIONALLY OUTPUT VERY SMALL TABLES.
  THESE ARE GENERALLY EASILY FIXED MANUALLY, AS OTHER GENERATED TABLES USUALLY HAVE SPARE SEATS.

  DUE TO COMPUTATIONAL LIMITATIONS AND TIME COMPLEXITY, IT IS NOT FEASIBLE TO PRODUCE AN ABSOLUTE OPTIMAL SOLUTION.
  (SEE BIG O NOTATION AND SET PARTITIONING PROBLEM/K-COLOUR VERTEX COLOURING PROBLEM).
  THIS PROGRAM WILL GENERATE A "GOOD" BUT NOT NECESSARILY OPTIMAL SOLUTION. MAKE MODIFICATIONS TO INAPPROPRIATE TABLES AT YOUR DISCRETION.
  PROGRAM MAY TAKE SEVERAL SECONDS TO PRODUCE A RESULT, PARTICULARLY FOR LARGE EVENTS (>500 GUESTS).

  IF YOU ENCOUNTER A BUG NOT MENTIONED, IT IS NOW A FEATURE.

## INFO

    Copyright (C) 2020  Ryan Liu

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

## CONTACT

  Email;   liurjk@gmail.com<br>
  Discord; Desync#6290

## INFO
WRITTEN IN PYTHON 3.8.1<br>
CREATED BY Ryan JK Liu/Desync<br>
SOURCE CODE AVAILABLE AT: <https://github.com/LordDesync/seating_planner>
