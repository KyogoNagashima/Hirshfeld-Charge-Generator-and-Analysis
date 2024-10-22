import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class IRC_Hirshfeld {
	public static int totalCount = -1;
	public static int count = 0; 
	public static int TS = 1;
	public static int index = 0;

	public static void main(String[] args) throws IOException {
		String file_IRC = args[0];
		
		infoScan(file_IRC);
		
		System.out.println("midpoint: "+TS);
		System.out.println("count: "+totalCount);
		
		scanFile(file_IRC);

		System.out.println("Job Completed");
		
	}
	public static void infoScan(String file_IRC) throws FileNotFoundException {
		String trimmedLine = "";
		Scanner s = new Scanner(new File(file_IRC)); //Change file name depending on name of IRC file you want to interpret. Make sure the file is in the same folder as this java doc.
		
		while (s.hasNextLine()) {
			String line = s.nextLine();
			line = line.trim();
			
			if (line.equals("PES minimum detected on this side of the pathway.")) {
				System.out.println("minimum detected");
				if (TS==1) {
					TS += totalCount;
				} else {
					TS += 0;
				}
			}
			
			if (line.equals("Input orientation:")) { //Input Orientation is the keyword to start processing data.
				totalCount++;
				
				for (int i=0; i<5; i++) {
					line = s.nextLine();
				}
				trimmedLine = line.trim();
				
				while (!trimmedLine.equals("Distance matrix (angstroms):")){ //Distance matrix is the keyword to stop reading in data.
					line = s.nextLine();
					trimmedLine = line.trim(); // it is important to trim and remove spaces infront so that it is interpretted by the wordScan properly.

				}
			} 
		} 
		
		s.close();
		 
	}

	public static void scanFile(String file_IRC) throws IOException { 
		boolean firstHalfDone = false;
		boolean midpoint = false;
		
		index = totalCount-TS;
		System.out.println("index: "+index);
		
		String trimmedLine = "";
		Scanner s = new Scanner(new File(file_IRC));
		
		while (s.hasNextLine()) {
			String line = s.nextLine();
			line = line.trim();
			
			if (line.equals("Input orientation:")) { //Input Orientation is the keyword to start processing data.
				
				if (index<=totalCount-1 && firstHalfDone==false) {
					index++; 
				} else {
					firstHalfDone = true; 
					System.out.println("First half done: "+firstHalfDone);
					if (midpoint == false) {
						midpoint = true;
						index = totalCount-TS-1; //
					}

				}
				
				if (firstHalfDone) {
					index--; 
				}
				
				count++;
				if (count%10!=1) { 
					
				} 
				else {
					System.out.println("index: "+index);
					System.out.println("count: "+count);
					
					String numbering = String.valueOf(index);				
					File HQtxt = new File("HQ"+numbering+".com"); //Name of File
					HQtxt.createNewFile(); //Creates a new File
					FileWriter myChange = new FileWriter(HQtxt);
	
					myChange.append("%nprocshared=10"+"\r"+"%mem=12GB"+"\r"+"# m06/genecp"+"\r"); 
					myChange.append("\r");
					myChange.append("title card required"+"\r");
					myChange.append("\r");
					myChange.append("0 1"+"\r");
	
					for (int i=0; i<5; i++) {
						line = s.nextLine();
					}
					
					trimmedLine = line.trim();
					while (!trimmedLine.equals("Distance matrix (angstroms):")){ //Distance matrix is the keyword to stop reading in data.
						//System.out.println(trimmedLine);
						String editedLine = editLine(trimmedLine);
	
						myChange.append(editedLine+"\r");
					
						line = s.nextLine();
						trimmedLine = line.trim(); // it is important to trim and remove spaces infront so that it is interpretted by the wordScan properly.
					}
					
					myChange.append("Pd 0"+"\r");
					myChange.append("SDD"+"\r");
					myChange.append("****"+"\r");
					myChange.append("-C -H -P -Br -N -O -F 0"+"\r");
					myChange.append("def2tzvpp"+"\r");
					myChange.append("****"+"\r");
					myChange.append("\r");
					myChange.append("Pd 0"+"\r");
					myChange.append("SDD"+"\r");
					for (int i=0; i<5; i++) {
						myChange.append("\r");
					}
					
					myChange.close();
				}

				
				
			} 
		} 
		
		s.close();
		
	}
	
	public static String editLine(String line) {
		if (line.equals("---------------------------------------------------------------------")) { //This is the key to signal that we are looking at a new IRC frame.
        	String empty = "";
			return empty;
        }
		String[] split = line.split("\\s+"); //Splits the line when empty space is encountered.
		String element = split[1];
		if (element.equals("1")) {
			element = "H";
		}
		if (element.equals("5")) {
			element = "B";
		}
		if (element.equals("6")) {
			element = "C";
		}
		if (element.equals("7")) {
			element = "N";
		}
		if (element.equals("8")) {
			element = "O";
		}
		if (element.equals("9")) {
			element = "F";
		}
		if (element.equals("46")) {
			element = "Pd";
		}
		String x = split[3]; //extract x coordinate
        String y = split[4]; //extract y coordinate
        String z = split[5]; //extract z coordinate
          
        String finalLine = " "+element+"          "+x+"     "+y+"     "+"     "+z;
        return finalLine;
	}
	
}


























