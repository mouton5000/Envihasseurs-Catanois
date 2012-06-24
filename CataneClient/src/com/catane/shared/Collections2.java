package com.catane.shared;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;

public class Collections2 {

	public static <T,U> void put(HashMap<T, ArrayList<U>> h, T key, U value){
		ArrayList<U> ar = h.get(key);
		if(ar == null){
			ar = new ArrayList<U>();
			h.put(key,ar);
		}
		ar.add(value);
	}
	
	public static <T> String join(Collection<T> c, char del){
		StringBuilder s = new StringBuilder();
		if(c.size() != 0)
		{
			Iterator<T> it = c.iterator();
			s.append(it.next().toString());
			while(it.hasNext()){
				s.append(del);
				s.append(it.next().toString());
			}
		}
		return s.toString();
	}
}
