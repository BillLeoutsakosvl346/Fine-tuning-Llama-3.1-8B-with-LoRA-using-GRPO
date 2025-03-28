This is a README file explaining how to reproduce the results, and how I felt about the task!


How to reproduce the results:

1) Initial evaluation: To reproduce the initial evaluation you would have to run the initial_eval.py file. 
                        I could probably have set a seed for you to have been able to reproduce the exact same results,
                        but I had forgotten this at the time. Nevertheless, I am testing whether the model gets the
                        numerical answer correct by making it put it after a ####. Its performance with no fine-tuning
                        was at around 45%. This can probably vary but single digit percentage points, but not too much
                        as the temperture is set at 0.1.

2) Fine-tuning: To do the same fine-tuning as I did, you have to run the grpo_training.py file. I selected batch_size=24 
                as I decided to go with an H200 SXM GPU. it was training for close to 7 hours, for 1 epoch over the entire 
                trining set (7473 problems). Adjust the batch_size depending on the gpu(s) you will use so that you have maximum 
                gpu utilisation without OOM issues (I made this mistake myself). Keep in mind that the batch_size has to be
                divisible by the number of generations (num_generations). 

3) Fine-tuned model evaluation: Similarly with the initial evaluation, you have to run the fine_tuned_eval.py. Again didn't 
                                set seed, but temperture is at 0.1, meaning that the results will be a few percentage points 
                                around 80%, and definitely significantly improved from the initial eval you will run.



How I felt about the task:

Well, this is was my first time fine-tuning an LLM, my first time using runpod, and surprisingly my first time interacting with hugging face!
Now at hindsight, I understand why this would be a very simple task for someone who has done similar things, nevertheless I will not sit there
and say yeah yeah it was easy. I encountered many problems, and I think that if someone with experience was watching me trying all sorts of different
things, he would probably laugh at some of my attempts. For example, before I decided to go for GRPO, I was trying to do PPO, and because the library 
required a reward network instead of a function, I was trying to set a trivial network to satisfy the parameter requirement and then add the result of 
the reward function. All of this of course did not work out and I ended up switching to GRPO, after reading more about it and understanding it better.
(I thought it was a different thing before). Also I spent around a day trying to set up an SSH connection and work remotely from VS code, but again I 
ran into countless problems, and I ended up teaching my self how to control everything from a web terminal and github. To someone with experience,
I assume that all the above may seem like I was trying to extract chocolate milk from a brown cow :). Nevertheless, I eventrually managed to push llama from 
45% to 80% performance on the gsm8k test set!
I admit, that due to my lack of experience on similar tasks, I relied on the experience of others on the internet, as well as ChatGPT! For example if you 
asked me why I decided to train only the Q, K, V matrices and the output projections, my answer would be that I did a bit of research online and discussed 
with LLMs and I concluded that this is a classic case for llama in order to balance performance and cost. Afterwards, I was thrilled when I saw the jump 
of the performance go to 80%! 
Finally speaking on my reliance on LLMs to solve the task, the answer is yes, I got a lot of help when it came to things that have to do with experience as well as speeding up
the coding of certain trivial parts and to learn things like what commands I should run in the terminal to do certain tasks, but I always understood my code, 
the assignment of my parameters and the general thinking behing everything to the last line! I am sure that if an experienced person decided these parameters
the results could have been a lot better and cheaper.
Currently, after 5 days of learning and applying things to do this task, I feel like I have learned quite a few things I didn't know, but more importantly,
my appetite for learning these things, especially alogside the people that created the best AI software engineer in the world, grew exponentially! Like I did
in my previous internship, I love researching and figuring things out in the code on my own, and my learning process could be sped up significanlty if advised 
from experts. I am genuinely looking forward to a summer full of coding and fine-tuning so that this is the last time we would have to, if we make genie even better!

Thank you for giving me the opportunity to work on this assignment!