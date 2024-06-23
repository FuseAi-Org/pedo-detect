const names = [
    "Michael Johnson", "Emily Brown", "Christopher Davis", "Jessica Wilson",
    "Joshua Miller", "Amanda Anderson", "Daniel Thomas", "Sarah Moore",
    "Matthew Taylor", "Ashley Jackson", "Andrew White", "Megan Harris",
    "David Clark", "Samantha Lewis", "James Hall", "Jennifer Young",
    "John King", "Laura Wright", "Ryan Scott", "Melissa Green",
    "Kevin Adams", "Brittany Baker", "Brian Gonzalez", "Rachel Nelson",
    "Jason Carter", "Heather Mitchell", "Justin Perez", "Michelle Roberts",
    "Brandon Turner", "Kimberly Phillips", "Robert Campbell", "Stephanie Parker",
    "Anthony Evans", "Nicole Edwards", "Steven Collins", "Rebecca Stewart",
    "Timothy Sanchez", "Christina Morris", "Mark Rogers", "Amber Murphy"
  ];
  
  const nameMap = new Map();
  let nameCounter = 0;
  
  const generateUniqueName = (userId) => {
    if (!nameMap.has(userId)) {
      if (nameCounter < names.length) {
        nameMap.set(userId, names[nameCounter]);
        nameCounter++;
      } else {
        // If we run out of names, just use a default naming convention
        nameMap.set(userId, `User${nameCounter}`);
        nameCounter++;
      }
    }
    return nameMap.get(userId);
  };
  
  export default generateUniqueName;
  