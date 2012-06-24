package com.catane.client.map;

import org.vaadin.gwtgraphics.client.VectorObject;

public final class HexagoneInfos {

	private Terre terre;
	
	private HexagoneInfos left;
	private HexagoneInfos right;
	private HexagoneInfos up;
	private HexagoneInfos down;
	private HexagoneInfos upLeft;
	private HexagoneInfos upRight;
	private HexagoneInfos downLeft;
	private HexagoneInfos downRight;
	
	private int num;
	private String color;
	private VoleurPath voleur;
	private PionPath pastille;
	private PionJoueurPath intLeft;
	private PionJoueurPath intRight;
	
	private RoutePath routLeft;
	private RoutePath routUp;
	private RoutePath routRight;
	private VectorObject batLeft;
	private VectorObject batUp;
	private VectorObject batRight;
	
	
	public HexagoneInfos(int num, Terre terre) {
		this.num = num;
		this.terre = terre;
	}

	public Terre getTerre(){
		return terre;
	}
	
	
	public HexagoneInfos getLeft() {
		return left;
	}

	
	public void setLeft(HexagoneInfos left) {
		this.left = left;
	}

	public HexagoneInfos getRight() {
		return right;
	}

	public void setRight(HexagoneInfos right) {
		this.right = right;
	}

	public HexagoneInfos getUp() {
		return up;
	}

	public void setUp(HexagoneInfos up) {
		this.up = up;
	}

	public HexagoneInfos getDown() {
		return down;
	}

	public void setDown(HexagoneInfos down) {
		this.down = down;
	}

	public HexagoneInfos getUpLeft() {
		return upLeft;
	}

	public void setUpLeft(HexagoneInfos upLeft) {
		this.upLeft = upLeft;
	}

	public HexagoneInfos getUpRight() {
		return upRight;
	}

	public void setUpRight(HexagoneInfos upRight) {
		this.upRight = upRight;
	}

	public HexagoneInfos getDownLeft() {
		return downLeft;
	}

	public void setDownLeft(HexagoneInfos downLeft) {
		this.downLeft = downLeft;
	}

	public HexagoneInfos getDownRight() {
		return downRight;
	}

	public void setDownRight(HexagoneInfos downRight) {
		this.downRight = downRight;
	}

	public VoleurPath getVoleur() {
		return voleur;
	}

	public void setVoleur(VoleurPath voleur) {
		this.voleur = voleur;
		if(voleur!=null)
			voleur.setHi(this);
	}

	public PionPath getPastille() {
		return pastille;
	}

	public void setPastille(PionPath pastille) {
		this.pastille = pastille;
	}

	public PionJoueurPath getIntLeft() {
		return intLeft;
	}

	public void setIntLeft(PionJoueurPath intLeft) {
		this.intLeft = intLeft;
		if(intLeft != null)
			intLeft.setHi(this);
	}

	public PionJoueurPath getIntRight() {
		return intRight;
	}

	public void setIntRight(PionJoueurPath intRight) {
		this.intRight = intRight;
		if(intRight != null)
			intRight.setHi(this);
	}

	public RoutePath getRoutLeft() {
		return routLeft;
	}

	public void setRoutLeft(RoutePath pjp) {
		this.routLeft = pjp;
		if(routUp != null)
			routUp.setHi(this);
	}

	public RoutePath getRoutUp() {
		return routUp;
	}

	public void setRoutUp(RoutePath routUp) {
		this.routUp = routUp;
		if(routUp != null)
			routUp.setHi(this);
	}

	public RoutePath getRoutRight() {
		return routRight;
	}

	public void setRoutRight(RoutePath routRight) {
		this.routRight = routRight;
		if(routUp != null)
			routUp.setHi(this);
	}

	public VectorObject getBatLeft() {
		return batLeft;
	}

	public void setBatLeft(VectorObject arLeft) {
		this.batLeft = arLeft;
		if(arLeft instanceof PionJoueurPath && arLeft != null)
			((PionJoueurPath) arLeft).setHi(this);
	}

	public VectorObject getBatUp() {
		return batUp;
	}

	public void setBatUp(VectorObject arUp) {
		this.batUp = arUp;
		if(arUp instanceof PionJoueurPath && batLeft != null)
			((PionJoueurPath) arUp).setHi(this);
	}

	public VectorObject getBatRight() {
		return batRight;
	}

	public void setBatRight(VectorObject arRight) {
		this.batRight = arRight;
		if(arRight instanceof PionJoueurPath && arRight != null)
			((PionJoueurPath) arRight).setHi(this);
	}

	public int getNum() {
		return num;
	}

	public String getColor() {
		return color;
	}
	
	public void setColor(String color) {
		this.color = color;
	}
	
	
	
}
