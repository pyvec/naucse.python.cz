# Domácí projekty

Pošlete svým koučům řešení úloh 6 a 8.

Úloha 8 se vám možná bude zdát složitá a nepřehledná a vyplodíte pravděpodobně trochu zamotaný kód, což je v pořádku. V dalších lekcí si budeme ukazovat, jak tento program zlepšit a budeme refaktorovat. I když je spousta z vás napřed, zkuste využít k psaní programu jen to, co byste měli znát z předchozích lekcí. Nepište funkce, nepoužívejte try/except bloky, zkuste to pravdu napsat jen pomocí IFů. Budete nad tím muset přemýšlet opravdu do hloubky a pak vám bude dávat větší smysl, až se bude kód vylepšovat a upravovat.


## Pet names, Mountain Heights


### Pet Names
Create a dictionary to hold information about pets. Each key is an animal's name, and each value is the kind of animal.
  - For example, 'ziggy': 'canary'
Put at least 3 key-value pairs in your dictionary.
Use a for loop to print out a series of statements such as "Willie is a dog."



### Pet Names 2
Make a copy of your program from Pet Names.
Modify one of the values in your dictionary. You could clarify to name a breed, or you could change an animal from a cat to a dog.
  - Use a for loop to print out a series of statements such as "Willie is a dog."
Add a new key-value pair to your dictionary.
  - Use a for loop to print out a series of statements such as "Willie is a dog."
Remove one of the key-value pairs from your dictionary.
  - Use a for loop to print out a series of statements such as "Willie is a dog."
Bonus: Use a function to do all of the looping and printing in this problem.


 
### Mountain Heights

Wikipedia has a list of the tallest mountains in the world, with each mountain's elevation. Pick five mountains from this list.
  - Create a dictionary with the mountain names as keys, and the elevations as values.
  - Print out just the mountains' names, by looping through the keys of your dictionary.
  - Print out just the mountains' elevations, by looping through the values of your dictionary.
  - Print out a series of statements telling how tall each mountain is: "Everest is 8848 meters tall."
Revise your output, if necessary.
  - Make sure there is an introductory sentence describing the output for each loop you write.
  - Make sure there is a blank line between each group of statements.

### Mountain Heights 2
Revise your final output from Mountain Heights, so that the information is listed in alphabetical order by each mountain's name.
  - That is, print out a series of statements telling how tall each mountain is: "Everest is 8848 meters tall."
  - Make sure your output is in alphabetical order.

### Mountain Heights 3
This is an extension of Mountain Heights. Make sure you save this program under a different filename, such as mountain_heights_3.py, so that you can go back to your original program if you need to.
  - The list of tallest mountains in the world provided all elevations in meters. Convert each of these elevations to feet, given that a meter is approximately 3.28 feet. You can do these calculations by hand at this point.
  - Create a new dictionary, where the keys of the dictionary are still the mountains' names. This time however, the values of the dictionary should be a list of each mountain's elevation in meters, and then in feet: {'everest': [8848, 29029]}
  - Print out just the mountains' names, by looping through the keys of your dictionary.
  - Print out just the mountains' elevations in meters, by looping through the values of your dictionary and pulling out the first number from each list.
  - Print out just the mountains' elevations in feet, by looping through the values of your dictionary and pulling out the second number from each list.
  - Print out a series of statements telling how tall each mountain is: "Everest is 8848 meters tall, or 29029 feet."
Bonus:
  - Start with your original program from Mountain Heights. Write a function that reads through the elevations in meters, and returns a list of elevations in feet. Use this list to create the nested dictionary described above.


### Mountain Heights 4
This is one more extension of Mountain Heights.
  - Create a new dictionary, where the keys of the dictionary are once again the mountains' names. This time, the values of the dictionary are another dictionary. This dictionary should contain the elevation in either meters or feet, and the range that contains the mountain. For example: {'everest': {'elevation': 8848, 'range': 'himalaya'}}.
  - Print out just the mountains' names.
  - Print out just the mountains' elevations.
  - Print out just the range for each mountain.
  - Print out a series of statements that say everything you know about each mountain: "Everest is an 8848-meter tall mountain in the Himalaya range."


# Bonusy

Článek, který vysvětluje rozdíl mezi [seznamy a slovníky](https://www.quora.com/What-is-the-main-difference-between-a-list-tuple-and-dictionaries)