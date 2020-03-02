package dk.itu.mario.engine.level;

import java.util.Random;
import java.util.*;

//Make any new member variables and functions you deem necessary.
//Make new constructors if necessary
//You must implement mutate() and crossover()

public class MyDNA extends DNA {

	public int numGenes = 0; // number of genes

	// Use these constants to make your DNA strings.

	// Represents a gap in the floor that Mario can fall through and die.
	public static final char GAP_CHAR = 'G';
	// Represents a straight, flat section of ground.
	public static final char STRAIGHT_CHAR = 'S';
	// Represents ground with coins above it.
	public static final char COINS_CHAR = 'C';
	// Represents a set of stairs that Mario needs to jump over.
	public static final char HILL_CHAR = 'H';
	// Represents ground with monsters over it (e.g., goombas, koopas).
	public static final char MONSTERS_CHAR = 'M';

	// Return a new DNA that differs from this one in a small way.
	// Do not change this DNA by side effect; copy it, change the copy, and return
	// the copy.
	public MyDNA mutate() {
		MyDNA copy = new MyDNA();
		// YOUR CODE GOES BELOW HERE
		Random rand = new Random();
		String chromosome = this.getChromosome();
		// System.out.println(this.getChromosome());
		int mutationLoc = rand.nextInt(chromosome.length());
		String chars = "GSCHM";
		String mutant = "";
		// System.out.println(chromosome.length());
		for (int i = 0; i < chromosome.length(); i++) {
			int randLetterIdx = rand.nextInt(chars.length());
			int randNumber = rand.nextInt(10);
			if (i == mutationLoc) {
				mutant += chromosome.substring(0, i);

				try {
					Integer.parseInt(chromosome.substring(i, i + 1));
					if (chromosome.charAt(i - 1) == 'G') {
						randNumber = rand.nextInt(3);
					}
					mutant += randNumber;
				} catch (Exception e) {

					mutant += chars.charAt(randLetterIdx);
				}

				mutant += chromosome.substring(i + 1, chromosome.length());
			}

		}
		copy.setChromosome(mutant);
		copy.setNumGenes(this.chromosome.length() / 2);
		// System.out.println(copy);

		// YOUR CODE GOES ABOVE HERE
		return copy;

	}

	// Do not change this DNA by side effect
	public ArrayList<MyDNA> crossover(MyDNA mate) {
		ArrayList<MyDNA> offspring = new ArrayList<MyDNA>();
		// YOUR CODE GOES BELOW HERE
		Random rand = new Random();
		String myChromosome = this.getChromosome();
		String mateChromosome = mate.getChromosome();
		int crossPoint = rand.nextInt(myChromosome.length());

		MyDNA childOne = new MyDNA();
		MyDNA childTwo = new MyDNA();

		String chrom1 = mateChromosome.substring(0, crossPoint)
				+ myChromosome.substring(crossPoint, myChromosome.length());
		// System.out.println("Cross1: " + chrom1);
		childOne.setChromosome(chrom1);
		childOne.setNumGenes(chrom1.length() / 2);

		String chrom2 = myChromosome.substring(0, crossPoint)
				+ mateChromosome.substring(crossPoint, mateChromosome.length());
		// System.out.println("Cross2: " + chrom2);
		childTwo.setChromosome(chrom2);
		childTwo.setNumGenes(chrom2.length() / 2);

		offspring.add(childOne);
		offspring.add(childTwo);

		// YOUR CODE GOES ABOVE HERE
		return offspring;
	}

	// Optional, modify this function if you use a means of calculating fitness
	// other than using the fitness member variable.
	// Return 0 if this object has the same fitness as other.
	// Return -1 if this object has lower fitness than other.
	// Return +1 if this objet has greater fitness than other.
	public int compareTo(MyDNA other) {
		int result = super.compareTo(other);
		// YOUR CODE GOES BELOW HERE

		// YOUR CODE GOES ABOVE HERE
		return result;
	}

	// For debugging purposes (optional)
	public String toString() {
		String s = super.toString();
		// YOUR CODE GOES BELOW HERE
		// System.out.println(s);
		// YOUR CODE GOES ABOVE HERE
		return s;
	}

	public void setNumGenes(int n) {
		this.numGenes = n;
	}

}
