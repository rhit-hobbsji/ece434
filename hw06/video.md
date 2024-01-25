1. Where does Julia Cartwright work?
National Instruments

2. What is PREEMT_RT? Hint: Google it.
Patches for linux kernel to implement real-time computing

3. What is mixed criticality?
Thr process of running different tasks in this case real time vs non real time applications through hardware or software.

4. How can drivers misbehave?
Drivers can have issues in performance, communications amongs each others, or just not being updated

5. What is Δ in Figure 1?
The time between the event and real-time task executes

6. What is Cyclictest[2]?
Takes a two time stamps and measures the duration between the sleep supposed sleep time to get delta.

7. What is plotted in Figure 2?
The plot of the cyclictest for a mainline kernel and real time kernel for preempt and preempt_rt.

8. What is dispatch latency? Scheduling latency?
Dispatch latency is the amount of time between the event to occur and thread waking up. Scheduling latency is the amount of time for the thread to be executed.

9. What is mainline?
The official version of the kernel.

10. What is keeping the External event in Figure 3 from starting?
Running the thread through the interrupt handler causing requests to be delayed until irq is free.

11. Why can the External event in Figure 4 start sooner?
IRQ is only used to wake up the threads allowing for higher priroity interrupt to be scheduled on top of an current thread.
