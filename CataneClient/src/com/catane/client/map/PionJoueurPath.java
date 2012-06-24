package com.catane.client.map;

import com.catane.client.Colors.PlayerColors;

public abstract class PionJoueurPath extends PionPath{
	private int joueur;

	
	public PionJoueurPath(int i) {
		super(0,0);
		this.setJoueur(i);
	}

	public int getJoueur() {
		return joueur;
	}

	public void setJoueur(int joueur) {
		this.joueur = joueur;
	}

	public void color() {
		this.setFillColor(PlayerColors.getPlayerColor(getJoueur()));
	}
	
}

class ColoniePath extends PionJoueurPath {


	public static final double COLONIE_HEIGHTR = 0.17;
	public static final double COLONIE_WIDTHR = 0.20;
	

	public static final int w = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH * COLONIE_WIDTHR);
	public static final int h = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH * COLONIE_HEIGHTR);

	
	

	/**
	 * Renvoie un chemin dessingant une colonie du joueur i à l'origine
	 * @param i 
	 */
	public ColoniePath(int i) {
		super(i);
		PionBuilder.makeColonie(this, w, h);
	}
	
	public void setX(int x){
		super.setX((int)(x-w/2));
	}
	
	public void setY(int y){
		super.setY((int)(y+h/2));
	}
}



class VillePath extends PionJoueurPath{

	public static final double VILLE_HEIGHTR = 0.25;
	public static final double VILLE_WIDTHR = 0.20;

	
	public static final int w = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH * VILLE_WIDTHR);
	public static final int h = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH * VILLE_HEIGHTR);
	
	/**
	 * Renvoie un chemin dessingant une ville du joueur i à l'origine
	 * @param i 
	 */
	public VillePath(int i) {
		super(i);
		PionBuilder.makeVille(this, w, h);
	}
	
	public void setX(int x){
		super.setX((int)(x-w/3));
	}
	
	public void setY(int y){
		super.setY((int)(y+h/3));
	}
	
}

enum SideDirection{LEFT,NONE,RIGHT};

class RoutePath extends PionJoueurPath{

	
	
	public static final double ROUTE_WIDTHR = 0.15;
	public static final double ROUTE_OFFSETR = 0.20;

	public static final int w = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH * ROUTE_WIDTHR);
	public static final int off = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH * ROUTE_OFFSETR);
	
	public RoutePath(int i, SideDirection dir) {
		super(i);
		PionBuilder.makeRoute(this, w, off, dir);
	}
	
}

class TransportPath extends PionJoueurPath{

	
	
	public static final double BATEAU_HEIGHTR = 0.10;
	public static final double BATEAU_OFFSETR = 0.33;

	public static final int h = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH*BATEAU_HEIGHTR);
	public static final int off = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH * BATEAU_OFFSETR);
	
	public TransportPath(int i, SideDirection dir) {
		super(i);
		PionBuilder.makeTransport(this, h, off, dir);
	}
}

class CargoPath extends PionJoueurPath{

	
	
	public static final double CARGO_HEIGHTR = 0.10;
	public static final double CARGO_OFFSETR = 0.23;

	public static final int h = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH*CARGO_HEIGHTR);
	public static final int off = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH*CARGO_OFFSETR);
	
	public CargoPath(int i, SideDirection dir) {
		super(i);
		PionBuilder.makeCargo(this, h, off, dir);
	}
}

class VoilierPath extends PionJoueurPath{

	
	
	public static final double VOILLIER_HEIGHTR = 0.10;
	public static final double VOILLIER_OFFSETR = 0.15;

	public static final int h = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH*VOILLIER_HEIGHTR);
	public static final int off = (int)(HexagonePath.HEXAGONES_SIDE_LENGTH*VOILLIER_OFFSETR);
	
	public VoilierPath(int i, SideDirection dir) {
		super(i);
		PionBuilder.makeVoilier(this, h, off, dir);
	}
}
