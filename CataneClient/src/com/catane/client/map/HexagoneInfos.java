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
	private VectorObject arLeft;
	private VectorObject arUp;
	private VectorObject arRight;
	
	
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
		intLeft.setHi(this);
	}

	public PionJoueurPath getIntRight() {
		return intRight;
	}

	public void setIntRight(PionJoueurPath intRight) {
		this.intRight = intRight;
		intRight.setHi(this);
	}

	public VectorObject getArLeft() {
		return arLeft;
	}

	public void setArLeft(VectorObject arLeft) {
		this.arLeft = arLeft;
		if(arLeft instanceof PionJoueurPath)
			((PionJoueurPath) arLeft).setHi(this);
	}

	public VectorObject getArUp() {
		return arUp;
	}

	public void setArUp(VectorObject arUp) {
		this.arUp = arUp;
		if(arUp instanceof PionJoueurPath)
			((PionJoueurPath) arUp).setHi(this);
	}

	public VectorObject getArRight() {
		return arRight;
	}

	public void setArRight(VectorObject arRight) {
		this.arRight = arRight;
		if(arRight instanceof PionJoueurPath)
			((PionJoueurPath) arRight).setHi(this);
	}

	public int getNum() {
		return num;
	}

	public String getColor() {
		// TODO Auto-generated method stub
		return color;
	}
	
	public void setColor(String color) {
		// TODO Auto-generated method stub
		this.color = color;
	}
	
	
	
}
