import java.util.Scanner;

public class Main{

    private static Scanner sc;
    private static String userInput;
    private static String[] stopWords;

    /**
    * The main method of this program (start of execution)
    */
    public static void main(String[] args){

        //
        // init class properties
        //
        userInput = "";
        sc = new Scanner(System.in);
        stopWords = new String[]{"bye", "stop", "end", "quit", "goodbye"};

        // prompt user for input
        System.out.println("Hello, how are you feeling?");

        while(true){

            // get user input
            userInput = sc.nextLine();

            // check if user wants to end session
            if( stopWordsContains(userInput) ){
              break;
            }

            //
            // Modify user input here / sent request to API
            //

            userInput = userInput;

            //
            // User input has been modified
            //

            System.out.println("Are you really feeling " + userInput + "?");

        }
    }

    public static Boolean stopWordsContains(String word){
        for(String s : stopWords){
            if( word.equals(s) ){
                return true;
            }
        }
        return false;
    }
}
