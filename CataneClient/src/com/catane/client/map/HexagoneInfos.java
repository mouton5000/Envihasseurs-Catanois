package com.catane.client.map;

import java.util.ArrayList;

import org.vaadin.gwtgraphics.client.DrawingArea;
import org.vaadin.gwtgraphics.client.VectorObject;

import com.catane.client.User;


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

	/**
	 * Si vrai, alors il y a un brigand, sinon un pirate, si null, rien.
	 */
	private VoleurPath voleur;
	private PionPath pastille;

	private PionJoueurPath intLeft;
	private PionJoueurPath intRight;

	private RoutePath routLeft;
	private RoutePath routUp;
	private RoutePath routRight;


	private ArrayList<Bateau> bateauxLeft;
	private ArrayList<Bateau> bateauxUp;
	private ArrayList<Bateau> bateauxRight;
	private VectorObject batLeft;
	private VectorObject batUp;
	private VectorObject batRight;


	public HexagoneInfos(int num, Terre terre) {
		this.num = num;
		this.terre = terre;

		bateauxLeft = new ArrayList<Bateau>();
		bateauxUp = new ArrayList<Bateau>();
		bateauxRight = new ArrayList<Bateau>();

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

	public void setVoleur(VoleurPath voleur){
		this.voleur = voleur;
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

	private void addBat(Bateau b, ArrayList<Bateau> bats, SideDirection dir){
		if(bats.add(b)){
			VectorObject vo = null;
			User u = User.getPlayer(b.getJoueur());
			if(bats.size() == 1){
				switch(b.getType()){
				case TRANSPORT:
					vo = new TransportPath(b.getJoueur(), dir);
					break;
				case CARGO:
					vo = new CargoPath(b.getJoueur(), dir);
					break;
				case VOILIER:
					vo = new VoilierPath(b.getJoueur(), dir);
					break;
				}
			}
			else
			{
				ArrayList<Integer> ar = new ArrayList<Integer>();
				for(Bateau bp : bats)
					ar.add(bp.getJoueur());
				vo = new BateauxGroup(ar, dir);
				if(ar.contains(User.getMe().getNumber()))
					u = User.getMe();

			}

			switch(dir){
			case LEFT :
				setBatLeft(vo);
				break;
			case RIGHT:
				setBatRight(vo);
				break;
			case NONE:
				setBatUp(vo);
				break;

			}
			String color = u.getColor().getColorCode();

			if(vo instanceof PionJoueurPath)
				((PionJoueurPath) vo).setFillColor(color);
			else
				((BateauxGroup) vo).setFillColor(color);
		}
	}

	private void removeBat(Bateau b, ArrayList<Bateau> bats, SideDirection dir){
		if(bats.remove(b)){
			VectorObject vo = null;
			User u = null;
			if(bats.size() == 1){
				Bateau bp = bats.get(0);
				switch(bp.getType()){
				case TRANSPORT:
					vo = new TransportPath(bp.getJoueur(), dir);
					break;
				case CARGO:
					vo = new CargoPath(bp.getJoueur(), dir);
					break;
				case VOILIER:
					vo = new VoilierPath(bp.getJoueur(), dir);
					break;
				}
				u = User.getPlayer(bp.getJoueur());
			}
			else if(bats.size() > 1)
			{
				ArrayList<Integer> ar = new ArrayList<Integer>();
				for(Bateau bp : bats)
					ar.add(bp.getJoueur());
				vo = new BateauxGroup(ar, dir);
				if(ar.contains(User.getMe().getNumber()))
					u = User.getMe();
			}

			/*
			 * S'il n'y a plus de bataeu, vo est null
			 */
			switch(dir){
			case LEFT :
				setBatLeft(vo);
				break;
			case RIGHT:
				setBatRight(vo);
				break;
			case NONE:
				setBatUp(vo);
				break;

			}

			if(vo != null){
				String color = u.getColor().getColorCode();

				if(vo instanceof PionJoueurPath)
					((PionJoueurPath) vo).setFillColor(color);
				else
					((BateauxGroup) vo).setFillColor(color);
			}
		}
	}

	public VectorObject getBatLeft() {
		return batLeft;
	}

	public void addBatLeft(Bateau b){
		ArrayList<Bateau> bats = bateauxLeft;
		SideDirection dir = SideDirection.LEFT;
		addBat(b,bats,dir);
	}

	public void removeBatLeft(Bateau b){
		ArrayList<Bateau> bats = bateauxLeft;
		SideDirection dir = SideDirection.LEFT;
		removeBat(b,bats,dir);
	}

	public void clearBatLeft(){
		bateauxLeft.clear();
		setBatLeft(null);
	}

	private void setBatLeft(VectorObject arLeft) {
		if(batLeft != null && batLeft.getParent() != null)
			((DrawingArea)batLeft.getParent()).remove(batLeft);
		this.batLeft = arLeft;
		if(arLeft instanceof PionJoueurPath && arLeft != null)
			((PionJoueurPath) arLeft).setHi(this);
	}

	public VectorObject getBatUp() {
		return batUp;
	}

	public void addBatUp(Bateau b){
		ArrayList<Bateau> bats = bateauxUp;
		SideDirection dir = SideDirection.NONE;
		addBat(b,bats,dir);
	}

	public void removeBatUp(Bateau b){
		ArrayList<Bateau> bats = bateauxUp;
		SideDirection dir = SideDirection.NONE;
		removeBat(b,bats,dir);
	}

	public void clearBatUp(){
		bateauxUp.clear();
		setBatUp(null);
	}

	private void setBatUp(VectorObject arUp) {
		if(batUp != null && batUp.getParent() != null)
			((DrawingArea)batUp.getParent()).remove(batUp);
		this.batUp = arUp;
		if(arUp instanceof PionJoueurPath && batLeft != null)
			((PionJoueurPath) arUp).setHi(this);
	}

	public VectorObject getBatRight() {
		return batRight;
	}

	public void addBatRight(Bateau b){
		ArrayList<Bateau> bats = bateauxRight;
		SideDirection dir = SideDirection.RIGHT;
		addBat(b,bats,dir);
	}

	public void removeBatRight(Bateau b){
		ArrayList<Bateau> bats = bateauxRight;
		SideDirection dir = SideDirection.RIGHT;
		removeBat(b,bats,dir);
	}

	public void clearBatRight(){
		bateauxRight.clear();
		setBatRight(null);
	}

	private void setBatRight(VectorObject arRight) {
		if(batRight != null && batRight.getParent() != null)
			((DrawingArea)batRight.getParent()).remove(batRight);
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
