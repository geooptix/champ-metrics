# champ-metrics
Aux metric calculations

Requirements:

`pip install azure-storage`

Usage:
````
usage: start.py [-h] logFile visitID [visitID ...]

positional arguments:
  logFile     Path to output log file
  visitID     Visit ID

optional arguments:
  -h, --help  show this help message and exit
````

Examples:
````
start.py output.log 3667
start.py output.log 3218 3219 4178 4278 4179 3222 2466 3348 3294 4279 3765 2467 3349 3295 3767 2758 3663
start.py output.log 3224 3248 3073 3074 2736 3647 4512 2737 2738 3649 2740 3650 4514 2741 3652 3661 2757
start.py output.log 2742 2743 2744 3653 4515 2748 3654 4516 2749 3655 2750 2751 3657 3658 3659 2755 3660
````
