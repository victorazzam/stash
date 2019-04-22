//Damos Swap them all zero days solution

import java.util.Scanner;

public class solution
{
	public static void main(String [] a)
	{
		String[] chars = {"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"};
		String ch = "a";
		for (int ab = 1; ab < 27; ab++)
		{

			for (int i = 0; i < 26;i++)
			{
				if (ab + i < 26)
				{
					ch = chars[i];
					chars[i] = chars[i+ab];
					chars[i+ab] = ch;
				}
			}
		}
		for (String i:chars) System.out.print(i);
		Scanner in = new Scanner(System.in);
		int r = in.nextInt();
	}

}