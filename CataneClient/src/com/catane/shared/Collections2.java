package com.catane.shared;

import java.util.ArrayList;
import java.util.HashMap;

public class Collections2 {

	public static <T,U> void put(HashMap<T, ArrayList<U>> h, T key, U value){
		ArrayList<U> ar = h.get(key);
		if(ar == null){
			ar = new ArrayList<U>();
			h.put(key,ar);
		}
		ar.add(value);
	}
}
