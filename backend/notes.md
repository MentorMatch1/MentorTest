### Matching Algorithm.
Accounting for the model selecting the same mentor for max. 

For the first iteration around should we make sure the scores are above a certain level?

## Issues:
Greedy algorithm here? It picks the optimal mentor for each mentee on the first iteration, however this may cause for that menotrs slots to be immediately filled
up and other people down the line who are better fits for that specific mentor may have difficult fits.
How do we overcome this?

We can try an approach where if a person has multiple fits above 0.80 then we can randomly choose one (as they will all be good fits)
This might allow for people down the line to have their optimal fit as well. 

# Would this problem exist? In general computer science people will have good matching scores with other computer science people, same with other majors (etc)
# it might be a rare case as everyones descriptions are very unique, so many people will be matched differently on all iterations?

If all of a specific mentors slots are filled up then we will remove them from being able to be picked. 
However this may cause a problem that there are outliers within the iteration that they might not get a very good mentor.

Should we have a threshold limit of they must be a good match above 70%? Depends on the real life data
The model wont be perfect either, its just doing the best it can to match based of off the parameters given, in any case there will be outliers
As long as these outliers are outlined and their best fits are shown

Matching based off of percentage levels (ex) starting with 0.90 matches, then next iteration 0.80 matches, going further down until 0.60
