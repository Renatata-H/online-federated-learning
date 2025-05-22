# Online Federated Learning Framework
This is a scientific initiation project with FAPESP funding. You can read more about this [here](https://bv.fapesp.br/pt/bolsas/223950/aprendizado-federado-online-aplicado-em-ciberseguranca/).

The code is not yet finished, and therefore still buggy. But you can run it in your machine if you so wish. 

Tutorial for the current version, which still is bugged and its interaction with user is still being worked on:

1. Clone this repository into the server machine (central operator);

2. Edit the `/src/config.py` file so that `server_ip` has the IPv4 address of this machine, and also list all of the workers' names in `workers_names`. Create the empty repository `/src/logs` as well;

3. Copy this configured repository into all the other machines used for the simulation — the attacker and all the workers, of which it is necessary to have at least 1;

4. Now run each of the folloing, in this other, in their respective machines:
        `python3 /src/server.py`
        `python3 /src/client.py` (for all workers)
        `python3 /src/attacker.py`

After that, the code should run. 

Note that it is still buggy on the attacker/client sidess, so this perhaps will break. This is still a project on course.
