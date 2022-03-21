Weight lifting is a category of strength training where an athlete repeatedly performs an exercise with adjustable load (progressive overload) to strength muscles, bones or neurological connections of the body. These exercises are often performed with a piece of equipment called a barbell in motions such as the bench press, squat, deadlift or overhead press. It's common for lifters to complete each of these exercises in sets (groups) with some desired number of reps for each repeated set. 5x5 (5 sets of 5 reps) or 3x8 (3 sets of 8 reps) are commonly desired exercise volume programs for single exercises. While a new weight lifter may add 5 lbs to their 5x5 squat each week, it can be harder to continue progressing as an advanced athlete.  

To optimize muscle gains and performance, many sub-disciples of weight lifting have been developed to hone & optimize performance. Some athletes may training with a 'time-under-tension' (hypertrophy) or an 'explosive' (velocity based training) focus to optimize that aspect of their training, but it can be difficult to measure progress/performance with such metrics that are harder to compare/record unlike counting the number of reps in your head as the exercise is performed.

An exciting 'data-driven' approach to weight training is on the horizon with equipment historically only usable by professional trainers & athletes making it into the hands of consumers. [Calibrex](https://calibrex.com/) is a hardware & software startup selling an affordable barbell velocity recording solution targeting consumers & less-specialized trainers. Their sub-200 dollar system rivals existing $1000+ dollar solutions already used by professional athletes & olympic weightlifters.

For our final project in 528, we want to build an improved android version of the iOS Calibrex smartphone application. We see two main limitation with their implementation: 1) the trainer or athlete must inform the application an exercise has started by pressing 'start' & 'stop' 2) the user must also enter the exercise they are performing & the weight.

We believe we can automate these user tasks by identifying 'repetition events' in the continuous stream of the barbell height/distance data. Instead of requiring the user to identify the start and end points of a particular exercise, our solution would automatically identify these events without user input. Achieving this would allow the user to forget about having to record their lifting data within the Calibrex app, and only requires them to attach the sensors to their barbell, avoiding all interaction with their smartphone until after the session, ultimately limiting distraction and improving ease of use.

Existing Calibrex Sensor Usage:

![Trainer/User Example](https://github.com/naman159/528-final-project/blob/main/images/draw.jpg?raw=true)

![Calibrex App](https://github.com/naman159/528-final-project/blob/main/images/calibrex.png?raw=true)

![Calibrex Data Output](https://github.com/naman159/528-final-project/blob/main/images/calibrex-out.png?raw=true)

Final Project Backlog:
- Android Application that can connect to two BLE sensors & records lidar distance data
- On-device set recognition (Can we identify when the user is performing an exercise vs resting vs changing weight?)
- On-device sep recognition within a set (Can we correctly identify the number of reps performed during the set and exclude noise from walk-out and rest?)
- On-device exercise recognition for a series of sets (Can we identify when the user changes to a different exercise?)
- Post-exercise report generation (Can we provide a useful & accurate summary of the session to the user?)
