Starting examples
Understanding ODD - https://www.sciencedirect.com/science/article/pii/S030438001000414X

Sample models to learn from: https://modelingcommons.org/browse/one_model/6475#model_tabs_browse_procedures

Examples:
Can two digital conversations on the same platform affect one another? How would I detect this? 
Can we determine when the point of bifurcation happens? Onset bifurcation in digital conversations–the transformation from controlled growth & death (equilibrium) to uncontrolled growth.
At what point do we transition from normal growth to cancerous structure? To do this we might have to give agents some weight or simply count the number of particles on each branch. What is the critical threshold (pc). Will it be the number of replies? And what happens when the conversation reaches this threshold.
How do we determine the equilibrium point, when this critical threshold is reached? What dx/dt=0, what is x in this regard
What is the goal of the digital platforms, reaching stable states or something entirely different?

When does the conversation die? When do people stop replying to a conversation?

We have established that this happens in phases, early engagement, middle engagement and late engagement?

How much capacity can the environment support? What will be our rate of diffusion? The platforms can support a lot of data.

We shall simulate as the model tends to t→ infinity∞. 

# 1. OVERVIEW
 1.1 Purpose 
What is the model for?
What questions does it address?
Who is the intended audience?
Example
Purpose: This model simulates the diffusion of molecules in a heterogeneous environment to understand how obstacles affect diffusion rates. It is designed for students learning about Brownian motion and for researchers studying transport in porous media.

This model simulates the two-dimensional diffusion of molecules undergoing Brownian motion in a heterogeneous environment with obstacles. It is designed to:

Research purpose: Investigate how obstacles and spatial heterogeneity affect diffusion rates and coefficients

Validation purpose: Compare simulated diffusion coefficients with theoretical predictions from the Einstein-Smoluchowski equationPrimary questions addressed:

Possible research questions
How does the diffusion coefficient emerge from random molecular motion?
How do obstacles reduce effective diffusion rates?
Under what conditions is diffusion isotropic (Difx = Dify) vs anisotropic?
How does obstacle density affect the transition from free to hindered diffusion?


 ## 1.2 Entities, state variables, and scales
What to include
Entities: What are the agents/objects?
State variables: What properties do they have?
Scales: Space and time dimensions
### 1.2.1 Entities
Molecules: Individual diffusing particles
Patches: Grid cells representing space
 Environment: The simulation world
### 1.3 State variables
Example
Molecules:
xcor, ycor: Position coordinates
heading: Direction of movement (0-360°)
init-pos-x, init-pos-y: Initial position
dist-x, dist-y: Displacement from origin
Patches:
pcolor: Color (red = obstacle, black = free space)
Globals:
Difx, Dify, Dif: Diffusion coefficients
step-size: Distance moved per time step
zoom: Scaling factor for visualization
### 1.4 Scales
Spatial: 2D grid, zoom × 100 nanometers
Temporal: Each tick = time-step (user-defined)
Number of molecules: User-defined
### 1.5 Process overview and scheduling
What happens each time step?
In what order?
Who acts when?
Example of scheduling
Each time step (tick):
1. All molecules move simultaneously
2. For each molecule:
   a. Choose random heading (0-360°)
   b. Move forward by step-size
   c. If collision with obstacle (red patch):
      - Move back
      - Choose new random heading
   d. Update displacement (dist-x, dist-y)
3. Calculate diffusion coefficients:
   - Difx = mean(dist-x²) / (2 × time)
   - Dify = mean(dist-y²) / (2 × time)
   - Dif = mean(dist-x² + dist-y²) / (4 × time)
4. Update visualizations
Timing: Synchronous updating (all agents move before 
        measurements are taken)
# 2. DESIGN CONCEPTS
##  2.1 Theoretical and empirical background
Basic Principles
What to include:
What theory underlies the model?
What real-world phenomenon does it represent?
Example
The model implements Einstein-Smoluchowski equation for 
Brownian motion:
    ⟨r²⟩ = 2dDt
where ⟨r²⟩ is mean squared displacement, d is dimensions 
(2 for 2D), D is diffusion coefficient, and t is time.
Molecules undergo random walks with:
- Random direction each step (uniform distribution 0-360°)
- Fixed step size (derived from D and Δt)
- Reflective boundaries at obstacles
## 2.2 Individual decision-making
## 2.3 Learning, prediction, sensing
## 2.3.1 Emergence
What to include:
What patterns emerge from individual behaviors?
What is not explicitly programmed?
Example: Emergent properties:
Gaussian distribution of molecule positions over time
Reduced effective diffusion coefficient in presence of obstacles
Isotropic diffusion in homogeneous environments (Difx ≈ Dify)
Anisotropic diffusion with aligned obstacles
These patterns emerge from individual random walks without being explicitly programmed.
### 2.3.2 Adaptation
What to include:
Do agents change their behavior?
How do they adapt?
Example
Molecules do not adapt or learn. Their behavior is purely 
stochastic with constant parameters throughout the simulation.
(Or, if they did adapt):
Molecules reduce step-size when encountering high obstacle density, representing energy loss in collisions.
### 2.3.3 Objective/fitness
What to include:
What are agents trying to achieve?
How is "success" measured?
Example
Molecules have no objectives. They move randomly according to physical laws without goals or fitness measures.
Observation objective: Measure diffusion coefficient D to compare with theoretical predictions.
### 2.3.4 Sensing
What to include:
What information can agents perceive?
How far can they sense?
Example
Molecules sense:
- Obstacle presence: Detect red patches upon collision
- Sensing range: Immediate patch only (no lookahead)
Molecules cannot sense:
- Other molecules (no collision avoidance)
- Distance to obstacles
- Gradient fields
### 2.4 Interaction
What to include:
How do agents interact with each other?
Direct or indirect?
Example
Molecules do NOT interact with each other:
No collision detection between molecules
No communication
No influence on each other's movement
Molecules DO interact with environment:
Collision with obstacles → bounce back
Spatial exclusion from obstacle patches
### 2.5 Stochasticity
What to include:
What is random in the model?
Why is randomness used?
Example
Stochastic elements:
1. Initial molecule positions: Random uniform distribution
2. Movement direction: Random heading each step (uniform 0-360°)

Purpose of stochasticity:
- Represents thermal fluctuations in Brownian motion
- Captures microscopic randomness of molecular collisions
- Essential for emergent diffusion behavior

Pseudo-random number generator: NetLogo's built-in RNG with user-controllable seed for reproducibility

## 2.6 Collectives
What to include:
Do agents form groups?
How are aggregations handled?
Example
No explicit collectives. All molecules are independent.
Implicit collective: The entire population is measured together to calculate mean squared displacement and diffusion coefficient.
## 2.7 Observations
What to include:
What data is collected?
How and when?
Example
Data collected each tick:
- dist-x, dist-y: Individual displacements
- Difx, Dify, Dif: Population-level diffusion coefficients

Visualization:
- Molecule positions (real-time)
- Time series plots of D (updated continuously)

Output: CSV file with time, Difx, Dify, Dif for analysis
# 3. DETAILS
## 3.1 Initialization
What to include:
Initial state of the model
Parameter values
Example:
Initial conditions:
Environment:
- World: 51×51 patches
- Obstacles: User-drawn red patches (or loaded from file)
- Free space: Black patches
Molecules:
- Number: User-defined (default: 100)
- Initial positions: Random in non-obstacle patches
- Initial heading: Not applicable (chosen at first move)
- Initial displacement: (0, 0)
Parameters:
- free-diffusion-value: User-defined (default: 50 nm²/µs)
- time-step: User-defined (default: 0.01 µs)
- zoom: 100 (scaling factor)
- step-size: Calculated from √(4 × D × Δt)
Random seed: User-controllable for reproducibility
## 3.2 Input data
What to include:
External data sources
How is data used?
Example
Optional input:
Obstacle configuration: Can load from file or draw manually
Experimental D values: For comparison/validation
No time-series inputs. All parameters constant during run.
If no obstacle file provided, user draws obstacles interactively before starting simulation.
## 3.3 Submodels
What to include:
Detailed descriptions of each process
Equations, pseudocode, or flowcharts
Example
SUBMODEL 1: Molecule Movement
FOR each molecule:
  1. Choose random heading:
     heading ← random(0, 360)
  2. Calculate attempted move:
     new-x ← xcor + step-size × sin(heading)
     new-y ← ycor + step-size × cos(heading)
  3. Check for obstacles:
     IF patch-at(new-x, new-y) is red:
       REPEAT steps 1-2 until free patch found
     ELSE:
       Move to (new-x, new-y)
  4. Update displacement:
     dist-x ← xcor - init-pos-x
     dist-y ← ycor - init-pos-y
SUBMODEL 2: Diffusion Coefficient Calculation
Called each tick after all molecules move:
1. Calculate mean squared displacements:
   MSDx ← mean(dist-x² for all molecules)
   MSDy ← mean(dist-y² for all molecules)
   MSD ← mean(dist-x² + dist-y² for all molecules)
2. Calculate diffusion coefficients:
   Difx ← MSDx / (2 × current-time × zoom²)
   Dify ← MSDy / (2 × current-time × zoom²)
   Dif ← MSD / (4 × current-time × zoom²)
3. Convert units to nm²/µs
Note: Division by zoom² converts from screen to physical units


