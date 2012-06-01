package com.catane.shared;

public class Math2 {

	/**
	 * Renvoie le (vrai) reste de la division euclidienne de a par b
	 * @param a
	 * @param b
	 * @return
	 */
	public static int mod(int a, int b){
		int c = a%b;
		if(c < 0)
			c += b;
		return c;
	}
	
	public static int div(int a, int b){
		int c = a/b;
		if(a < 0 && a%b != 0)
			c -= 1;
		return c;
	}
	
	public static void main(String[] args) {
		System.out.println(-23/12 + " " +Math2.div(-24,12));
	}

	public static double dist(double x1, double y1, double x2, double y2) {
		return Math.pow(Math.pow((x2-x1), 2)+Math.pow((y2-y1),2), 0.5);
	}
}
