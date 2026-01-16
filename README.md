# Pure Fields of Small Discriminant

This project is a follow up to my [project on quadratic fields](https://github.com/algebraity/quadratic-field-analysis) where I did something similar. My goal is to compute the invariants all all pure, totally real fields with a minimal polynomial of degree p from 2 to some small prime, with discriminant less than some large number that is still computationally feasible.

I learned some interesting things from my previous project, but now that I know more about number fields, I would like to track more invariants for more fields and see what patterns I can find. This would also make a good entry level data engineering project once I have all the numbers, which will enable me to use my fledgling data analysis skills in an interesting way.

# Roadmap

My first course of action is to figure out what all I want to compute. Once I have a list, I will test it out on totally real quadratics in a way similar to what I did before. Then, I will generalize the code and allow and prime and a bound on the discriminant to be entered, so I can compute these invariants for much larger fields. I will then slowly compute invariants for larger and larger fields, gathering an extensive data set in the process.

Checklist:
1. Decide list of invariants to compute and the methods by which to compute them.
2. Appropriate my code from [my previous project](https://github.com/algebraity/quadratic-field-analysis) to compute these new invariants.
3. Generalize the code so I can compute with a bound on the discriminant, and use any degree.
4. Start generating the data sets.
