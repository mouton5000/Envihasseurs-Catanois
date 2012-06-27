package com.catane.client.map;

import com.catane.client.map.MapConnectable.LinkType;

public class Bateau {

	private int num;
	private int joueur;
	private LinkType type;
	
	
	public Bateau(int num, int joueur, LinkType type) {
		super();
		this.num = num;
		this.joueur = joueur;
		this.type = type;
	}


	public int getNum() {
		return num;
	}


	public int getJoueur() {
		return joueur;
	}


	public LinkType getType() {
		return type;
	}
	
	@Override
	public boolean equals(Object obj) {
		Bateau b;
		if(obj instanceof Bateau){
			b = (Bateau) obj;
			return b.num == num && b.getType() == b.getType();
		}
		return false;
	}
	
	@Override
	public int hashCode() {
		return super.hashCode();
	}
	
	@Override
	public String toString() {
		return "["+this.getNum()+" "+this.joueur+" "+this.getType()+"]"; 
	}
	
	
}
