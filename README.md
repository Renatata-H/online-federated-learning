# Online Federated Learning Framework
This is a scientific initiation project with FAPESP funding. You can read more about this [here](https://bv.fapesp.br/pt/bolsas/223950/aprendizado-federado-online-aplicado-em-ciberseguranca/).

The code is not yet finished, and therefore still buggy. But you can run it in your machine if you so wish. 

Tutorial for the current version, which still is bugged and its interaction with user is still being worked on:

1. Clone this repository into all the machines used for the simulation (central operator, attacker, and all the workers, which needs to there be at least 1);
2. Since the config.txt file is not useful yet, manually edit the worker.py so the variable 'operator_id' has a string with the IP4 of the central operator machine;
3. In the same idea, manually edit the variable 'names' of the start_attack() function in attacker.py so that it contains all the computer names of the workers;
4. Now, run each of the following, in this order, in their respective machines: `python3 central.py`, `python3 worker.py` (for all workers) and `python3 attacker.py`.
5. The attacker machine will be waiting for input, which is the port number that it will try to attack the workers. For convinience, use port 12346.

After that, the code should run. 

Note that it is still buggy on the attacker side, so this perhaps will break. This is still a project on course.
