package com.catane.client.map;

import java.util.ArrayList;
import java.util.Iterator;

import com.catane.client.CataneClient;
import com.catane.client.infosWidgets.InfoWidget;


public class Terre {

	private String name;
	private int index;
	
	public String getName() {
		return name;
	}
	
	public int getIndex(){
		return index;
	}

	public Terre(int index, String name) {
		super();
		this.name = name;
		this.index = index;
	}
	
	private static ArrayList<Terre> terres = new ArrayList<Terre>();
	private static Terre chosenOne;
	
	public static Terre getChosenOne() {
		return chosenOne;
	}
	
	public static Terre getTerre(int index){
		return terres.get(index);
	}

	public static Iterator<Terre> getTerreIterator(){
		return terres.iterator();
	}
	
	public static void makeTerres(){
		String[] names = Map.terres;
		
		int i = 0;
		for(String s : names)
			terres.add(new Terre(i++,s));
		chosenOne = terres.get(0);
	}
	
	public void choose(){
		chosenOne = this;
		Map.getLittleMap().draw();
		InfoWidget iw = CataneClient.instance.info;
		iw.getLb().setSelectedIndex(index);
		iw.refreshInfos();
		
		
	}
	
}
